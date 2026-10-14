"""DAG Airflow - Ingestion batch horaire"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def check_new_files():
    """Vérifie les nouveaux fichiers CSV"""
    print("🔍 Vérification des nouveaux fichiers CSV...")
    return True


def ingest_to_kafka():
    """Envoie les fichiers vers Kafka"""
    print("📤 Envoi vers Kafka...")


default_args = {
    'owner': 'ecostream',
    'depends_on_past': False,
    'start_date': datetime(2026, 10, 1),
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'dag_batch_ingestion',
    default_args=default_args,
    description='Ingestion horaire des fichiers CSV',
    schedule_interval='@hourly',
    catchup=False,
    tags=['ecostream', 'ingestion']
)

t1 = PythonOperator(
    task_id='check_files',
    python_callable=check_new_files,
    dag=dag
)

t2 = PythonOperator(
    task_id='ingest_kafka',
    python_callable=ingest_to_kafka,
    dag=dag
)

t1 >> t2