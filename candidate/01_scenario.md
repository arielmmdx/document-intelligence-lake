# 01 — Scenario

A records company digitizes mixed files for ~40 regulated customers. Analysts and a customer portal must **query** the same information that today lives in files, and sometimes **reprint** it as a clean PDF.

## Sources

| Source | Typical shape | Why it hurts |
| --- | --- | --- |
| Scanned PDF | 50–10,000 image pages; often one form after a cover | OCR, layout drift, tables that span pages |
| Digital PDF | Embedded text, sometimes mixed scanned appendices | Do not OCR everything |
| Excel / CSV | Multi-sheet, merged headers, 10k–50M rows | Typing and scale: pandas vs PySpark |
| Word | Narrative + tables | Structure vs free text |
| SQLite | Tables, FKs, blobs | Integrity; file may not split |
| Text / email dumps | Encoding, long lines | Chunking |

The same business id (policy, shipment, person) can appear across formats in one batch.

## Volumes (use these unless you change them and say why)

- 2,000 documents/day; 8,000 at month-end
- PDF: p50 = 40 pages, p95 = 800, p99 = 10,000
- Mix: ~15% Excel, 5% Word, 2% SQLite, rest PDF/text
- Raw retention 7 years (legal hold); silver/gold 3 years unless hold
- Tenant isolation: customer A must not see customer B

## Done means

1. Every file is accounted for (or quarantined with a reason). Nothing silent-dropped.
2. Structured fields are queryable in a lake within an SLA you define.
3. PII is classified. Raw scans are not the analyst zone.
4. Consumers: Athena SQL, Tableau or Power BI, a **new PDF** from tables, a website from governed data.
5. A partial run must not look like a successful publish.

## The team’s first idea (you will redesign this)

Bronze ingest → an LLM reads the first 20 pages and **writes Python** → that script runs on the whole file → silver → model → Glue crawler / Athena / BI / PDF / web.

Read [02_naive_architecture.md](02_naive_architecture.md) next.
