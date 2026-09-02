# 02 — Expected interview answers

Phrases need not match. Use while they talk.

## Airflow

**Strong:** DAG of sensors + ECS + Glue operators; nothing heavy on the Airflow **EC2**; LLM only on a page/header sample; mapped tasks for page batches; pools; idempotent run key; branch to quarantine; task-level retries.

**Weak:** “Lambda triggers Lambda.” Pandas of 40 GB on the Airflow EC2. Bedrock on all 10,000 pages. One task “process_file” for every format.

## Python vs PySpark

**Strong:** Thresholds; Excel → Glue **after** a header/sheet contract from a sample; SQLite → Python paging; PDF pages → mapped workers; gold joins in Spark with an explicit partition key.

**Weak:** “Spark for everything” or “Fargate for the 50M-row workbook.” **Also weak:** sending every Excel row to Bedrock, or skipping layout because “Excel already has columns.”

## Distributed

**Strong:** 50-page batches + overlap; reduce by `document_id`; skew via pools; Iceberg snapshot as commit; replay = new DAG run with same key.

**Weak:** One ECS task, 10k pages in RAM. Unlimited parallelism.

## Naive critique / layout

**Strong:** No `exec` of LLM Python; contract + ECR; stratified sample; **Excel/Word also get T4a on a sample**; crawler is not the model; dataset publish.

**Weak:** “We will sandbox eval() in prod” with no promotion path. “Large Excel skips AI so we just Spark it” with no header/contract story.

## Medallion / serving / security

**Strong:** Grain stated; `layout_version`; analysts on gold; Airflow EC2 role ≠ analyst; no OCR in CloudWatch.

**Weak:** Tableau on landing. One IAM role for all tasks.
