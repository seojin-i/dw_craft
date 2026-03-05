import json

from core.agent.agents.base import BaseAgent
from core.agent.prompts.search_company_info_prompt import CompanyInfoPrompt, SystemPropmt
from core.agent.tools.tool_registry import TOOLS

class StockResearchAgent(BaseAgent):
    def __init__(self, model="gpt-4o"):
        super().__init__(model)
        self.messages = []

    def __str__(self):
        return "StockResearchAgent"

    def __call__(self, *args, **kwargs):
        return self.process()

    def prompt_chaining(self, user_input: str, prompt_chains: list[str]) -> list[str]:
        """
        Prompt chaining logic to handle multi-step reasoning.
        :param user_input:
        :return: list() -> messages
        """
        response_chain = []
        final_prompts = []          # 최종 프롬프트들을 저장할 리스트
        prev_response = user_input  # 이전 사용자의 질문
        for i, prompt in enumerate(prompt_chains):
            final_prompt = f"""
            {prompt}
            처음 사용자가 입력한 내용은 다음과 같아. 응답할 때 항상 이 내용을 고려해서 답변해줘
            {user_input}
            또한 응답시 아래 내용도 참고해서 답변해줘
            {prev_response}"""
            final_prompts.append(final_prompt)
            response = self.llm.chat(
                messages=[
                    {"role": "system", "content": SystemPropmt.system_prompt},
                    {"role": "user", "content": final_prompt}
                ]
            )
            response_chain.append(response.content)    # LLM 응답 결과를 다음 프롬프트의 입력으로 사용
            prev_response = response.content           # 다음 프롬프트의 입력을 업데이트
        return response_chain, final_prompts           # 최종 응답 체인과 최종 프롬프트 반환

    def process(self, user_input: str = None):
        self.debug_log = []  # 디버그 로그 초기화

        messages = [
            {"role": "system", "content": SystemPropmt.system_prompt},
            {"role": "user", "content": user_input},
        ]
        tool_schemas = [tool.schema() for tool in TOOLS.values()]
        self.debug_log.append({"step": "LLM 호출", "tools_available": [t.name for t in TOOLS.values()]})

        response = self.llm.chat(messages=messages, tools=tool_schemas)

        # Tool 호출이 있을 경우 실행 후 결과를 다시 LLM에 전달하여 추가 응답을 받는 로직
        if response.tool_calls:
            messages.append(response)  # assistant의 tool_calls 메시지 추가
            for call in response.tool_calls:
                tool_name = call.function.name
                tool_args = json.loads(call.function.arguments)
                self.debug_log.append({"step": "Tool 호출", "tool": tool_name, "args": tool_args})

                tool = TOOLS.get(tool_name)
                result = tool.process(**tool_args)
                self.debug_log.append({"step": "Tool 결과", "tool": tool_name, "result": result})

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": tool_name,
                    "content": json.dumps(result, ensure_ascii=False)
                })
            # LLM이 tool 호출 결과를 반영하여 최종 응답 생성
            final_response = self.llm.chat(messages=messages)
            self.debug_log.append({"step": "최종 응답 생성"})
            return final_response.content

        self.debug_log.append({"step": "Tool 호출 없이 직접 응답"})
        return response.content

    # @process.setter
    # def process(self):
    #     pass