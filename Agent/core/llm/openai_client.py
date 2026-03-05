import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
class OpenAIClient:
    def __init__(self, model="gpt-4"):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.openai_client = OpenAI(api_key=api_key)
        self.async_openai_client = AsyncOpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages, tools=None):
        """
        동기 클라이언트
        :param messages:
        :param tools:
        :return:
        """
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools
        )
        return response.choices[0].message

    async def async_chat(self, messages, tools=None):
        """
        비동기 클라이언트
        :param messages:
        :param tools:
        :return:
        """
        response = await self.async_openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools
        )
        return response.choices[0].message
    def __str__(self):
        return f"OpenAIClient(model={self.model})"

