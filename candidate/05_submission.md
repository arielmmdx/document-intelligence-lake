# 05 — Submission (take-home only)

Calendar time (stop at 6 hours):

## 1. Critique of the naive design

Generated Python, first-20-pages, single process, crawler-as-model.

## 2. Airflow DAG

Task graph, sensors, retries, mapped tasks, idempotency keys, what runs on MWAA vs ECS vs Glue.

## 3. Python vs PySpark vs distributed units

40-page PDF, 10,000-page PDF, 40 GB Excel, SQLite snapshot. Decision rule and work-unit sizes.

## 4. Layout / AI boundary

Artifact, approval, versioning. No `exec` of model code in the data plane unless you describe CI → ECR digest.

## 5. Bronze / silver / gold

Grain, keys, tenant, publish gate, catalog.

## 6. Serving and security

Athena / BI / PDF / website. SSO+MFA, job roles, PII, KMS.

## 7. SLA and cost (order of magnitude)

p95 vs p99, Textract/Glue/Airflow parallelism, uncertainty.

## 8. v1 vs later, and AI disclosure
