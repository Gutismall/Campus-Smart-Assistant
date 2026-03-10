from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    """
    Abstract base class for all LLM providers.
    Any new provider must implement this interface.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and return the text response.
        All implementations must be synchronous at this layer;
        async handling is done by the caller.
        """
        ...
