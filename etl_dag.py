from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage, bigquery
import pandas as pd

# Configuración
project_id = 'vehiculos-etl-2025'
bucket_name = 'vehiculos-etl-bucket'
dataset_id = 'vehiculos_dw'
gcs_client = storage.Client.from_service_account_json('/opt/airflow/gcp_credentials.json')
bq_client = bigquery.Client.from_service_account_json('/opt/airflow/gcp_credentials.json')

default_args = {
    'owner': 'henry',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='etl_vehiculos_dag',
    default_args=default_args,
    description='ETL for SRI vehicle data (2024)',
    schedule_interval=None,
    start_date=datetime(2025, 3, 24),
    catchup=False,
) as dag:
    inicio = DummyOperator(task_id='inicio')
    fin = DummyOperator(task_id='fin')

    # Tareas (se conectarán a transformations.py)
    cargar_dim_vehiculo = PythonOperator(
        task_id='cargar_dim_vehiculo',
        python_callable=lambda: None,  # Placeholder, se reemplazará con transform_vehiculos
        op_kwargs={'gcs_client': gcs_client, 'bq_client': bq_client, 'bucket_name': bucket_name, 'project_id': project_id, 'dataset_id': dataset_id}
    )

    cargar_dim_canton = PythonOperator(
        task_id='cargar_dim_canton',
        python_callable=lambda: None,  # Placeholder, se reemplazará con transform_canton
        op_kwargs={'gcs_client': gcs_client, 'bq_client': bq_client, 'bucket_name': bucket_name, 'project_id': project_id, 'dataset_id': dataset_id}
    )

    cargar_dim_tiempo = PythonOperator(
        task_id='cargar_dim_tiempo',
        python_callable=lambda: None,  # Placeholder, se reemplazará con transform_tiempo
        op_kwargs={'bq_client': bq_client, 'project_id': project_id, 'dataset_id': dataset_id}
    )

    cargar_fact_registros = PythonOperator(
        task_id='cargar_fact_registros',
        python_callable=lambda: None,  # Placeholder, se reemplazará con transform_registros
        op_kwargs={'gcs_client': gcs_client, 'bq_client': bq_client, 'bucket_name': bucket_name, 'project_id': project_id, 'dataset_id': dataset_id}
    )

    inicio >> [cargar_dim_vehiculo, cargar_dim_canton, cargar_dim_tiempo] >> cargar_fact_registros >> fin