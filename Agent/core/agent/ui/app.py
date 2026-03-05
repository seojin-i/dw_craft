import streamlit as st
from datetime import datetime

from core.agent.agents.RouterAgent import RouterAgent

class StreamlitUI:
    def __init__(self):
        self.router = RouterAgent()
        # =========================
        # 2️⃣ Streamlit 기본 설정
        # =========================
        st.set_page_config(
            page_title="Stock AI Chat",
            page_icon="📈",
            layout="centered"
        )

        st.title("📈 Stock Research Chatbot")

        # =========================
        # 3️⃣ 세션 상태 초기화
        # =========================
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # =========================
        # 4️⃣ 기존 메시지 출력
        # =========================
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # =========================
        # 5️⃣ 사용자 입력 받기
        # =========================
        self.user_input = st.chat_input("궁금한 주식 정보를 입력하세요...")  # 초기값 설정

        if self.user_input:
            # 1️⃣ 사용자 메시지 저장
            st.session_state.messages.append({
                "role": "user",
                "content": self.user_input,
                "timestamp": datetime.now()
            })

            with st.chat_message("user"):
                st.markdown(self.user_input)

            # 2️⃣ Agent 호출
            with st.spinner("AI가 분석 중입니다..."):
                # RouterAgent가 적절한 Agent로 라우팅하여 응답 생성
                agent = self.router.process(prompt=self.user_input)

                if isinstance(agent, str):
                    response = agent
                    debug_info = None
                else:
                    # Sub-Agent의 process 메서드를 호출하여 최종 응답 생성
                    response = agent.process(user_input=self.user_input)
                    debug_info = getattr(agent, 'debug_log', None)

            # 3️⃣ Assistant 메시지 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now()
            })

            with st.chat_message("assistant"):
                st.markdown(response)

            # 4️⃣ 뉴스 목록 별도 표시
            if debug_info:
                for log in debug_info:
                    if log.get("step") == "Tool 결과" and isinstance(log.get("result"), list):
                        with st.expander("📰 크롤링된 뉴스 원본 데이터"):
                            for i, item in enumerate(log["result"], 1):
                                st.markdown(f"**{i}.** {item}")

            # 5️⃣ 내부 동작 과정 표시
            with st.expander("🔍 내부 동작 과정 보기"):
                st.markdown(f"**1단계: 라우팅**")
                st.code(self.router.last_routing_result, language="text")
                st.markdown(f"**선택된 Agent:** `{agent}`")

                if debug_info:
                    for i, log in enumerate(debug_info):
                        st.markdown(f"**{i+1}. {log['step']}**")
                        st.json(log)
