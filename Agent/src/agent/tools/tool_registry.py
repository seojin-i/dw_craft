from .company_profile import CompanyProfileTool
from .static_crawling import WebStaticCrawlingTool
from .dynamic_crawling import WebDynamicCrawlingTool
TOOLS = {
    "search_company": CompanyProfileTool(),
    "static_web_crawling" : WebStaticCrawlingTool(),
    "dynamic_web_crawling" : WebDynamicCrawlingTool()
}

def get_tool_by_name(name):
    """
    이름으로 도구를 찾는 함수
    :param name:
    :return:
    """
    for tool in TOOLS:
        if tool.name == name:
            return tool
    return None

# def get_tool_schema():
#     """
#     사용 가능한 도구의 schema를 반환하는 함수
#     :return:
#     """
#     return [tool.schema for tool in TOOLS]

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