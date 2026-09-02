# 04 — Scoring rubric

Holistic: `Strong hire / Hire / Mixed / No hire / Strong no hire`

## Must show (senior DE)

- **Airflow** on **EC2** as orchestrator; ECR/ECS and Glue as workers; no Lambda-driven pipeline.
- **LLM layout on a sample** for PDF, Excel, and Word. Never 10k pages into the model.
- **Python** on ECS for bounded format work; **PySpark** on Glue when rows/files are large and splittable.
- **Distributed units** for 10k-page PDFs (map/reduce, overlap, pools, retries).
- Critique of generated Python and first-20-pages.
- Medallion + atomic publish + analysts not on landing.

A missing section with “I would do X next” beats a wallpaper of service names.

## Negative

- Lambda (or Step Functions) as the real orchestrator despite the constraint
- `exec` of LLM Python in the data plane
- One Fargate task holds 10k pages or 50M Excel rows
- PySpark on SQLite as a blob; OCR on `.xlsx`
- Heavy work on the Airflow EC2 (LLM, OCR, Spark)
- Bedrock/LLM on every page of a 10k-page PDF
- Analysts on the landing bucket
- Crawler as the model; `current/` copy as publish

## Record

```text
Candidate:
Evaluator:
Date:
Format: live / take-home

Airflow DAG:
Python vs PySpark:
Distributed units:
Naive critique:
Medallion / publish / IAM:

Overall: Strong hire / Hire / Mixed / No hire / Strong no hire
Summary:
```
