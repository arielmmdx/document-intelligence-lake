# Naive architecture (team sketch)

This is **not** the target design. It is the first whiteboard. Your job is to keep the intent and replace the failure modes.

## Intent that is worth keeping

- Immutable landing, then bronze / silver / gold.
- Layout is a signal: many 10k-page packets are the **same form** after a short preamble.
- AI can help **discover** structure faster than hand-writing every parser.
- Serving is not only SQL: regenerated PDF, BI, and a website share the same governed tables.
- AWS: S3, containers for Python, Glue catalog, Athena.

## Proposed steps

```text
source file
  → (1) ingest to bronze
  → (2) AI reads first 20 pages, emits a Python extractor
  → (3) run that Python on the full document → silver
  → (4) data modeling
  → (5) Glue catalog + Athena + Tableau/Power BI + website + new PDF
```

## Implied AWS sketch

- One S3 bucket with `bronze/` and `silver/` prefixes
- A Python job (unspecified compute) that calls an LLM
- `exec` or save-and-run of model-generated code
- Glue crawler on silver
- Athena workgroup for everyone
- Tableau connecting to Athena

See [diagrams/01-naive-overview.mmd](diagrams/01-naive-overview.mmd).

## Known tensions (you should go deeper)

You do not need to invent these from scratch, but you must take a position:

- First 20 pages may be a cover letter, TOC, or a **different** layout than page 4,000.
- A 10,000-page scanned PDF is not a single Python process on one laptop.
- Excel, SQLite, and Word do not need OCR; forcing one “PDF brain” onto them is waste.
- Generated Python is an unreviewed program with access to data. That is a security boundary.
- Glue crawlers infer schema; they do not create a semantic model or tenant isolation.
- Object PUT is atomic; publishing 400 Parquet files is not.

Your redesign should name components, data contracts, IAM roles, PII handling, compute routing, and how a layout version is approved and reused.
