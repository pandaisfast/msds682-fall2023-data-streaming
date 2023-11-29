# dag_0_starter.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
with DAG(
    'hello_world',
    default_args=default_args,
    description='Hello World',
    schedule_interval='* * * * *',  # Cron expression (every minute)
    catchup=False,
    
) as dag:

    # Task to get current datetime
    get_datetime = BashOperator(
        task_id='get_datetime',
        bash_command='date',  # Bash command to get current date
    )
    
## airflow tasks test hello_world get_datetime 2023-11-28