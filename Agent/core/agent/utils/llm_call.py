import os

from openai import AsyncOpenAI

from core.agent.utils.base import BaseCallLlm


class asyncCallLlm(BaseCallLlm):
    """
    LLM의 응답을 파싱하는 클래스입니다.
    """
    def __init__(self, response: str):
        self.response = response
        self.OPEN_API_KEY = os.getenv("OPEN_API_KEY")

    @property
    def _create_client(self):
        if not self.OPEN_API_KEY:
            raise ValueError("OPEN_API_KEY is not set in environment variables.")
        return AsyncOpenAI(self.OPEN_API_KEY)

    async def llm_call(self, prompt: str, model = "gpt-4o") -> str:
        messages = []
        messages.append({"role": "system", "content": prompt})
        chat_completion = await self._create_client.chat.completions.create(
            model=model,
            messages=messages
        )
        return chat_completion.choices[0].message.content

