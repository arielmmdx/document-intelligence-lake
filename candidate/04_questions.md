# 04 — Questions

Use as the live spine or as take-home prompts. Depth on **Airflow, Python, PySpark, and distributed work** matters more than naming extra AWS products.

## 1. Airflow DAG

- Sketch the DAG: task names, sensors, retries, pools, `catchup`, and what a **mapped** task is for.
- How does a DAG run id relate to `tenant_id` + file checksum so retries are idempotent?
- Where do you **branch** (PDF vs Excel vs SQLite vs quarantine)? `BranchPythonOperator` or separate DAGs — why?
- Airflow is the orchestrator, not the engine: what must **not** run inside a worker process on the MWAA node?

## 2. Python vs PySpark

- Decision rule: ECS Python vs Glue PySpark. Give thresholds (rows, bytes, pages), not a brand preference.
- 50M-row Excel: how do you parse headers/merged cells in Spark without a driver OOM?
- SQLite: why might Spark be the wrong default? How do you page in Python?
- What belongs in a **shared Python library** (in ECR) vs a **Spark job script**?

## 3. Distributed compute

- How do you turn a 10,000-page PDF into work units (size, overlap for tables that span pages, reduce/merge)?
- Skew: one tenant drops 2,000 huge PDFs. What happens to Airflow pools and Glue DPUs?
- Shuffle: when gold joins PDF-extracted lines to Excel lines, what do you partition on?
- Checkpoint / replay: Airflow task retry vs Spark job bookmark vs rewriting an Iceberg snapshot.

## 4. Naive design critique

- Why is “LLM writes Python, then we run it” a production incident?
- Why do the first 20 pages fail as a layout rule?
- What should AI emit instead (contract vs code), and who promotes it?

## 5. Medallion and catalog

- Grain of bronze vs silver vs gold. `layout_version` and lineage to `s3://…` / page range.
- Glue crawlers vs explicit tables / Iceberg. Why?
- When is silver “safe to read”?

## 6. Serving and security (shorter)

- Tableau on Athena: types, IAM, partitions. Source of truth for a reprinted PDF?
- Roles: MWAA execution role vs ECS task role vs Glue job role vs analyst SSO. Who can read landing?
- PII in logs. KMS at job grain vs per page.

## 7. What you would not build in v1

Name three deferrals and the risk of each.
