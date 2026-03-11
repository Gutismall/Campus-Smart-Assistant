import os
from .base import BaseLLMClient

def get_llm_client() -> BaseLLMClient:
    """
    Factory function that reads LLM_PROVIDER from .env and returns
    the appropriate LLM client instance.

    Supported values for LLM_PROVIDER:
      - "gemini"  → Google Gemini (default)
      - "openai"  → OpenAI GPT models

    To add a new provider:
      1. Create a new file in services/llm/ (e.g. anthropic.py)
      2. Implement BaseLLMClient
      3. Add a new case to this factory
      4. Set LLM_PROVIDER=your_provider in .env
    """
    provider = os.environ.get("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        from .gemini import GeminiClient
        return GeminiClient()

    elif provider == "openai":
        from .openai import OpenAIClient
        return OpenAIClient()

    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER '{provider}'. "
            "Supported values: 'gemini', 'openai'."
        )
