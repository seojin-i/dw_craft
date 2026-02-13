import wikipedia
from src.agent.tools.base import BaseTool


class CompanyProfileTool(BaseTool):
    name = "get_company_profile"
    description = "특정 회사의 정보를 Wikipedia 사이트를 이용해서 조회하는 도구입니다."

    def schema(cls) -> dict:
        return {
            "type": "function",
            "function": {
                "name": cls.name,
                "description": (
                    "Fetch a company profile from Wikipedia. "
                    "You MUST provide a valid company_name."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_name": {
                            "type": "string",
                            "description": (
                                "Official company name to search on Wikipedia. "
                                "Example: 'Tesla, Inc.' or 'Apple Inc.'."
                            )
                        }
                    },
                    "required": ["company_name"]
                }
            }
        }

    def process(self, **kwargs) -> dict:
        company_name = kwargs.get("company_name")

        # 🔒 ②번 방어 코드 (여기!)
        if not company_name:
            return {
                "source": "wikipedia",
                "error": "company_name is required but was not provided"
            }

        if isinstance(company_name, list):
            company_name = company_name[0]

        wikipedia.set_lang("en")

        search_results = wikipedia.search(company_name)
        if not search_results:
            return {
                "source": "wikipedia",
                "company": company_name,
                "error": f"No Wikipedia page found for {company_name}"
            }

        page_title = search_results[0]
        summary = wikipedia.summary(page_title, sentences=3)

        return {
            "source": "wikipedia",
            "resolved_title": page_title,
            "profile_summary": summary + "\n\n[DEBUG_TAG_ABC123]"
        }
