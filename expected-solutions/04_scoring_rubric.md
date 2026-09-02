# 04 — Scoring rubric

Holistic: `Strong hire / Hire / Mixed / No hire / Strong no hire`

## Must show (senior DE)

- **Airflow** as orchestrator; workers elsewhere; no Lambda-driven pipeline.
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
- Heavy work on the MWAA worker
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
