# 01 — Expected architecture (solution)

Not the only valid design. Invariants matter: Airflow orchestrates, workers are Python or PySpark, work units are bounded, AI does not `exec` code, publish is atomic.

## Spine: one Airflow DAG on Amazon MWAA

Lambda is not used. MWAA sensors and operators call ECS and Glue.

```text
T1  s3_sensor          wait for landing object (checksum in XCom)
T2  classify           ECS Python: MIME, scanned?, page count, sheets, size
T3  branch             PDF | Excel | SQLite | Word/text | quarantine
T4a layout             ALWAYS for unknown fingerprints: sample → extraction contract
T4b extract            apply that contract at scale (ECS and/or Glue PySpark)
T5  silver             Glue PySpark: types, PII tags, Iceberg staging
T6  gold               Glue PySpark: business grain, conformed keys
T7  publish            Iceberg snapshot / catalog swap, then optional PDF render
```

**T4a is not PDF-only.** Excel and Word also need a layout/contract. What changes is *how you sample* and *which engine applies the contract* — not whether you skip discovery.

- **MWAA node** only orchestrates (sensors, BranchPythonOperator, GlueJobOperator, EcsRunTaskOperator, ShortCircuit). No OCR, no Spark, no pandas on 50M rows on the scheduler/worker of Airflow.
- **Idempotency key:** `tenant_id + sha256(file) + contract_version`. Same key → skip or overwrite staging for that `run_id` only.
- **Mapped tasks** (Airflow 2.3+ dynamic task mapping): one mapped ECS task per 50-page PDF batch with 1-page overlap.
- **Pools:** `textract`, `glue_dpu`, `ecs_extract` so one hot tenant cannot starve the cluster.
- **Retries:** Airflow retries the **task**, not the whole DAG, with backoff. Glue jobs are restartable from staging.

## Python vs PySpark (expected rule)

| Work | Engine | Why |
| --- | --- | --- |
| Classify, Word, small digital PDF, SQLite paging, layout sample | **Python on ECS** | Format adapters, bounded memory, simple retries |
| Excel/CSV ≳ 2M rows or ≳ 1 GB | **PySpark on Glue** | Splittable rows, driver must not collect the workbook |
| Gold joins, compaction, Iceberg commit | **PySpark on Glue** | Cluster CPU, partition by `tenant_id` |
| 10k-page scanned PDF | **Mapped ECS + Textract async** | Pages are the partition; Spark does not split a JPEG PDF usefully |

SQLite: integrity check + `SELECT … WHERE id > ? LIMIT n` in Python. Do not hand Spark a 40 GB `.sqlite` blob.

## Layout / AI (every messy format, including Excel and Word)

Do **not** send a 50M-row workbook or a 10k-page PDF through Bedrock row-by-row. Do **not** OCR `.xlsx`.

Do **always** (unless a known `contract_id` already matches the fingerprint):

1. **Sample** a cheap slice.
2. Draft or match an **extraction contract** (JSON): columns, header row, sheet names, repeating tables, PII flags.
3. **Promote** the contract (schema + optional human/CI).
4. **Apply** it with a trusted runtime at scale.

| Format | Sample for layout (T4a) | Apply at scale (T4b) |
| --- | --- | --- |
| Scanned PDF | Stratified pages + Textract/Bedrock | Mapped ECS + Textract on page batches |
| Digital PDF | Text-layer sample, not full OCR | ECS Python interpreter |
| Excel / CSV | First ~200 rows, all sheet names, merged-cell map; Bedrock only on that sample if the header is ambiguous | **Glue PySpark** reads the rest with the contract (`header_row`, `skip_rows`, column map) |
| Word | Headings + first tables via python-docx; Bedrock on that extract if needed | ECS Python (document is rarely Spark-shaped) |
| SQLite | `PRAGMA` + `LIMIT` sample per table | Python paging; schema *is* the contract if it is already relational |

Skipping T4a for “large Excel” in an older sketch was a shortcut. The shortcut is only: **no OCR / no LLM on every row**. Discovery still happens on a sample. Known tenant templates skip T4a after a fingerprint hit.

## Medallion

| Layer | Holds | Who reads |
| --- | --- | --- |
| **Landing** | Immutable original bytes, Object Lock, CMK-raw | ingest + layout + extract roles |
| **Bronze** | Inventory (object, pages, class) + optional Textract JSON (still raw-class) | pipeline roles |
| **Silver** | Typed Parquet/Iceberg: `tenant_id`, `document_id`, `page_range`, `layout_version`, `pii_class` | extract/model; analysts only if Lake Formation allows |
| **Gold** | Business entities (claim, line, shipment) | Athena analysts, Tableau, PDF renderer, API |
| **Serve** | Not a lake layer: Athena workgroups, BI, ECS PDF from **gold**, website API |

Quarantine is landing-class, never under a serving prefix.

## Security (short)

SSO + MFA for humans. MWAA execution role starts ECS/Glue but does not need `s3:GetObject` on all of gold if workers have their own roles. Analysts never list landing. KMS data keys at **job** grain, not per page.

## Serving

Gold is source of truth. Tableau → Athena. New PDF = render job from gold. Website ≠ pre-signed landing PDFs.

## v1

Ship: MWAA DAG, classify, Textract path, one contract language, ECS + Glue routing, Iceberg publish, Lake Formation tenant filter, PDF job.

Defer: website search index, per-tenant CMK, active-active.
