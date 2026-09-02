# Scoring rubric

Mechanical completeness is evidence, not a score. Recommendation is holistic:

`Strong hire / Hire / Mixed / No hire / Strong no hire`

## Time and format

- Live: they covered critique, work units, security, serving, and a gap list inside 90 minutes.
- Take-home: `SUBMISSION.md` is internally consistent, time-boxed, and discloses AI use.

A missing section with an explicit “I would do X next” is better than a wallpaper of service names.

## Critique quality

Look for a precise attack on generated Python, layout drift, unsplittable files, crawler-as-model, and non-atomic publish. Keeping medallion + layout-as-signal + Glue/Athena is positive.

## Work units and compute

Look for bounded retries, page/batch maps, a written rule ECS vs Glue Spark, and a plan for SQLite/Excel that is not OCR. Glue jobs as the Spark plane when a long-lived cluster is unjustified is a valid senior choice.

## AI boundary

Look for a **versioned extraction contract** (or equivalent), promotion to ECR, reuse via registry, stratified sampling, and mid-document fingerprint change → new contract or quarantine. Prompt logs without page dumps.

## Data and catalog

Look for grain, tenant_id, layout_version, lineage to object/page, explicit Glue DDL or Iceberg, crawlers as optional discovery only.

## Security

Look for SSO+MFA, distinct job roles, KMS per zone, Lake Formation or a real replacement, PII classification, quarantine in raw zone, safe telemetry.

## Serving

Look for gold as BI source of truth, PDF render as a job from tables, website not scanning S3 PDFs, Athena workgroup isolation.

## Operability and cost

Look for publish gate, reconciliation counts, poison policy, Textract/Bedrock/S3 quotas, and arithmetic with uncertainty — not laptop-linear fantasy.

## Negative signals

- `exec` / save-and-run LLM Python in prod with no promotion path
- One Fargate task reads 10k pages into memory
- Analysts on raw bucket
- Per-page KMS or per-page Bedrock with no quota math
- Glue crawler as the modeling strategy
- “We’ll put failures on a DLQ” with no accounting or access control
- Tableau reading bronze PDFs
- Claiming OCR+LLM eliminates residual PII risk

## Evidence record

```text
Candidate:
Evaluator:
Date:
Format: live / take-home

Strongest signal:

Largest concern:

Critique of naive design:

Compute routing:

AI boundary:

IAM / PII / SSO:

Publication / SLA / cost:

Overall recommendation:
Strong hire / Hire / Mixed / No hire / Strong no hire

Summary:
```
