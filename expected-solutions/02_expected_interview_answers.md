# 02 — Expected interview answers

Phrases need not match. Use while they talk.

## Airflow

**Strong:** LLM only on a sample; recipe JSON; Python/Spark writes silver; docstrings and helpers described; Airflow EC2 does not parse PDFs.

**Weak:** “Send the 10k-page PDF to the LLM.” “Bedrock writes Parquet.” DAG with no docstrings and a 400-line task.

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
