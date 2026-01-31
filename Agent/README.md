# uv + OpenAI 프로젝트 구조
이 프로젝트는 uv 프레임워크와 OpenAI API를 활용하여 다양한 기능을 구현하는 것을 목표로 합니다. 아래는 프로젝트의 주요 디렉토리 및 파일 구조에 대한 설명입니다.
```
agent/
├─ pyproject.toml
├─ uv.lock
├─ .env                     # OPENAI_API_KEY
│
├─ src/
│  ├─ agent/
│  │  ├─ agent.py
│  │  ├─ planner.py
│  │  ├─ memory.py
│  │  ├─ tools.py
│  │  └─ prompts.py
│  │
│  └─ llm/
│     └─ openai_client.py
│
├─ main.py
└─ README.md
```

### Project start guide
1. OpenAI API Key 설정  
   `.env` 파일에 OpenAI API Key를 추가합니다.
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
2. create pyproject.toml  
   프로젝트 루트 디렉토리에서 `pyproject.toml` 파일을 생성하고 최소 필요 조건의 의존성을 추가합니다.
   ```toml
    [project]
    name = "toy-openai-agent"
    version = "0.1.0"
    requires-python = ">=3.11"
    
    dependencies = [
      "openai>=1.12.0",
      "pydantic>=2.6",
      "python-dotenv>=1.0",
      "rich>=13.7"
    ]
   ```
3. uv install && 패키지 의존성 설치
```bash
pip install uv
uv sync
```
4. git fork & clone  
   이 저장소를 포크한 후 로컬 머신에 클론합니다.