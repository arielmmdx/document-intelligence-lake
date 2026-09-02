# Submission (take-home only)

Calendar time spent (stop at 6 hours):

## Critique of the naive design

What you keep, what you reject, and why. Cover generated Python, the “first 20 pages” heuristic, and single-compute assumptions.

## Target architecture

Components, data zones, and control flow. You may attach mermaid. Name AWS services only when they change a failure mode.

## Work units and compute routing

How a 40-page PDF, a 10,000-page PDF, a 40 GB Excel, and a SQLite snapshot are partitioned. ECS vs Glue/Spark decision rule.

## Layout contract and AI boundary

The artifact produced by layout intelligence, approval, versioning, and reuse. Prompt/data handling.

## Data model (bronze / silver / gold)

Grain, keys, tenant id, layout version, lineage back to page/object. Catalog strategy.

## Serving

Athena, BI, regenerated PDF, website. Consistency model: which store is source of truth.

## Security

IAM roles, SSO/MFA, Lake Formation or replacement, KMS, network, PII, logs, ECR.

## Reliability and publication

Idempotency, quarantine, dataset-level publish, replay.

## SLA, capacity, cost

Assumptions, arithmetic, quotas (Textract/Bedrock/S3/Glue), uncertainty.

## v1 vs later

Deferred work and residual risk.

## AI tool disclosure

Tools used and how you checked vendor claims.
