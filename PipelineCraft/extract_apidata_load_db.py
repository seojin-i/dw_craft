"""
API Call을 통해 Data를 Extract && Load 하기 위한 DAG
"""
import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable

# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 1), # 9/1의 Data부터 처리하기 위함.
    'retries': 1,
}

def get_api_data(**context):
    """
    API를 호출하여 xcom으로 다음 Task에 전달
    :param context: Airflow Variables Info
    :return: Requests.Response.Json
    """
    start_date = context['data_interval_start']
    print(type(start_date))
    end_date = start_date + timedelta(days=7)
    url = Variable.get("api_url")
    url = url.format(start_date = start_date.strftime("%Y%m%d"), end_date = end_date.strftime("%Y%m%d"))
    print('** url: ', url)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()
    return data

def save_to_postgres(**context):
    """
    전달받은 api data를 Table에 적재하기 위한 변환 과정
    :param context: Requests.Response.Json Object
    :return:
    """
    # XCom에서 데이터 가져오기
    json_data = context['ti'].xcom_pull(task_ids='get_api_data')
    items = json_data.get("items", [])
    print('** items: ', items)

    if not items:
        print("No data to insert")
        return

    # PostgreSQL 연결
    pg_hook = PostgresHook(postgres_conn_id='assignment_db')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # batch insert
    records = [
        (
            d['project'],
            d['article'],
            d['granularity'],
            datetime.strptime(d['timestamp'], "%Y%m%d%H"),
            d['access'],
            d['agent'],
            d['views']
        )
        for d in items
    ]

    # executemany로 한 번에 삽입
    cursor.executemany(
        """
        INSERT INTO public.data_engineering_page_view
        (project, article, granularity, timestamp, access, agent, views)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (article, timestamp) DO NOTHING
        """,
        records
    )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(records)} rows inserted into PostgreSQL")

with DAG(
        dag_id='wikimedia_pageviews_to_postgres',
        default_args=default_args,
        schedule_interval='@daily',
        catchup=True
) as dag:
    get_api_data = PythonOperator(
        task_id='get_api_data',
        python_callable=get_api_data,
        provide_context=True,
    )
    save_to_postgres = PythonOperator(
        task_id='save_to_postgres',
        python_callable=save_to_postgres,
        provide_context=True,
    )
get_api_data >> save_to_postgres
