# 03 — Interview facilitator guide (75–90 min)

Do not open draw.io. Use the Mermaid in the root README if you want a teaching debrief.

## Before

Send `candidate/` ~24 hours ahead. You use this folder. Whiteboard or mermaid.live.

## 0:00–0:08 Alignment

One-minute restatement: batch completeness, PII, tenants, SQL + BI + PDF + web.

If they reach for Lambda or Step Functions as the orchestrator: “Constraints say Airflow on EC2.”

## 0:08–0:22 Critique

Generated Python, first 20 pages, one process, one OCR path, crawler publish.

## 0:22–0:50 Airflow + Python + PySpark + distribution

Ask them to **draw the DAG**. Then:

- What runs on Airflow EC2 vs ECS vs Glue?
- How the LLM sees a 10k-page PDF (sample, not the whole file)
- Mapped ECS tasks for the remaining pages
- Excel Spark vs SQLite Python
- **Probe:** “Does large Excel skip layout? Why not OCR/LLM every row — and how do you still learn the header?”
- Idempotency key and pools

This block is the hiring signal for this trial.

## 0:50–0:70 Medallion, publish, security

Landing vs bronze vs silver vs gold. Snapshot commit. SSO vs task roles. Landing not for analysts.

## 0:70–0:85 Serving, SLA, v1 cuts

p95 vs p99. Textract cost. Three deferrals.

## 0:85–0:90 Close

OCR residual risk. Optional: walk the Mermaid in the root README.

If they freeze on IAM: “Three roles: Airflow, Glue, analyst.” Do not rescue the LLM-exec point.
