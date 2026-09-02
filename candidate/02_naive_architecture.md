# 02 — Naive architecture (critique this)

This is the **first whiteboard**, not the target. Keep medallion layers, layout-as-a-signal, and AWS serving. Replace what is unsafe or will not scale.

```text
file → (1) bronze
     → (2) LLM, first 20 pages, emits a Python script
     → (3) run that script on the full document → silver
     → (4) modeling
     → (5) Glue crawler + Athena + Tableau + website + new PDF
```

Implied sketch: one S3 bucket, `exec` of model-generated Python, one process for a 10,000-page PDF, crawler as “the model,” everyone on one Athena workgroup.

See [diagrams/01_naive_pipeline.mmd](diagrams/01_naive_pipeline.mmd).

## Take a position on each

1. Generated Python running on real PII.
2. “First 20 pages define the rest of the packet.”
3. One machine / one process for 10,000 pages or 50M Excel rows.
4. The same OCR path for Excel, SQLite, and Word.
5. Glue crawler vs an explicit silver/gold schema.
6. Copying files into `silver/current/` as “publish.”

Your redesign must use **Apache Airflow** (Amazon MWAA) as the orchestrator of the whole pipeline — see [03_constraints.md](03_constraints.md).
