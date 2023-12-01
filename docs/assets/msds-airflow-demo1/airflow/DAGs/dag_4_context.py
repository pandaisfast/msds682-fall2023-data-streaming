import logging
import pendulum
from airflow.decorators import dag, task

# Define the DAG using the @dag decorator
# start_date is set to the current time with pendulum.now()
# schedule_interval="@daily" means the DAG will run once a day
@dag(
    dag_id='Demo_4',
    start_date=pendulum.now(),
    # schedule_interval="@daily", # cron presets like @daily, @hourly, @weekly,
    schedule_interval="* * * * *",  # This will schedule the DAG to run every minute
    catchup=False  # Avoids backfilling past dates for simplicity
)
def simple_log_details_dag():
    # Define a task using the @task decorator
    @task
    def log_execution_date(**kwargs):
        # Accessing the execution date from the context variables
        # 'ds' is a standard Airflow context variable for execution date in 'YYYY-MM-DD' format
        exec_date = kwargs['ds']
        # Logging the execution date
        logging.info(f"Execution date is {exec_date}")

    # Instantiate the task within the DAG context
    log_execution_date_task = log_execution_date()

# Create the DAG instance to be recognized by Airflow
simple_log_details = simple_log_details_dag()

# airflow tasks test Demo_4 log_execution_date 2023-01-01
