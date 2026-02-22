from abc import ABC, abstractmethod

from core.llm.openai_client import OpenAIClient

class BaseAgent(ABC):
    def __init__(self, model="gpt-4o"):
        self.llm = OpenAIClient(model=model)
        self.messages = []

    def act(self, observation):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def learn(self, experience):
        raise NotImplementedError("This method should be overridden by subclasses.")