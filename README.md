# 🚀 Sales Data Lakehouse: GCS to BigQuery Pipeline

This project implements an automated ETL pipeline using **Cloud Composer (Airflow)** to ingest sales data from **Google Cloud Storage (GCS)** into **BigQuery**. It includes data validation, custom monitoring, and automated alerting.

## 🛠 Tech Stack

* **Storage:** Google Cloud Storage (`sales-data-lake`)
* **Orchestration:** Cloud Composer 2 (Airflow 2.6.3)
* **Data Warehouse:** BigQuery
* **Monitoring:** Cloud Logging & Cloud Monitoring Alerts

---

## 📖 Step-by-Step Setup Guide

### 1. Infrastructure Initialization

First, set up your bucket and dataset. Note that the bucket is configured as a **Multi-region (us)** for high availability.

```bash
# Set variables
export PROJECT_ID=$(gcloud config get-value project)

# Create the Multi-region bucket
gsutil mb -l us gs://sales-data-lake/

echo "order_id,product,quantity,amount,order_date
ORD001,Laptop,2,2400.50,2026-01-23
ORD002,Mouse,5,125.00,2026-01-23
ORD003,Keyboard,3,210.75,2026-01-23" > sales_20260123.csv

gsutil cp sales_20260123.csv gs://sales-data-lake/input/

# Create BigQuery Dataset
bq mk --location=us sales_dataset

```

<img width="1047" height="153" alt="image" src="https://github.com/user-attachments/assets/f9cca333-a018-4cd0-9078-aa97bb6b771b" />

### 2. Create Cloud Composer Environment
```
gcloud composer environments create composer-gcs-bq \
  --location us-central1 \
  --image-version composer-2.5.0-airflow-2.6.3 \
  --environment-size small
```


### 2-A. IAM Configuration

The Cloud Composer Service Account requires permissions to interact with GCS and BigQuery.

```bash
# Get the SA from your Composer environment
COMPOSER_SA=$(gcloud composer environments describe <YOUR_ENV> --location <LOCATION> --format="value(config.nodeConfig.serviceAccount)")

# Assign Roles
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$COMPOSER_SA" --role="roles/storage.objectViewer"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$COMPOSER_SA" --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$COMPOSER_SA" --role="roles/bigquery.jobUser"

```

### 3. Deploy the DAG

Upload the Airflow DAG to your Composer's dedicated GCS folder.

```bash
gcloud composer environments storage dags import \
  --environment <ENV_NAME> \
  --location <LOCATION> \
  --source dags/gcs_to_bq_pipeline.py

```

### 4. Data Ingestion (Simulated)

Drop a file into the lake to trigger the process (or wait for the daily schedule).

```bash
# Upload sample data
gsutil cp sample_data/sales_20260124.csv gs://sales-data-lake/input/

```

### 5. Monitoring & Verification

* **Check Data:** Run `SELECT * FROM sales_dataset.sales_data` in the BQ Console.
* **Logs:** View Airflow logs via the Composer UI for task-level debugging.
* **Metrics:** Custom metrics are sent to `custom.googleapis.com/gcs_to_bq/pipeline_success`.

---

## 🚨 Alerting Logic

The pipeline is integrated with Cloud Monitoring. Alerts are triggered if:

1. The DAG fails entirely.
2. The validation step finds **0 rows** (indicating a source data issue).
3. An SLA breach occurs (task duration exceeds limits).

---

## 🔒 Security

* **Service Accounts:** Uses Least Privilege principle.
* **Storage:** Public access is disabled on `sales-data-lake`.

---

### Next Step

Would you like me to create the `.gitignore` file and a sample `cloud-setup.sh` script to automate all the CLI commands listed above?
