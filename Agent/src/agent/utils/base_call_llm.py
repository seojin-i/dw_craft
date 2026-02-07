from abc import ABC, abstractmethod

class BaseCallLLM(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def call_llm(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses.")