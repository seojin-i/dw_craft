from core.agent.agents.base import BaseAgent
class ThemaInfoAgent(BaseAgent):
    def __init__(self, model="gpt-4o"):
        super().__init__(model)
        self.messages = []

    @property
    def process(self):
        pass