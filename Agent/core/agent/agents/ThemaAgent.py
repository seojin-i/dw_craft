from core.agent.agents.base import BaseAgent
class ThemaInfoAgent(BaseAgent):
    def __init__(self, model="gpt-4o"):
        super().__init__(model)
        self.messages = []

    def __str__(self):
        return "ThemaInfoAgent"

    def __call__(self, *args, **kwargs):
        return self.process()

    def process(self):
        pass