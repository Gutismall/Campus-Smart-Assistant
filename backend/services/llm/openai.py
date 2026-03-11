import os
from .base import BaseLLMClient

class OpenAIClient(BaseLLMClient):
    """OpenAI LLM provider (GPT-4o, GPT-3.5, etc.)."""

    def __init__(self):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package is not installed. Add 'openai' to requirements.txt."
            )

        api_key = os.environ.get("OPENAI_API_KEY")
        self._model_name = os.environ.get("OPENAI_MODEL")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")

        self._client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
