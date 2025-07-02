# Pipeline ETL para Datos de Vehículos del SRI

## Instrucciones para Usar este Proyecto

Este repositorio contiene un pipeline ETL para procesar datos de registro de vehículos nuevos (2024) del Servicio de Rentas Internas (SRI) de Ecuador usando Apache Airflow y Google BigQuery. Sigue estos pasos para ejecutarlo:

1. **Clona el Repositorio**:
   ```bash
   git clone https://github.com/Henred/etl-airflow-vehiculos.git
   cd etl-airflow-vehiculos

2. Instala Dependencias:
Asegúrate de tener Docker instalado (descarga desde docker.com).
Verifica con: docker --version.

3. Inicia el Contenedor Airflow:
docker run -d -p 8080:8080 \
-v $(pwd)/dataset:/opt/airflow/dags \
-v $(pwd)/dataset:/opt/airflow/data \
-v $(pwd)/dataset:/opt/airflow/scripts \
-v $(pwd)/logs:/opt/airflow/logs \
-v $(pwd)/plugins:/opt/airflow/plugins \
--name airflow apache/airflow:2.7.3

4. Inicializa Airflow:
Si es la primera vez, inicializa la base de datos:

docker exec -it airflow bash
airflow db init
exit

5. Instala Librerías Necesarias:
docker exec -it airflow pip install google-cloud-storage google-cloud-bigquery pandas openpyxl

6. Configura la Clave de Servicio de Google Cloud:
Copia tu archivo JSON de la cuenta de servicio (por ejemplo, vehiculos-etl-2025-123456.json) al contenedor:
docker cp ~/gcp_credentials/vehiculos-etl-2025-123456.json airflow:/opt/airflow/gcp_credentials.json
Asegúrate de que el proyecto vehiculos-etl-2025, el bucket vehiculos-etl-bucket, y el dataset vehiculos_dw estén configurados en Google Cloud.

7. Accede a Airflow:
Abre http://localhost:8080 en tu navegador (usuario: admin, contraseña: admin).
Activa el DAG etl_vehiculos_dag y haz clic en "Trigger DAG" para ejecutarlo.

8. Verifica la Ejecución:
Revisa los logs si hay errores:
docker logs airflow

Los resultados se cargarán en las tablas Dim_Vehiculo, Dim_Canton, Dim_Tiempo, y Fact_Registro_Vehiculos en BigQuery.
