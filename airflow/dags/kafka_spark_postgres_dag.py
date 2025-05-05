from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='kafka_spark_postgres_pipeline',
    default_args=default_args,
    description='Kafka -> Spark -> Postgres ETL',
    schedule_interval='@hourly',
    catchup=False,
    tags=['etl', 'spark', 'kafka'],
) as dag:

    run_spark_job = BashOperator(
        task_id='run_spark_job',
        bash_command='spark-submit /opt/bitnami/spark/my_spark_job.py',
    )

    run_spark_job
