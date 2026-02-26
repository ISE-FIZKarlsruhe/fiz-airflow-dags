from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="demo1",
    start_date=datetime(2022, 1, 1),
    schedule="0 0 * * *",
    catchup=False,
    tags=["demo"],
)
def demo1():

    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task
    def airflow():
        print("airflow from python")

    hello >> airflow()

# Instantiate the DAG (required for Airflow to pick it up)
dag = demo1()
