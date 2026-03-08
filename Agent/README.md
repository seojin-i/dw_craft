# Stock Ressearch Agent (주식 정보 조사 에이전트)
- uv + OpenAI 프로젝트 구조
- 목적: 
  - 이 프로젝트는 uv 프레임워크와 OpenAI API를 활용하여 다양한 기능을 구현하는 것을 목표로 합니다. 아래는 프로젝트의 주요 디렉토리 및 파일 구조에 대한 설명입니다.
- 특징: 
  - 이 Agent는 특정 종목의 공개된 정보를 수집·요약·설명한다.
  - 투자 판단이나 매매 조언은 하지 않는다.
- 디렉토리 구조 
```
agent/
├─ pyproject.toml
├─ uv.lock
├─ .env                     # OPENAI_API_KEY
│
├─ core/
│  ├─ agent/
│  │  └─ base.py
│  │  └─ SearchAgent.py
│  │  └─ ThemaAgent.py
│  ├─ prompts/
│  │  └─ router_prompt.py
│  │  └─ search_company_info_prompt.py
│  ├─ test/
│  ├─ tools/
│  │  └─ base.py
│  │  └─ company_profile.py
│  │  └─ dynamic_crwaling.py
│  │  └─ static_crawling.py
│  │  └─ tool_registry.py
│  ├─ utils/
│  │  └─ base_call_llm.py
│  ├─ validator/
│  │  └─ tool_registry.py
│  ├─ llm/
│  │  └─ validate_wrapper.py
├─ backend/
│
├─ main.py
└─ README.md
```
내부 Agent 구조 설명
```
User
 ↓
RouterAgent
 ├─ SearchAgent
 ├─ ThemaAgent
 ├─ ...
 ↓
Synthesizer (LLM)
 ↓
User
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
5. Streamlit UI 실행  
   프로젝트 루트 디렉토리에서 `main.py`를 실행하여 에이전트를 시작합니다.
   ```bash
   streamlit run main.py
   ```
6. UI에서 종목명 입력  
   Streamlit UI에서 관심 있는 종목명을 입력하고 에이전트가 정보를 수집·요약·설명하는 과정을 확인합니다.
   관심있는 주식 명을 입력해도 동작합니다. (예시: "삼성전자", "애플", "테슬라" 등)