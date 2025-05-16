from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.email import send_email
from src.extract import extract_breweries
from src.transform import transform_to_silver
from src.aggregate import aggregate_to_gold
from src.validate import (
    validate_bronze_data,
    validate_silver_data,
    validate_gold_data,
)
from src.metrics import log_metrics


def failure_alert(context):
    dag_run = context.get("dag_run")
    task = context.get("task_instance")
    message = f"""
    🚨 Falha na DAG {dag_run.dag_id}
    Tarefa: {task.task_id}
    Execução: {dag_run.execution_date}
    Erro: {context.get('exception')}
    """
    print(message)
    send_email(to="devteam@example.com", subject="🚨 Airflow Task Failure", html_content=message)


def format_date(ds: str) -> str:
    return ds.replace("-", "")


default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes=1),
    "email_on_failure": True,
    "on_failure_callback": failure_alert,
}

with DAG(
    dag_id="breweries_etl_pipeline",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Pipeline ETL com Bronze, Silver e Gold usando dados da Open Brewery DB",
    default_args=default_args,
) as dag:

    t1 = PythonOperator(
        task_id="extract_breweries",
        python_callable=extract_breweries,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
    )

    t_check_bronze = PythonOperator(
        task_id="validate_bronze_data",
        python_callable=validate_bronze_data,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
        retries=0,
        depends_on_past=False,
    )

    t2 = PythonOperator(
        task_id="transform_to_silver",
        python_callable=transform_to_silver,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
        trigger_rule="all_done",
    )

    t_check_silver = PythonOperator(
        task_id="validate_silver_data",
        python_callable=validate_silver_data,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
        retries=0,
        depends_on_past=False,
    )

    t3 = PythonOperator(
        task_id="aggregate_to_gold",
        python_callable=aggregate_to_gold,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
        trigger_rule="all_done",
    )

    t_check_gold = PythonOperator(
        task_id="validate_gold_data",
        python_callable=validate_gold_data,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
        retries=0,
        depends_on_past=False,
    )

    t_log_metrics = PythonOperator(
        task_id="log_metrics",
        python_callable=log_metrics,
        op_kwargs={"execution_date": "{{ ds | replace('-', '') }}"},
        trigger_rule="all_done",
    )

    t1 >> t_check_bronze >> t2 >> t_check_silver >> t3 >> t_check_gold >> t_log_metrics
