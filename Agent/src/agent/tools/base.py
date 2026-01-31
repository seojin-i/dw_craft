from abc import ABC, abstractmethod
class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def schema(self) -> dict:
        """
        OpenAI tool schema
        """
        pass

    @abstractmethod
    def process(self, **kwargs) -> dict:
        """
        Actual tool execution
        """
        pass

    def validate(self, **kwargs):
        """
        Optional input validation
        """
        return True