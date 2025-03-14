from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta

Execution_date = datetime.now().strftime("%Y-%m-%d")


defaut_args = {
    'owner' : 'ndtien2004',
    'depends_on_past' : False,
    'start_date': datetime(2025,14,3),
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



