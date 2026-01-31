import json
from pprint import pprint

from src.llm.openai_client import OpenAIClient
from src.agent.tools.tool_registry import TOOLS

SYSTEM_PROMPT = """
You are a stock research assistant.
When the user mentions a company name,
you MUST call the get_company_profile tool.
You MUST always provide the company_name argument.
Do NOT answer from your own knowledge.
AND
You explain company information and public facts.
You do NOT give investment advice.
You organize your answer into:
1. Company overview
2. Recent issues
3. Financial trend summary
4. Risks and things to watch
"""


class StockResearchAgent:
    def __init__(self):
        self.llm = OpenAIClient(model="gpt-4o-mini")
        self.tools = [tool.schema() for tool in TOOLS]
        self.tool_map = {tool.name: tool for tool in TOOLS}

    def __str__(self):
        return "StockResearchAgent using tools: " + ", ".join([tool.name for tool in TOOLS])

    def process(self, **kwargs):
        while True:
            user_input = input("Enter your stock research query: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Bye 👋")
                break

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]

            try:
                # 1️⃣ 첫 LLM 호출 (tool 선택)
                response = self.llm.chat(messages, tools=self.tools)

                # 2️⃣ tool 호출 처리
                if response.tool_calls:
                    # 🔥 1. assistant 메시지를 먼저 추가
                    messages.append({
                        "role": "assistant",
                        "content": response.content,
                        "tool_calls": [
                            {
                                "id": call.id,
                                "type": "function",
                                "function": {
                                    "name": call.function.name,
                                    "arguments": call.function.arguments,
                                }
                            }
                            for call in response.tool_calls
                        ]
                    })

                    # 🔥 2. tool 실행 & tool 메시지 추가
                    for call in response.tool_calls:
                        tool_name = call.function.name
                        tool_args = json.loads(call.function.arguments)

                        tool = self.tool_map[tool_name]
                        result = tool.process(**tool_args)

                        messages.append({
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": json.dumps(result, ensure_ascii=False)
                        })
                    # 🔥 3. tool 결과 포함해 다시 호출
                    response = self.llm.chat(messages)

                # 4️⃣ 최종 답변 출력
                print("\n" + "=" * 50)
                print(response.content)
                print("=" * 50 + "\n")

            except Exception as e:
                print(f"Error during LLM chat: {e}")
                continue


if __name__ == "__main__":
    # llm = OpenAIClient(model="gpt-4o-mini")
    agent = StockResearchAgent()
    agent.process()