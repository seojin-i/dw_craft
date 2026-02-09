from .base import BaseTool
from .company_profile import CompanyProfileTool
from .web_crawling import WebCrawlingTool
from .validate_wrapper import ValidateWrapper
# from src.agent.tools.financial_data import FinancialDataTool
# from src.agent.tools.news_search import NewsSearchTool

def get_all_tools():
    """
    한번에 초기화 할 수 있도록 도와주는 함수
    :return:
    """
    return [
        BaseTool(),
        CompanyProfileTool(),
        WebCrawlingTool(),
        # FinancialDataTool(),
        # NewsSearchTool()
    ]
def get_tool_by_name(name):
    """
    이름으로 도구를 찾는 함수
    :param name:
    :return:
    """
    tools = get_all_tools()
    for tool in tools:
        if tool.name == name:
            return tool
    return None
def list_tool_names():
    """
    사용 가능한 도구 이름 목록을 반환하는 함수
    :return:
    """
    tools = get_all_tools()
    return [tool.name for tool in tools]
