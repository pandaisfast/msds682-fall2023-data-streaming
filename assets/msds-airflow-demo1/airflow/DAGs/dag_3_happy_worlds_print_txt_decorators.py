# Demo 3. Decorators

# REVIEW: Demo 2. Dependency-based Workflow
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


#### ABOVE CODE IS THE SAME AS DEMO 2 ####

from airflow.decorators import dag, task

# @dag decoratesto denote it's the main function
@dag(
    dag_id='Demo_3_decorator',
    default_args=default_args,
    schedule_interval='* * * * *',  # Every minute
    catchup=False
)
def demo_dag():
    # Task 1: Bash Script
    @task(task_id='hello_world_task')
    def hello_world():
        # Execute your bash command or script here
        return 'Bash command executed'

    # Task 2: Python Script
    @task(task_id='hello_world_2_task')
    def hello_world_2():
        print("Hello World 2")
        return 'Python script executed'

    # Task 3: Independent Python Script
    @task(task_id='python_script_3_task')
    def run_python_script_3():
        # Execute your script here
        return 'Python script 3 executed'

    # Task 4: Generate a TXT Document
    @task(task_id='generate_run_details_task')
    def generate_run_details():
        now = datetime.now()
        # Write to file or perform other actions
        return f"Run successful\nTime: {now.strftime('%Y-%m-%d %A %H:%M')}"

    # Setting up dependencies
    hello = hello_world() # Instantiate the task within the DAG context
    hello2 = hello_world_2()
    script3 = run_python_script_3()
    generate_details = generate_run_details()

    [hello, hello2] >> script3 >> generate_details

# Instantiate the DAG
demo_workflow = demo_dag()

    # airflow tasks test Demo_3_decorator hello_world_task 2023-01-01
    # airflow tasks test Demo_3_decorator hello_world_2_task 2023-01-01
    # airflow tasks test Demo_3_decorator python_script_3_task 2023-01-01
    # airflow tasks test Demo_3_decorator generate_run_details_task 2023-01-01
