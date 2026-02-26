
# 🎵 Sparkify Data Pipelines with Airflow

Welcome to the Sparkify Airflow Automation project! If you're looking at this, you're witnessing the transformation of raw, messy JSON data into a beautiful, queryable Star Schema in Amazon Redshift. We've automated the whole thing because, honestly, who has the time to run `COPY` commands manually in 2026?

---

## 🛠 Pre-requisites: The Setup

Before you flip the switch on the DAG, you need to set up your infrastructure. Think of this as preparing the stage before the band starts playing.

### 1. IAM: The Secret Handshake

You need an IAM user with `Programmatic access` and the `AmazonS3ReadOnlyAccess` policy.

* **Pro Tip**: Grab your **Access Key ID** and **Secret Access Key**. You'll need these to let Airflow talk to your S3 bucket.

### 2. Redshift: The Powerhouse

Whether you use a **Redshift Cluster** or **Serverless**, ensure it's "Publicly Accessible."

* Create a **Workgroup** and **Namespace** if using Serverless.
* **Security Group**: Make sure your inbound rules allow traffic on port `5439`.

### 3. S3: The Warehouse

Create a bucket (e.g., `han-udacity-project`) and upload the project data:

* `log-data/`
* `song-data/`
* `log_json_path.json`

> **Note**: Watch those hyphens! Redshift is picky about prefixes.

---

## 🔌 Connecting the Dots

Airflow needs to know where everything is. Go to the Airflow UI -> **Admin** -> **Connections**.

| Conn ID | Conn Type | Details |
| --- | --- | --- |
| `aws_credentials` | Amazon Web Services | Login: Access Key, Password: Secret Key |
| `redshift` | Postgres | Host: Your Endpoint, Schema: `dev`, Port: `5439` |

**The CLI Shortcut:** If you prefer the command line, use the `conn-uri` format. Just watch out for URL encoding on special characters like `:` or `/`.

---

## 🏗 The Blueprints: Creating Tables

Before the data flows, the tables must exist. Run the provided DDL in your Redshift Query Editor. We’ve beefed up the `VARCHAR` lengths for `artist_name` and `userAgent` because some data is just... extra.

---

## 🚀 The Operators: Our Heavy Lifters

This project features four custom-built operators that do the heavy lifting:

1. **StageToRedshift**: Moves JSON data from S3 to Redshift Staging tables using the `COPY` command. It supports JSON paths for that tricky log data.
2. **LoadFact**: Populates the `songplays` fact table. It's built for speed and is **Append-only**.
3. **LoadDimension**: Handles our four dimension tables. It features a `append_only` toggle—if set to `False`, it performs a **Truncate-Insert** to keep our data fresh and idempotent.
4. **DataQuality**: The guardian of our pipeline. It runs SQL test cases and raises a `ValueError` if the data doesn't meet our expectations.

---

## 🩺 Debugging & Lessons Learned

If the DAG turns red (and it might!), here’s the battle-tested checklist:

* **Check the Logs**: Airflow logs are your best friend. Look for `psycopg2.errors` for SQL issues.
* **VARCHAR Length**: If you see `String length exceeds DDL length`, go back to Redshift and increase your `VARCHAR(256)` to `512` or more.
* **S3 Prefixes**: Ensure your `s3_key` in the DAG matches your S3 folder name exactly.

---

## ✨ Final Thought

Once the DAG is all green, you’ve successfully automated a production-grade data pipeline. Don't forget to **delete your Redshift resources** when you're done to save your credits!

**Happy Automating!** 🚀
