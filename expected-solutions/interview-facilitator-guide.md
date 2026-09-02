# Interview facilitator guide (75–90 min)

Do not show `expected-architecture.md` or `diagrams/expected-architecture.drawio` until the last 5 minutes, and only if you want a teaching debrief. The candidate should redraw, not reverse-engineer the expected solution.

## Setup (before)

- Send `candidate/` 24 hours ahead for live interviews (read-only), or nothing if you want cold design (harder, more noise).
- Recommended: send scenario + naive architecture only; keep QUESTIONS.md as your spine.
- Whiteboard, mermaid.live, or the blank page in `architecture.drawio`.

## 0:00–0:08 Alignment

Ask them to restate the business outcome in one minute. Listen for: batch completeness, PII, tenant isolation, more than one consumer (SQL, BI, PDF, web).

If they jump to Kafka or Databricks, pull back: “AWS is the constraint unless you justify a swap.”

## 0:08–0:20 Critique of the naive pipeline

Force a position on:

1. Generated Python as the extractor
2. First-20-pages heuristic
3. One process for 10,000 pages
4. One path for PDF and Excel and SQLite

A senior should reject unbounded `exec` in the data plane. Accept “LLM drafts a contract, human or CI promotes a trusted image.”

## 0:20–0:40 Architecture and work units

Ask them to draw landing → bronze → extract → silver → gold → serve.

Probe:

- Idempotent ingest (checksum + tenant + logical doc id)
- Page batches vs whole file
- Table rows that span pages
- Excel → Spark/Glue vs PDF → ECS
- Dataset publish (Iceberg/manifest), not prefix overwrite

## 0:40–0:60 Security and PII

Roles on the board: ingest, layout, extract, glue, analyst, break-glass.

SSO + MFA for humans. Task roles for jobs. Separate KMS. No OCR in CloudWatch.

If they put analysts on the landing bucket, that is a strong negative unless they immediately correct.

## 0:60–0:75 Serving, SLA, cost

Athena + Lake Formation. Tableau as a consumer of gold, not of raw PDF.

p95 800-page vs p99 10k-page: different SLO is mature.

Cost: Textract pages dominate PDFs; Glue DPU for Excel; Bedrock only on samples.

## 0:75–0:85 Gaps

“What do you not build in v1?” Strong candidates defer website search index, full active-active DR, or per-tenant KMS until volume justifies it — and name the risk.

## 0:85–0:90 Close

Ask residual re-identification / OCR error risk. They should not claim 100% field accuracy.

## Remote tips

If they freeze on IAM, give a prompt: “Start with three S3 buckets and three roles.” Do not rescue the AI-exec issue.
