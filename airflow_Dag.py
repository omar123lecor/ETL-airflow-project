from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from youtube_ETL import main

dafault_args = {
    'owner' : 'airflow',
    'depends_on_past':False,
    'start_date': datetime(2024,25,9),
    'email':'sabor.zahra15@gmail.com',
    'email_on_failure':True,
    'email_on_retry':True,
    'retries': 1,
    'retry_delay' : timedelta(minutes=1)
}

dag = DAG(
    'Youtube_dag',
    default_args=dafault_args,
    description='My first test'
)
run_etl = PythonOperator(
    task_id='complet_youtube_etl',
    python_callable=main,
    dag = dag,
)

run_etl