# Demo 2. Dependency-based Workflow
"""
repo1/
└── airflow/
    └── dags/
        ├── hello_world.sh
        ├── python_script_3.py
        └── example_dag.py
"""


# dag_2_happy_worlds_print_txt.py
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

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

dag = DAG(
    'Demo_2',
    default_args=default_args,
    schedule_interval='* * * * *',  # Every minute
)


# Task 1: Bash Script
hello_world_task = BashOperator(
    task_id='hello_world_task',
    ### Note!! https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html
    ### Space in the end is needed.
    bash_command='/Users/Shared/msds682-fall2023-data-streaming/docs/assets/msds-airflow-demo1/airflow/dags/hello_world.sh ',
    dag=dag
)

# Task 2: Python Script
def hello_world_2():
    print("Hello World 2")

hello_world_2_task = PythonOperator(
    task_id='hello_world_2_task',
    python_callable=hello_world_2,
    dag=dag,
)

# Task 3: Independent Python Script
def run_python_script_3():
    exec(open("/Users/Shared/msds682-fall2023-data-streaming/docs/assets/msds-airflow-demo1/airflow/dags/python_script_3.py").read())

python_script_3_task = PythonOperator(
    task_id='python_script_3_task',
    python_callable=run_python_script_3,
    dag=dag,
)


# Task 4: Generate a TXT Document
def generate_run_details():
    now = datetime.now()
    with open("/Users/Shared/msds682-fall2023-data-streaming/docs/assets/msds-airflow-demo1/output/run_details.txt", "w") as file:
        # file.write(f"Run successful\nRun number: [Your Logic for Run Number]\nTime: {now.strftime('%Y-%m-%d %A %H:%M')}")
        file.write(f"Run successful\nTime: {now.strftime('%Y-%m-%d %A %H:%M')}")
generate_run_details_task = PythonOperator(
    task_id='generate_run_details_task',
    python_callable=generate_run_details,
    dag=dag,
)

# Setting up dependencies

hello_world_task
hello_world_2_task
[hello_world_task, hello_world_2_task] >> python_script_3_task
python_script_3_task >> generate_run_details_task

    # airflow tasks test Demo_2 hello_world_task 2023-01-01
    # airflow tasks test Demo_2 hello_world_2_task 2023-01-01
    # airflow tasks test Demo_2 python_script_3_task 2023-01-01
    # airflow tasks test Demo_2 generate_run_details_task 2023-01-01

