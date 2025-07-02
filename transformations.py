from google.cloud import storage, bigquery
import pandas as pd

def transform_vehiculos(gcs_client, bq_client, bucket_name, project_id, dataset_id):
    # Lee el archivo CSV desde GCS (simulado localmente por ahora)
    bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.blob('data/vehiculos.csv')
    blob.download_to_filename('/tmp/vehiculos.csv')
    df = pd.read_csv('/tmp/vehiculos.csv')

    # Transforma los datos para Dim_Vehiculo
    dim_vehiculo_df = df[['modelo', 'marca', 'tipo', 'clase']].drop_duplicates().reset_index(drop=True)
    dim_vehiculo_df['id_vehiculo'] = range(1, len(dim_vehiculo_df) + 1)

    # Carga a BigQuery
    table_id = f"{project_id}.{dataset_id}.Dim_Vehiculo"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = bq_client.load_table_from_dataframe(dim_vehiculo_df, table_id, job_config=job_config)
    job.result()

def transform_canton(gcs_client, bq_client, bucket_name, project_id, dataset_id):
    # Lee el archivo CSV
    bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.blob('data/vehiculos.csv')
    blob.download_to_filename('/tmp/vehiculos.csv')
    df = pd.read_csv('/tmp/vehiculos.csv')

    # Transforma los datos para Dim_Canton
    dim_canton_df = df[['canton']].drop_duplicates().reset_index(drop=True)
    dim_canton_df['id_canton'] = range(1, len(dim_canton_df) + 1)

    # Carga a BigQuery
    table_id = f"{project_id}.{dataset_id}.Dim_Canton"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = bq_client.load_table_from_dataframe(dim_canton_df, table_id, job_config=job_config)
    job.result()

def transform_tiempo(bq_client, project_id, dataset_id):
    # Simula la generación de Dim_Tiempo (puedes usar 'fecha' del CSV)
    # Placeholder: Deberías extraer años, meses, etc., de 'fecha'
    pass

def transform_registros(gcs_client, bq_client, bucket_name, project_id, dataset_id):
    # Simula la generación de Fact_Registro_Vehiculos
    # Placeholder: Deberías unir Dim_Vehiculo, Dim_Canton, Dim_Tiempo y contar registros
    pass