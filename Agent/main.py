import json
import streamlit as st

from src.llm.openai_client import OpenAIClient
from src.agent.prompts.search_company_info_prompt import CompanyInfoPrompt, SystemPropmt
from src.agent.tools.tool_registry import TOOLS

class StockResearchAgent:
    def __init__(self):
        self.llm = OpenAIClient(model="gpt-4o")
        self.tools = [tool.schema() for tool in TOOLS]
        self.tool_map = {tool.name: tool for tool in TOOLS}
        self.messages = []

    def __str__(self):
        return "StockResearchAgent using tools: " + ", ".join([tool.name for tool in TOOLS])

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
                    {"role": "system", "content": SystemPropmt.system_prompt,
                    "role": "user", "content": final_prompt}
                ]
            )
            response_chain.append(response.content)    # LLM 응답 결과를 다음 프롬프트의 입력으로 사용
            prev_response = response.content           # 다음 프롬프트의 입력을 업데이트
        return response_chain, final_prompts           # 최종 응답 체인과 최종 프롬프트 반환

    def process(self):
        # streamlit UI 설정
        st.set_page_config(page_title="Stock Research Agent", page_icon="📈")
        st.title("📈 Stock Research Agent")

        # User input
        initial_input = st.text_area("궁금한 주식 정보 물어보세요:", height=100)
        custom_prompt = []
        # with st.expander("단계별 프롬프트 설정", expanded=False):
            # prompt chaining 실행
        if st.button("정보 검색 시작"):
            with st.spinner("정보를 검색하는 중입니다..."):
                final_response_chain, final_prompts = self.prompt_chaining(
                    initial_input, CompanyInfoPrompt.search_company_info_prompt
                )
        final_result_tab, details_tab = st.tabs(["최종 결과", "상세 과정"])

        with final_result_tab:
            st.write(final_response_chain)

        with details_tab:
            for i, (prompt, response) in enumerate(
                    zip(final_prompts, final_response_chain)
            ):
                with st.expander(f"단계 {i + 1}"):
                    st.markdown(f"**프롬프트**\n```\n{prompt}\n```")
                    st.markdown(f"**응답**\n```\n{response}\n```")


if __name__ == "__main__":
    agent = StockResearchAgent()
    agent.process()