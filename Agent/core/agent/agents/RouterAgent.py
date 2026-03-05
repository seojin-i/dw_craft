from .base import BaseAgent
from .SearchAgent import StockResearchAgent
from .ThemaAgent import ThemaInfoAgent
from core.agent.prompts.search_company_info_prompt import CompanyInfoPrompt, SystemPropmt
from core.agent.prompts.thema_info_prompt import ThemaInfoPrompt
from core.agent.prompts.router_prompt import RouterPrompt

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.stock_research_agent = StockResearchAgent()
        self.thema_info_agent = ThemaInfoAgent()

    def __call__(self, *args, **kwargs):
        return self.process()

    def process(self, **kwargs):
        category = self.llm.chat([
            {"role": "system", "content": RouterPrompt.router_prompt},
            {"role": "user", "content": kwargs.get("prompt", "")}
        ])
        self.last_routing_result = category.content  # 라우팅 결과 저장
        if "stock_research_agent" in category.content:
            return self.stock_research_agent
        elif "thema_info_agent" in category.content:
            return self.thema_info_agent
        else:
            return "처리할 수 없는 질문 유형입니다"

if __name__ == "__main__":
    router_agent = RouterAgent()
    # router_agent.process(prompt=SystemPropmt)