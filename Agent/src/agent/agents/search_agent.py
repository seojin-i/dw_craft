from src.agent.tools.tool_registry import get_tool_schema, run_rool

tools = get_tool_schema()

result = run_rool("get_company_profile", company_name="Apple Inc.")