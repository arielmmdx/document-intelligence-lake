# 02 — Expected interview answers

Phrases need not match. Use while they talk.

## Airflow

**Strong:** DAG of sensors + ECS + Glue operators; nothing heavy on the MWAA workers; mapped tasks for page batches; pools; idempotent run key; branch to quarantine; task-level retries.

**Weak:** “Lambda triggers Lambda.” Airflow DAG that `pandas.read_excel` of 40 GB on the scheduler. One task “process_file” for every format.

## Python vs PySpark

**Strong:** Thresholds; Excel → Glue; SQLite → Python paging; PDF pages → mapped workers; gold joins in Spark with an explicit partition key.

**Weak:** “Spark for everything” or “Fargate for the 50M-row workbook.”

## Distributed

**Strong:** 50-page batches + overlap; reduce by `document_id`; skew via pools; Iceberg snapshot as commit; replay = new DAG run with same key.

**Weak:** One ECS task, 10k pages in RAM. Unlimited parallelism.

## Naive critique

**Strong:** No `exec` of LLM Python; contract + ECR; stratified sample; crawler is not the model; dataset publish.

**Weak:** “We will sandbox eval() in prod” with no promotion path.

## Medallion / serving / security

**Strong:** Grain stated; `layout_version`; analysts on gold; MWAA role ≠ analyst; no OCR in CloudWatch.

**Weak:** Tableau on landing. One IAM role for all tasks.
