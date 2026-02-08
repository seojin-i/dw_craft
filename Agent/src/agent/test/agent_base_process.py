import json

from src.agent.prompts.search_company_info_prompt import CompanyInfoPrompt

def process(self, **kwargs):
    while True:
        user_input = input("궁금한 주식 정보 물어보세요: ").strip()
        if user_input.lower() in {"exit", "quit", "안녕", "종료"}:
            print("Bye 👋")
            break

        self.messages = [
            {"role": "system", "content": CompanyInfoPrompt.search_company_info_prompt},
            {"role": "user", "content": user_input}
        ]

        try:
            # 1️⃣ 첫 LLM 호출 (tool 선택)
            response = self.llm.chat(self.messages, tools=self.tools)

            # 2️⃣ tool 호출 처리
            if response.tool_calls:
                # 🔥 1. assistant 메시지를 먼저 추가
                self.messages.append({
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

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                # 🔥 3. tool 결과 포함해 다시 호출
                response = self.llm.chat(self.messages)

            # 4. 최종 결과를 답변으로 설정
            self.messages.append({
                "role": "assistant",
                "content": response.content
            })

            # 5. 최종 답변 출력
            print("\n" + "=" * 50)
            # print(result_response.content)
            print(response.content)  # class 'openai.types.chat.chat_completion_message.ChatCompletionMessage'
            print("=" * 50 + "\n")

        except Exception as e:
            print(f"Error during LLM chat: {e}")
            continue