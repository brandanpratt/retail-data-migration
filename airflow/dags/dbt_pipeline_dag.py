from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "email": ["brandan.pratt1@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False
}

with DAG(
    dag_id="dbt_transformation_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 5, 1),
    schedule="@daily",
    catchup=False,
    tags=["dbt", "snowflake", "analytics"]
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        export DBT_PROFILES_DIR=/opt/airflow/retail_dbt && \
        cd /opt/airflow/retail_dbt && \
        dbt run
        """
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        export DBT_PROFILES_DIR=/opt/airflow/retail_dbt && \
        cd /opt/airflow/retail_dbt && \
        dbt test
        """
    )

    dbt_run >> dbt_test