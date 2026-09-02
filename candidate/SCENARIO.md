# Scenario

A records-operations company scans and collects documents for regulated customers (insurance, logistics, healthcare-adjacent back office). Downstream analysts and customer portals must search, aggregate, and **re-render** the same information that today lives in files.

## Sources

Inbound objects are not a single format:

| Source | Typical shape | Pain |
| --- | --- | --- |
| Scanned PDF | Image-only pages, 50–10,000 pages, often a repeating form layout after a cover section | OCR, layout drift, tables that span pages, skewed scans |
| Digital PDF | Embedded text and/or mixed scanned appendices | Do not OCR everything; still need structure |
| Excel / CSV | Multi-sheet workbooks, merged headers, 10k–50M rows | Typing, header detection, Spark vs pandas |
| Word | Narrative + embedded tables/images | Structure vs free text |
| SQLite | Operational extracts, FKs, blobs | Integrity, unsplittable files, PII in blobs |
| Plain text / email dumps | Encoding issues, long lines, nested forwards | Chunking, entity extraction |

The **same business entity** (policy number, shipment id, person) can appear across formats in one customer batch.

## What “done” means for the business

1. A batch lands immutably. Nothing is silently dropped.
2. Structured fields become queryable in a data lake within the stated SLA.
3. PII is classified and access-controlled. Raw scans are not the same zone as analyst tables.
4. Consumers can:
   - run SQL in Athena
   - connect Tableau or Power BI
   - generate a **new PDF** (cleaned/standard layout) from extracted data
   - show selected fields on an authenticated website
5. Failures are visible: poison pages, unknown layouts, and partial batches cannot look like a successful publish.

## Volumes (planning numbers)

Use these unless you state better assumptions:

- 2,000 documents/day average; 8,000 on month-end peaks
- p50 PDF = 40 pages; p95 = 800 pages; p99 = 10,000 pages
- 15% of objects are Excel; 5% Word; 2% SQLite; rest PDF/text
- OCR on a 10,000-page PDF is the worst-case unit you must design for
- Retention: raw 7 years (legal hold capable); silver/gold 3 years unless legal hold
- Multi-tenant: ~40 customers. Tenant isolation is required. Cross-tenant query is forbidden.

## The team’s first idea (you will improve this)

1. Land the file in a bronze layer.
2. An AI component reads the first ~20 pages, infers a stable layout, and **writes a Python script**.
3. Run that script over the rest of the document and land rows in silver.
4. Model data for analytics.
5. Catalog with AWS Glue, query with Athena, and serve PDF / BI / website.

Read [NAIVE_ARCHITECTURE.md](NAIVE_ARCHITECTURE.md) before proposing your design. A strong answer keeps what is useful (medallion layers, layout-as-signal, AWS serving) and replaces what is unsafe or unscalable.
