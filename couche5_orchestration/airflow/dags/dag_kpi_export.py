"""DAG Airflow - Export KPIs quotidien"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def export_kpis_to_hbase():
    """Exporte les KPIs vers HBase"""
    print("📊 Export des KPIs vers HBase...")


def generate_daily_report():
    """Génère le rapport quotidien"""
    print("📄 Génération du rapport quotidien...")


default_args = {
    'owner': 'ecostream',
    'start_date': datetime(2026, 10, 1)
}

dag = DAG(
    'dag_kpi_export',
    default_args=default_args,
    description='Export quotidien des KPIs',
    schedule_interval='@daily',
    catchup=False,
    tags=['ecostream', 'kpi']
)

t1 = PythonOperator(
    task_id='export_kpis',
    python_callable=export_kpis_to_hbase,
    dag=dag
)

t2 = PythonOperator(
    task_id='daily_report',
    python_callable=generate_daily_report,
    dag=dag
)

t1 >> t2