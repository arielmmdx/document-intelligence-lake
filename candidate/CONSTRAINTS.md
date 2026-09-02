# Constraints

Treat these as production constraints unless you explicitly change them and say why.

## Platform

- Primary cloud: **AWS**, region `eu-west-1` (customers in EU and UK). A DR story is required; active-active is not.
- Identity: **IAM Identity Center (SSO)** with **MFA** required. No long-lived IAM users for humans.
- Data lake storage: **S3**. Query: **Athena**. Catalog: **Glue Data Catalog**. Fine-grained access: **Lake Formation** (you may argue against it, but then replace it).
- Python extractors and layout services run as **container images in ECR**, executed on **ECS (Fargate preferred)** unless you justify EC2 or EKS.
- Heavy tabular / large-file Spark: **AWS Glue jobs** (Spark) or EMR. You choose and defend. Do not run 50M-row Excel on a single Fargate task by default.
- Orchestration: you choose (Step Functions, Airflow on MWAA, Glue workflows). Defend failure and map-reduce of pages.
- LLM / document AI: Bedrock, Textract, or a combination. You may propose another vendor but must fit IAM, VPC, and data-residency.

## Security and privacy

- Raw documents contain **PII** (names, addresses, government ids, health-adjacent notes). Classify before silver is widely readable.
- Logs, metrics, and traces must not contain raw OCR lines, prompts with full pages, or mappings of identifiers.
- Encryption: KMS CMKs, not only SSE-S3. Envelope encryption / data-key reuse must be explicit if you mention KMS at field granularity.
- Network: no public S3; VPC endpoints for S3, ECR, Glue, Athena, Bedrock/Textract as applicable.
- Image supply chain: scan ECR images; no secrets in images; task roles not the same as the pipeline deployer role.

## Engineering

- Work units must be **bounded and retryable**. A worker must not load a 10,000-page PDF or a 40 GB SQLite file into memory as one blob if you can avoid it.
- Publication of a silver/gold dataset must be **atomic at dataset level** (manifest, Iceberg snapshot, or equivalent). Copying files into `s3://.../silver/current/` one by one is not enough.
- Unknown layout or OCR garbage goes to **quarantine** in the raw security zone, with accounting. It is not dropped and not published.
- Multi-tenant: customer id on every object and every table. Lake Formation or equivalent row/column filters. Analyst of customer A cannot list customer B prefixes.

## Out of scope for the write-up

- Exact Terraform resource names
- Pixel-perfect OCR accuracy research
- Building the website frontend
- Real cost quotes beyond order-of-magnitude with dated assumptions

You still need a capacity model: workers, page batches, Textract/Bedrock quotas, S3 request rates, Glue DPU hours, and a p95 SLA for a 800-page PDF vs a 10,000-page PDF.
