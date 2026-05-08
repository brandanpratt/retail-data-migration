from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from etl.extract.extract_table import extract_table

default_args = {
    "owner": "brandan",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

tables = [
    "customers",
    "stores",
    "products",
    "orders",
    "order_items",
    "inventory",
    "payments"
]

with DAG(
    dag_id="retail_etl_pipeline",
    default_args=default_args,
    description="Retail ETL extraction pipeline",
    start_date=datetime(2026, 5, 1),
    schedule="@daily",
    catchup=False,
    tags=["retail", "etl", "sqlserver"],
) as dag:

    extraction_tasks = []

    for table in tables:

        task = PythonOperator(
            task_id=f"extract_{table}",
            python_callable=extract_table,
            op_args=[table]
        )

        extraction_tasks.append(task)