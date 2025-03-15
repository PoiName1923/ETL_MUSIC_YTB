from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from postgres.init import *
from mongodb.init import *


Execution_date = datetime.now().strftime("%Y-%m-%d")


defaut_args = {
    'owner' : 'ndtien2004',
    'depends_on_past' : False,
    'start_date': datetime(2025,3,15),
    'email': ['nguyendinhtien23012004@gmail.com'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry-delay' :timedelta(minutes=1)
}

dags = DAG(
    dag_id= 'ETL_Music_Dag',
    default_args=defaut_args,
    description="This is my first Dag",
    schedule_interval='@daily'
)

get_data  = PythonOperator(
    tast_id = 'getting_data',
    python_callable=get_daily_data_mongo,
    dags=dags
)
load_data = PythonOperator(
    task_id = 'loading_data',
    python_callable=loading_daily_postgres,
    dags=dags
)


get_data>>load_data