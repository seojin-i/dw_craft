from src.llm.openai_client import OpenAIClient

SYSTEM_PROMPT = """
You are a stock research assistant.
You explain company information and public facts.
You do NOT give investment advice.
You organize your answer into:
1. Company overview
2. Recent issues
3. Financial trend summary
4. Risks and things to watch
"""

def process():
    llm = OpenAIClient(model="gpt-4o-mini")

    while True:
        user_input = input("Enter your stock research query: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye 👋")
            break

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        ## 한번만 질문하고 종료할 경우
        # response = llm.chat(messages, tools=None)
        ## 질문에 대한 루프를 돌게하고 싶은 경우
        messages.append({"role": "user", "content": user_input})
        try:
            response = llm.chat(messages, tools=None)
        except Exception as e:
            print(f"Error during LLM chat: {e}")
            continue
        messages.append({"role": "system", "content": response})
        print("\n" + "=" * 50)
        print(response)
        print("=" * 50 + "\n")

if __name__ == "__main__":
    result = process()
