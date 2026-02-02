# 🚀 Sales Data Lakehouse: GCS to BigQuery (Data Fusion)

This repository automates the ingestion of CSV sales data from **Google Cloud Storage (GCS)** into **BigQuery** using **Cloud Data Fusion**. This "No-Code" approach is ideal for complex visual transformations and rapid deployment.

## 🏗 Architecture

1. **Source:** Raw CSV files landed in `gs://sales-data-lake/input/`.
2. **Transformation:** **Wrangler** plugin used for schema parsing and data cleaning.
3. **Sink:** Final data appended to `sales_dataset.sales_data` in BigQuery.
4. **Execution:** On-demand or scheduled Batch Pipeline running on ephemeral Dataproc clusters.
## 🛠 Tech Stack

* **Storage:** Google Cloud Storage (`sales-data-lake`)
* **Orchestration:** Data Fusion
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

### 2. Create Data-Fusion Environment

Create Instance:

```
# Set Project ID
gcloud config set project [YOUR_PROJECT_ID]

# Enable APIs
gcloud services enable datafusion.googleapis.com storage.googleapis.com bigquery.googleapis.com

# Create Data Fusion Instance (Basic Edition)
gcloud beta data-fusion instances create sales-fusion-instance \
    --location=us-central1 \
    --edition=basic

gcloud beta data-fusion instances list --location=us-central1
```


<img width="1757" height="292" alt="image" src="https://github.com/user-attachments/assets/fa48e744-4e14-4e94-aad8-d5ee4cc3294d" />


### 2. IAM Configuration (Crucial)

Data Fusion needs permission to manage Dataproc clusters and write to BigQuery.

1. Go to **IAM & Admin > IAM** in the Console.
2. Locate the **Cloud Data Fusion API Service Agent** (usually `service-[PROJECT_NUMBER]@gcp-sa-datafusion.iam.gserviceaccount.com`).
3. Grant it the **Cloud Data Fusion API Service Agent** role if not present.
4. Ensure your **Compute Engine Default Service Account** has `roles/bigquery.dataEditor` and `roles/storage.objectViewer`.


<img width="1892" height="778" alt="image" src="https://github.com/user-attachments/assets/ccc187b6-e31d-49fe-9d47-4cb7e945efcd" />

Since your Cloud Data Fusion instance is now provisioning, you can prepare your **`gcp-serverless-ingestion`** repository. This README provides a professional, step-by-step guide for a "No-Code" data lake pattern using the **Wrangler** and **BigQuery Sink** plugins.

### 3. Build the Pipeline (Visual Studio)

Once the instance is `RUNNING`, click **View Instance** to open the Data Fusion UI.

<img width="1590" height="412" alt="image" src="https://github.com/user-attachments/assets/475f6ff3-595a-46df-a176-08218e92b178" />


#### **A. Source (GCS)**

* Drag the **GCS** source onto the canvas.
* **Properties:** * *Reference Name:* `Sales_Raw_CSV`
* *Path:* `gs://sales-data-lake/input/`
* *Format:* `csv`

<img width="1897" height="956" alt="image" src="https://github.com/user-attachments/assets/d1e5bf4a-7b0d-4acf-8fa1-d74d922949b0" />


#### **B. Transform (Wrangler)**

* Connect GCS to a **Wrangler** node.
* Open Wrangler and select your sample file.
* **Directives:** Apply "Parse as CSV", "Set Column Names", and "Change Type" (e.g., `amount` to `float`).



#### **C. Sink (BigQuery)**

* Connect Wrangler to the **BigQuery** sink.
* **Properties:**
* *Dataset:* `sales_dataset`
* *Table:* `sales_data`
* *Operation:* `Insert` (Append)



### 4. Deploy and Run

1. Click **Draft** to save.
2. Click **Deploy** in the top right.
3. Click **Run** to start the manual ingestion.

---

## 📂 Repository Structure

```text
.
├── pipeline/
│   └── sales_ingestion_v1.json  # Exported Data Fusion pipeline JSON
├── schemas/
│   └── sales_schema.json        # BigQuery table schema definition
└── README.md

```

## 🚨 Troubleshooting

* **Tenant Project Error:** If instance creation fails, run `gcloud beta services identity create --service=datafusion.googleapis.com`.
* **Dataproc Failures:** Check if your project has enough **Compute Engine CPU Quota** for the ephemeral workers.

---

### Next Step

Would you like me to generate the **BigQuery Schema JSON** and the **Wrangler Directive script** so you can include them in your repository's `/schemas` and `/pipeline` folders?

[How to load data from Cloud Storage to BigQuery using Data Fusion](https://www.youtube.com/watch?v=b_7NZpw9PVE)

This video provides a complete visual walkthrough of the Wrangler and BigQuery sink configuration, which is the most interactive part of the Data Fusion setup.
