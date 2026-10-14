"""DAG Airflow - Traitement Spark toutes les 6h"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def run_spark_batch():
    """Lance le traitement Spark batch"""
    print("⚡ Traitement Spark en cours...")


default_args = {
    'owner': 'ecostream',
    'start_date': datetime(2026, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}

dag = DAG(
    'dag_spark_processing',
    default_args=default_args,
    description='Traitement batch Spark des KPIs',
    schedule_interval='0 */6 * * *',
    catchup=False,
    tags=['ecostream', 'spark']
)

task = PythonOperator(
    task_id='spark_kpi_computation',
    python_callable=run_spark_batch,
    dag=dag
)