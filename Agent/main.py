import asyncio

from core.agent.utils.llm_call import asyncCallLlm
from core.agent.ui.app import StreamlitUI

if __name__ == "__main__":
    # asyncio.run()
    StreamlitUI()