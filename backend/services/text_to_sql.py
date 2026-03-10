import os
import pathlib
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from google.genai import types
from services.llm import get_llm_client
from services.llm.gemini import GeminiClient
from services.tools import build_execute_sql_tool

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
            "Only include data belonging to their courses/tests."
        )
    elif role == "student":
        return (
            f"The current user is a student with student_id = {user_metadata['student_id']}. "
            "Only include data belonging to this student."
        )
    elif role == "admin":
        return "The current user is a system administrator with full read access."
    return "Unknown role. Do not return any personal data."


async def answer_question(question: str, user_metadata: dict | None, db: Session) -> str:
    """
    Uses Gemini Function Calling (Tool Use):
      1. The LLM receives the question + schema + an execute_sql tool.
      2. The LLM decides to call execute_sql with the appropriate SQL query.
      3. The SDK runs the tool, passes the result back to the LLM automatically.
      4. The LLM returns the final human-readable answer in one round-trip.
    """
    llm = get_llm_client()

    if not isinstance(llm, GeminiClient):
        return "Tool calling is not yet supported for the configured LLM provider."

    user_context = _build_user_context(user_metadata)
    system_instruction = f"{SCHEMA_CONTEXT}\n\nUser context: {user_context}"

    # Build the SQL tool with the current db session injected
    execute_sql = build_execute_sql_tool(db)

    chat = llm.client.chats.create(
        model=llm.model_name,
        config=types.GenerateContentConfig(
            tools=[execute_sql],
            system_instruction=system_instruction,
        ),
    )

    response = chat.send_message(question)
    
    # If the response has no text, it might be waiting for a tool result 
    # or it might have just returned a function call. 
    # The SDK usually handles the round-trip, but we need to ensure we grab the final text.
    if not response.text:
        # Check if the last part of the response is a function call
        # In case of manual handling or unexpected SDK state, return a fallback.
        return "The database assistant is processing your request..."

    return response.text.strip()
