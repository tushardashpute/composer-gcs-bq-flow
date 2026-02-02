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

<img width="1887" height="787" alt="image" src="https://github.com/user-attachments/assets/b7fefdb8-1450-460d-8459-7cd9955d3ffa" />


#### **C. Sink (BigQuery)**

* Connect Wrangler to the **BigQuery** sink.
* **Properties:**
* *Dataset:* `sales_dataset`
* *Table:* `sales_data`
* *Operation:* `Insert` (Append)


<img width="1912" height="907" alt="image" src="https://github.com/user-attachments/assets/4e96be49-18ec-4f88-be58-8c385d37325c" />


<img width="1903" height="902" alt="image" src="https://github.com/user-attachments/assets/76513e25-6a72-40f1-ad0f-cb8513e03ae3" />


### 4. Deploy and Run

1. Click **Draft** to save.
2. Click **Deploy** in the top right.
3. Click **Run** to start the manual ingestion.

---

<img width="1913" height="672" alt="image" src="https://github.com/user-attachments/assets/c31f3507-728b-4268-8c28-9d08cc9d076e" />

<img width="1915" height="645" alt="image" src="https://github.com/user-attachments/assets/1fc495d1-8515-42d7-afae-e5f232409197" />

<img width="1907" height="723" alt="image" src="https://github.com/user-attachments/assets/77ced8f9-20d7-4ada-98dd-1cda78f570fc" />

<img width="1911" height="798" alt="image" src="https://github.com/user-attachments/assets/1febd31e-c55b-4f93-96b6-2f864af4f995" />

<img width="1900" height="783" alt="image" src="https://github.com/user-attachments/assets/589102b0-32bf-4538-8ba0-a18897d97e95" />

<img width="1917" height="808" alt="image" src="https://github.com/user-attachments/assets/b33db49f-7517-4c83-9f6f-980f40206895" />

<img width="1911" height="992" alt="image" src="https://github.com/user-attachments/assets/5b1ca38a-d330-4ea4-85ef-bd630b70c295" />

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

To avoid ongoing costs for the Data Fusion instance (which can be expensive even when idle) and clean up your data lake, follow these steps in order.

### 1. Delete the Data Fusion Instance

This is the most important step to stop billing.

```bash
gcloud beta data-fusion instances delete sales-fusion-instance \
    --location=us-central1 \
    --project=psychic-ethos-484710-m3 \
    --async

```

*Note: Using `--async` returns you to the prompt immediately while the deletion happens in the background. It takes about 15-20 minutes to fully remove.*

---

### 2. Clean Up Storage & Data

Next, remove the raw data bucket and the BigQuery dataset you created.

* **Remove the GCS Bucket:**
```bash
# This deletes the bucket and all files inside (input/, temp/, etc.)
gcloud storage rm --recursive gs://sales-data-lake

```


* **Remove the BigQuery Dataset:**
```bash
# This deletes the dataset and the sales_data table
bq rm -r -f -d psychic-ethos-484710-m3:sales_dataset

```

---

#### **Cleanup**

To prevent incurring additional charges to your Google Cloud account, delete the resources used in this project:

1. **Delete Data Fusion:** `gcloud beta data-fusion instances delete sales-fusion-instance --location=us-central1`
2. **Delete GCS Bucket:** `gcloud storage rm --recursive gs://sales-data-lake`
3. **Delete BigQuery Dataset:** `bq rm -r -f sales_dataset`

---

---

### 3. Revert IAM Permissions (Optional)

If you want to return your project to its original security state, remove the policy bindings we added.

```bash
# Remove Service Account User role
gcloud iam service-accounts remove-iam-policy-binding \
    212614848326-compute@developer.gserviceaccount.com \
    --member="serviceAccount:service-212614848326@gcp-sa-datafusion.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Remove Worker roles
gcloud projects remove-iam-policy-binding psychic-ethos-484710-m3 \
    --member="serviceAccount:212614848326-compute@developer.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects remove-iam-policy-binding psychic-ethos-484710-m3 \
    --member="serviceAccount:212614848326-compute@developer.gserviceaccount.com" \
    --role="roles/dataproc.worker"

```


