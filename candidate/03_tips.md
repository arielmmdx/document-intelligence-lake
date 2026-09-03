# 03 — Tips: rules to respect when you improve the design

Treat these as production rules unless you change them and say why.

- **Airflow on EC2** starts the work. It does not parse PDFs or run Spark on 50M rows.
- **No Lambda** (and not Step Functions) as the main orchestrator.
- Workers: **ECS** (Python images from **ECR**) and **Glue PySpark**.
- **LLM** (any vendor) and/or **OCR** on a **sample** for PDF, Excel, and Word. Never send 10,000 pages to the LLM.
- Same file + same recipe version → same silver (or a clean skip). **Idempotent.**
- AWS `eu-west-1`. Humans: SSO + **MFA**. Lake: S3, Glue Catalog, Athena, Lake Formation (or name a replacement).
- PII in raw files. No OCR text in logs. KMS per zone. No public S3. Scan ECR images. Task role ≠ deploy role.
- Bounded work units. Quarantine unknown layouts in the **raw** zone, with counts.
- `tenant_id` on every object and table.

Out of scope: Terraform names, OCR papers, building the website UI. You still owe a rough capacity/cost sketch (sample vs full OCR, p95 vs p99).
