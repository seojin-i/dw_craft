1. Architecture (ELT)
   - RDB -> Airflow(PySpark Extract + Load) -> Databricks -> DBT + Airflow(PySpark) -> DashBoard 

2. 구성 환경
  - WSL2 이용하여 윈도우에서 리눅스 환경 설정. or Mac 에서 Airflow Install
  - WSL2가 사용할 Docker Desktop 다운로드 후 설치 (docker desktop에서 wsl2 기반 리눅스 배포판 사용하도록 설정 필요)
  - Airflow 설치 + 웹서버 및 스케줄러 실행 후 확인

3. 
