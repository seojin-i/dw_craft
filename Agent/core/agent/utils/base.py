from abc import ABC, abstractmethod

class BaseCallLlm(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def llm_call(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses.")