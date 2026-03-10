import os
from google import genai
from .base import BaseLLMClient

class GeminiClient(BaseLLMClient):
    """Google Gemini LLM provider (google-genai SDK)."""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        self._model_name = os.environ.get("GEMINI_MODEL")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")

        self._client = genai.Client(api_key=api_key)

    @property
    def client(self) -> genai.Client:
        return self._client

    @property
    def model_name(self) -> str:
        return self._model_name

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model_name,
            contents=prompt,
        )
        return response.text.strip()
