# Data Pipeline Portfolio

## Project Intro
-  Api 호출 결과 데이터를 Airflow workflow를 이용하여 Postgresql DB Table로 적재하는 파이프라인 입니다.
-  이 모든 과정은 docker-compose로 구현 하였습니다. 

## Basic Info
- **OS**: Window
- **Language**: Python3.11 (Venv env)
- **Env**: docker-compose
    
## Pipeline Info
1. **주요 files**
   - **README.md**
     - 프로젝트의 이해를 돕기 위한 문서
     - 환경설정, 파이프라인 구성 및 실행방법에 대해서 안내 합니다.
   - **docker-compose.yaml**
     - 프로젝트를 구동하기 위한 docker-compose 실행 파일
   - **de-test/dags/extract_data_load_to_table.py**
     - Airflow Task를 위한 Dag File
2. **구조**
   - **Workflow**
       - Api Call -> Airflow Schedule -> Table Load
   - **Api Url & Params**
     - https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}
   - **Airflow Info**
     - **Schedule**: @daily
     - **start_date**: 2025-09-01 ~
     - **Catchup**: True
       - DAG Unpause 상태로 변경시 9/1 ~ 이후의 Data를 자동으로 Catchup 하도록 구성.
       - Daily로 
     - **DAG Logic**
       - `data_interval_start`를 기준으로 7일치의 Api Data를 Daily로 Export 합니다. 
       - Api Call시 이미 적재된 중복 Data가 존재하기에, 중복이 존재할 경우 적재 되지 않도록 Transform 처리를 합니다. 
       - 최종적으로 Table에 각 컬럼의 순서에 맞도록 Load 합니다. 
     - **etc**
       - Dag의 코드 재사용성을 위해 변수 값은 Airflow Variable을 통해 가져오도록 설정하였습니다.
       - DB Connection 정보는 Airflow의 Connections를 통해 가져오도록 설정하였습니다.
   - **DB Info**
     - **Type**: Postgresql DB
     - **Table Schema**
          ```sql
             CREATE TABLE "data_engineering_page_view" (
                    "id" SERIAL NOT NULL,
                    "project" VARCHAR(255) NULL DEFAULT NULL,
                    "article" VARCHAR(255) NULL DEFAULT NULL,
                    "granularity" VARCHAR(255) NULL DEFAULT NULL,
                    "timestamp" TIMESTAMP NULL DEFAULT NULL,
                    "access" VARCHAR(255) NULL DEFAULT NULL,
                    "agent" VARCHAR(255) NULL DEFAULT NULL,
                    "views" INTEGER NULL DEFAULT NULL,
                    "created_at" TIMESTAMP NULL DEFAULT now(),
             PRIMARY KEY ("id"),
             UNIQUE ("article", "timestamp");
          ```
## Connection Info
- **Postgresql DB (Data 적재용)**
   -   **Host**: `localhost`
   -   **Port**: `5433`
   -   **Username**: `assignment`
   -   **Password**: `assignment`
   -   **Database**: `assignment`
- **Airflow web**
   - **Host**: http://localhost:8080
   - **User**: `airflow`
   - **Password**: `airflow`

## Project Execute
1. **프로젝트 결과물 확인법**
   1.  **docker-compose 실행**
      - 아래 명령어를 사용하여 모든 서비스를 시작합니다. 
      - `.env` 파일 변경 내역은 없습니다.
           ```bash
           docker-compose up -d
           ```
   2.  **Airflow UI 접속하여 생성된 Dag과 Catchup 결과 확인**
      - **DB에 접속하여 적재된 Data 확인**
   4.  **DAG RUN을 Test로 수행하여 멱등성 확인하기** 
   5. **프로젝트 종료**
    - 결과 확인 후, 모든 서비스 종료.
         ```bash
         docker-compose down
         ```

## Project Result
- **프로젝트 결과물** 
   1. **README.md** 
   2. **dag file**
      - **dags/extract_data_load_to_table.py**
