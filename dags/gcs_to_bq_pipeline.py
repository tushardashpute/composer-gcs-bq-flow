from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from google.cloud import monitoring_v3
import time

# Variables - In prod, use Airflow Variables
PROJECT_ID = "YOUR_PROJECT_ID_HERE" 
DATASET = "sales_dataset"
TABLE = "sales_data"
BUCKET = f"sales-data-bucket-{PROJECT_ID}"

def validate_rows_func():
    hook = BigQueryHook()
    sql = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET}.{TABLE}`"
    result = hook.get_first(sql)
    if result[0] == 0:
        raise ValueError("Data validation failed: Table is empty!")
    print(f"Validation passed: {result[0]} rows found.")

with DAG(
    dag_id="gcs_to_bq_prod_pipeline",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # 1. Load CSV from GCS to BQ
    load_csv = GCSToBigQueryOperator(
        task_id="load_gcs_to_bq",
        bucket=BUCKET,
        source_objects=["input/sales_*.csv"],
        destination_project_dataset_table=f"{PROJECT_ID}.{DATASET}.{TABLE}",
        source_format="CSV",
        skip_leading_rows=1,
        write_disposition="WRITE_APPEND", # Append for daily batches
        autodetect=True,
    )

    # 2. Python Validation
    validate_data = PythonOperator(
        task_id="validate_data",
        python_callable=validate_rows_func,
    )

    # 3. Success Audit (Example of a simple SQL transformation)
    audit_log = BigQueryInsertJobOperator(
        task_id="audit_log_update",
        configuration={
            "query": {
                "query": f"SELECT CURRENT_TIMESTAMP() as load_time, count(*) as total_rows FROM `{PROJECT_ID}.{DATASET}.{TABLE}`",
                "useLegacySql": False,
            }
        },
    )

    load_csv >> validate_data >> audit_log
