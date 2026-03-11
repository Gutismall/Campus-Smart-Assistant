import os
import pathlib
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from google.genai import types
from services.llm import get_llm_client
from services.llm.gemini import GeminiClient
from services.llm.openai import OpenAIClient
from services.tools import build_execute_sql_tool
import json

load_dotenv()

# Load the schema context from a dedicated prompt file so it stays human-readable.
# Falls back to the env var if the file doesn't exist.
_PROMPT_FILE = pathlib.Path(__file__).parent.parent / "prompts" / "schema_context.txt"
if _PROMPT_FILE.exists():
    SCHEMA_CONTEXT = _PROMPT_FILE.read_text(encoding="utf-8").strip()
else:
    SCHEMA_CONTEXT = os.environ.get("TEXT_TO_SQL_SCHEMA_CONTEXT", "").replace("\\n", "\n")


def _build_user_context(user_metadata: dict | None) -> str:
    if not user_metadata:
        return "The current user is unauthenticated. Do not return any personal data."
    role = user_metadata.get("role", "unknown")

    if role == "lecturer":
        return (
            f"The current user is a lecturer with lecturer_id = {user_metadata['lecturer_id']}. "
            "CRITICAL: You must ONLY return data belonging to their courses and tests. "
            "You are STRICTLY FORBIDDEN from returning information about any other lecturers or students. If requested, politely decline."
        )
    elif role == "student":
        return (
            f"The current user is a student with student_id = {user_metadata['student_id']}. "
            "CRITICAL: You must ONLY return data belonging to this exact student. "
            "You are STRICTLY FORBIDDEN from returning information about any other students or lecturers. If requested, politely decline."
        )
    elif role == "admin":
        return "The current user is a system administrator with full read access."
        
    return "Unknown role. Do not return any personal data."


async def answer_question(question: str, user_metadata: dict | None, db: Session) -> str:
    """
    Handles tool calling for both Gemini and OpenAI providers to execute SQL queries
    and return a natural language response.
    """
    llm = get_llm_client()
    user_context = _build_user_context(user_metadata)
    system_instruction = f"{SCHEMA_CONTEXT}\n\nUser context: {user_context}"
    
    execute_sql = build_execute_sql_tool(db)

    if isinstance(llm, GeminiClient):
        chat = llm.client.chats.create(
            model=llm.model_name,
            config=types.GenerateContentConfig(
                tools=[execute_sql],
                system_instruction=system_instruction,
            ),
        )

        response = chat.send_message(question)
        if not response.text:
            return "The database assistant is processing your request..."
        return response.text.strip()
        
    elif isinstance(llm, OpenAIClient):
        tools = [{
            "type": "function",
            "function": {
                "name": "execute_sql",
                "description": "Execute a SQL SELECT query against the campus PostgreSQL database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "A valid PostgreSQL SELECT statement."
                        }
                    },
                    "required": ["query"]
                }
            }
        }]
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": question}
        ]
        
        response = llm._client.chat.completions.create(
            model=llm._model_name,
            messages=messages,
            tools=tools,
            temperature=0,
        )
        
        response_msg = response.choices[0].message
        
        if response_msg.tool_calls:
            # Append the assistant's tool call message
            messages.append(response_msg)
            
            # Execute all tools the LLM requested
            for tool_call in response_msg.tool_calls:
                if tool_call.function.name == "execute_sql":
                    args = json.loads(tool_call.function.arguments)
                    result = execute_sql(args.get("query", ""))
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "execute_sql",
                        "content": str(result)
                    })
                    
            # Make a second call to get the final answer
            final_response = llm._client.chat.completions.create(
                model=llm._model_name,
                messages=messages,
                temperature=0,
            )
            return final_response.choices[0].message.content.strip()
        else:
            return response_msg.content.strip()

    else:
        return "Tool calling is not supported for the connected LLM provider."
