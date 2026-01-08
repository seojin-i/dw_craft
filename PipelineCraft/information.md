1. Architecture (ELT)
   - wikimedia API data -> Docker Airflow -> Postgres DB Load -> DBT + Airflow(PySpark)

2. Environment && Architecture Properties
  - Tool: Docker Desktop, pycharm
  - Language: python    
  - 2-1. 시스템 환경
     - WSL2 이용하여 윈도우에서 Airflow Install
     - WSL2가 사용할 Docker Desktop 다운로드 후 설치 (docker desktop에서 wsl2 기반 리눅스 배포판 사용하도록 설정 필요)
     - Airflow/Postgresql DB/Redis Container 생성 + 웹서버 및 스케줄러 실행 후 확인
  - 2-2. Airflow DAG 개발
     - Wikimedia Data를 API Call 하여 가져오도록 DAG 구성 (rel. [Wikimedia Api Document Page][https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html#get-number-of-page-views-for-a-page])
     - 가져온 데이터를 postgre DB에 저장
   
3. Result Output
  - docker-compose.yaml
  - extract_apidata_load_db.py
  - README.md
