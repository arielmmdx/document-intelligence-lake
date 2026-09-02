# Questions

Use these as the live interview spine or as take-home writing prompts. You do not need equal depth on every item. Prioritize risk.

## 1. Problem and SLA

- What is the unit of business completeness: a file, a page, a batch, a customer day?
- Propose an SLA for p95 (800 pages) and a separate posture for p99 (10,000 pages). What is allowed to be late?
- How do you tell a consumer that silver is **safe to read** vs still landing?

## 2. Ingestion and bronze

- What lands in S3 first, and what metadata do you persist before OCR?
- How do you make ingest idempotent if the same file is uploaded twice?
- Virus scanning, checksums, Object Lock / legal hold: where do they sit?

## 3. Formats (do not collapse them)

- PDF scanned vs digital vs mixed: how do you decide to OCR?
- Excel: header rows, merged cells, multiple sheets, huge workbooks — pandas, Spark, or Glue?
- Word vs PDF conversion: when is conversion a lie?
- SQLite: is one database one work unit? How do you preserve FKs and detect corruption?
- Text: encoding, chunk overlap, entity extraction vs regex.

## 4. Layout intelligence (the AI step)

- Why is “first 20 pages → generate Python” dangerous in production?
- What artifact should AI emit instead of (or before) code? Who approves it?
- How do you detect that page 4,512 switched to a second form?
- How is a layout version reused across documents and tenants (or not)?
- Where do prompts, page images, and model outputs live, and who can read them?

## 5. Extraction runtime

- Closed interpreter of a JSON/YAML contract vs generated Python in ECR: tradeoffs.
- If you still generate Python, what sandbox, CI, IAM, and promotion path exist?
- How do you parallelize a 10,000-page PDF without breaking tables that span pages?
- When do you move from ECS Fargate Python to Glue Spark? Give a decision rule, not a brand preference.

## 6. Silver, gold, catalog

- What is a silver row/grain? Page? Form instance? Line item?
- How do you model slowly changing layouts (same form, new checkbox in 2026)?
- Glue crawlers vs explicit table DDL / Iceberg? Why?
- What belongs in gold vs a BI semantic layer?

## 7. Serving

- Athena connector for Tableau/Power BI: what breaks (types, partitions, IAM, spill)?
- Regenerated PDF: is that a batch render job or an API? What is the source of truth?
- Website: query Athena live vs served aggregates / indexed store? Latency and cost.

## 8. Security and identity

- Draw IAM roles for: ingest, classifier, layout/AI, ECS extractor, Glue job, Athena analyst, Tableau, break-glass.
- SSO + MFA: how do humans get to data vs how jobs get to data?
- PII: column-level in Lake Formation, tokenization, or separate PII vault? Residual risk?
- KMS: one CMK or per zone / per tenant? Quota if you call KMS per page.

## 9. Reliability and operations

- Retry, lease, checkpoint, poison page, DLQ, reconciliation counts.
- Independent verification vs trusting the extractor.
- Observability without logging OCR text.
- Cost model for 2,000 docs/day and for a 10k-page incident.

## 10. What you would not build in v1

- Name three capabilities you defer and the risk of deferring them.
