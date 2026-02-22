from core.agent.agents.SearchAgent import StockResearchAgent
from core.agent.agents.ThemaAgent import ThemaInfoAgent
from core.agent.prompts.search_company_info_prompt import CompanyInfoPrompt, SystemPropmt
from core.agent.prompts.thema_info_prompt import ThemaInfoPrompt

class RouterAgent:
    def __init__(self):
        self.stock_research_agent = StockResearchAgent()
        self.thema_info_agent = ThemaInfoAgent()
    def __call__(self, *args, **kwargs):
        return self.process()

    def process(self, **kwargs):
        if  kwargs["prompt"] == SystemPropmt:
            return self.stock_research_agent.process
        elif kwargs["prompt"] == ThemaInfoPrompt:
            return self.thema_info_agent.process
        else:
            pass

if __name__ == "__main__":
    router_agent = RouterAgent()
    # router_agent.process(prompt=SystemPropmt)