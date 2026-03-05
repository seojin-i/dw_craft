from .company_profile import CompanyProfileTool
from .static_crawling import WebStaticCrawlingTool
from .dynamic_crawling import WebDynamicCrawlingTool

TOOLS = {
    "get_company_profile": CompanyProfileTool(),
    "Statistics_Web_Crawling": WebStaticCrawlingTool(),
    # "Dynamic_Web_Crawling": WebDynamicCrawlingTool()
}

def get_tool_by_name(name):
    """
    이름으로 도구를 찾는 함수
    :param name:
    :return:
    """
    return TOOLS.get(name, None)

def run_rool(tool_name, **kwargs):
    """
    도구를 실행하는 함수
    :param tool_name:
    :param kwargs:
    :return:
    """
    for tool in TOOLS:
        if tool.name == tool_name:
            return tool.process(**kwargs)
    raise ValueError(f"Tool {tool_name} not found")