from abc import ABC, abstractmethod
class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    def act(self, observation):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def learn(self, experience):
        raise NotImplementedError("This method should be overridden by subclasses.")