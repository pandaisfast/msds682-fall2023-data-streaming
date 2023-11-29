# Demo 1. Linear or Sequential workflow

# dag_1_geet_system_datetime_csv.py
import pandas as pd
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Function to process the datetime
def process_datetime_fn(ti):
    dt_string = ti.xcom_pull(task_ids='get_datetime')  # Pull data from previous task
    try:
        dt = datetime.strptime(dt_string, '%a %b %d %H:%M:%S %Z %Y')
        # Return processed datetime as a dictionary
        return {
            'year': dt.year,
            'month': dt.strftime('%b'),
            'day': dt.day,
            'time': dt.strftime('%H:%M:%S'),
            'day_of_week': dt.strftime('%a')
        }
    except ValueError as e:
        print("Error processing datetime:", e)
        return {}

# Function to save the processed datetime
def save_datetime_fn(ti):
    dt_processed = ti.xcom_pull(task_ids='process_datetime')
    if dt_processed:
        df = pd.DataFrame([dt_processed])
        file_path = '/Users/Shared/msds682-fall2023-data-streaming/docs/assets/msds-airflow-demo1/output/output_csv_file.csv'
        header = not os.path.exists(file_path)
        df.to_csv(file_path, mode='a', header=header, index=False)

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 1),
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
with DAG(
    'Demo_1_updated',
    default_args=default_args,
    description='Demo 1 - Updated',
    schedule_interval='* * * * *',  # Cron expression (every minute)
    catchup=False,
) as dag:

    # Task to get current datetime
    get_datetime = BashOperator(
        task_id='get_datetime',
        bash_command='date',  # Bash command to get current date
    )

    # Task to process datetime
    process_datetime = PythonOperator(
        task_id='process_datetime',
        python_callable=process_datetime_fn,  # Python function to be executed
    )

    # Task to save processed datetime
    save_datetime = PythonOperator(
        task_id='save_datetime',
        python_callable=save_datetime_fn,  # Python function to be executed
    )

    # Set task dependencies
    get_datetime >> process_datetime >> save_datetime

# airflow tasks test Demo_1_updated get_datetime 2023-01-01
# airflow tasks test Demo_1_updated process_datetime 2023-01-01
# airflow tasks test Demo_1_updated save_datetime 2023-01-01