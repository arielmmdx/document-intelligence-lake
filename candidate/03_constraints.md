# 03 — Constraints

Treat these as production rules unless you change them and say why.

## Orchestration (fixed)

- **Apache Airflow on Amazon MWAA** orchestrates the entire pipeline.
- **Do not use AWS Lambda** (or Step Functions as the primary orchestrator) to drive the DAG.
- Airflow tasks **call workers**: ECS Fargate (Python) and Glue Spark jobs (PySpark). Sensors/operators wait on S3, ECS, and Glue.
- A DAG run must be **idempotent** (same file + same contract version → same silver, or a clean skip).

## Platform

- AWS `eu-west-1`. DR required; active-active is not.
- Humans: IAM Identity Center (SSO) + **MFA**. No long-lived IAM users.
- Lake: S3, Glue Data Catalog, Athena, Lake Formation (or a named replacement).
- Python extractors: images in **ECR**, run on **ECS Fargate**.
- Large tabular / wide transforms: **Glue PySpark** (EMR only if you justify it).
- Document AI: Textract and/or Bedrock. Fit IAM, VPC, and EU residency.

## Security

- Raw files contain PII. Classify before silver is widely readable.
- Logs must not contain OCR lines, full-page prompts, or identifiers.
- KMS CMKs per zone, not only SSE-S3.
- No public S3. VPC endpoints for S3, ECR, Glue, Athena, MWAA, Textract/Bedrock.
- Scan ECR images. Task roles ≠ deploy role.

## Engineering

- Work units are **bounded and retryable**. Do not load a 10,000-page PDF or a 40 GB SQLite file as one in-memory blob.
- Publish silver/gold with a **dataset-level** commit (Iceberg snapshot or equivalent). Not object-by-object into `current/`.
- Unknown layout / poison page → **quarantine** in the raw zone, with counts. Not a silent drop.
- `tenant_id` on every object and table. No cross-tenant list or query.

## Out of scope

Terraform resource names, OCR research papers, building the website UI, fake-precise price quotes.

You still need a capacity sketch: Airflow parallelism, ECS vs Glue, Textract quotas, p95 (800 pages) vs p99 (10,000 pages).
