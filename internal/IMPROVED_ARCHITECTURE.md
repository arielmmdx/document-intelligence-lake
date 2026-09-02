# Improved architecture (evaluator reference)

This is a production-shaped answer, not the only acceptable one. Candidates may pick MWAA over Step Functions, Iceberg over a custom manifest, or EMR over Glue. Judge invariants.

## What was worth keeping from the naive sketch

- Medallion intent: raw land → structured silver → modeled gold.
- Layout as a **compressing signal**: if a 10,000-page packet is one form, discover structure once and apply many times.
- AI as an accelerator for **unknown** layouts, not as the per-page engine for known ones.
- AWS serving: Glue Data Catalog, Athena, BI, derived PDF, website.

## What to replace

| Naive | Replacement |
| --- | --- |
| LLM writes Python, then `exec` | LLM/Textract emit a **declarative extraction contract**; a **trusted interpreter** in ECR executes it |
| First 20 pages = layout | Stratified sample + **page fingerprints**; split the document if the fingerprint changes |
| One Python job for all formats | Format adapters; OCR only when there is no reliable text layer |
| One machine for 10k pages | Page-range work units; Textract async; map in Step Functions |
| Glue crawler = model | Explicit schemas / Iceberg; crawlers optional |
| One bucket, one role | Zones, CMKs, job roles, Lake Formation, SSO+MFA for humans |
| Copy into `silver/current/` | Staging + verify + **one catalog/snapshot commit** |

## Logical pipeline

1. **Land** — customer upload or SFTP → S3 landing. Checksum, tenant, content-type, Object Lock. Never mutate the object.
2. **Classify** — ECS Fargate: magic bytes, PDF text-layer probe, page count, encryption, size. Write bronze **inventory** (Glue table of objects), not a second copy of bytes unless required for legal isolation.
3. **Route**
   - Known layout fingerprint → pin `contract_id@version`
   - Unknown → layout discovery
   - Excel/CSV large → Glue Spark
   - SQLite → snapshot worker with paging queries
   - Unreadable/encrypted → quarantine
4. **Discover layout (expensive, rare)** — sample cover, 10%, 50%, 90%, last pages. Textract AnalyzeDocument and/or Bedrock multimodal. Output JSON contract: repeating header, table columns, key-value regions, page-local vs document-global fields. Human or policy gate. Store in registry.
5. **Extract (cheap, parallel)** — interpreter applies contract. PDFs: batches of N pages (e.g. 50) with overlap for tables that span pages. Merge in a reduce step keyed by `document_id`.
6. **Silver** — typed Parquet/Iceberg, `tenant_id`, `document_id`, `source_uri`, `page_range`, `layout_version`, `pii_class`, `extraction_job_id`.
7. **Gold** — business entities (claim, shipment, invoice line). Conformed keys across PDF and Excel for the same tenant.
8. **Publish** — independent checks (row counts vs pages, required fields, PII tags present) then Iceberg snapshot or manifest swap. Athena sees only published versions.
9. **Serve** — Athena workgroup per tenant; Tableau/PBI on gold; PDF renderer reads gold + template; website reads API on aggregates or governed views, not landing PDFs.

## AI, used correctly

AI is a **compiler of structure**, not the database.

- Call models on **samples and unknown templates**, not on every page of a known form (cost, quota, non-determinism).
- Deterministic OCR (Textract) for bulk pages; LLM for ambiguous header mapping and contract draft.
- Never give the model credentials to write S3 silver. It returns JSON to a service that validates against JSON Schema.
- If a team insists on generated Python: output is a **pull request** to the extractor repo → tests → image → ECR digest pinned in the contract. No runtime `eval`.

## Compute routing rule (copy this thinking)

```text
if format in {xlsx, csv} and (rows > ~2e6 or bytes > ~1GB):
    Glue Spark (or EMR)
elif pdf pages > ~200 or scanned:
    Step Functions map + Textract async + small Python reducers on ECS
elif sqlite:
    one (or few) workers; page by primary key; do not upload sqlite to Spark as a blob
else:
    ECS Fargate Python
```

Registry/control-plane Spark is optional. If a long-lived EMR cluster is idle cost, Glue jobs are the default Spark plane.

## S3 layout (example)

Separate buckets (not only prefixes) for blast-radius and CMKs:

- `dl-landing-{env}` — raw, Object Lock
- `dl-quarantine-{env}` — same classification as raw
- `dl-bronze-inventory-{env}` — metadata tables
- `dl-silver-{env}`
- `dl-gold-{env}`
- `dl-artifacts-{env}` — contracts, ECR-unrelated specs, manifests
- `dl-serving-pdf-{env}` — generated PDFs, shorter retention optional

Prefixes always include `tenant_id=/dt=/document_id=`.

## IAM (minimum set)

Humans: Identity Center permission sets, MFA. No access keys.

| Role | Can | Cannot |
| --- | --- | --- |
| ingest-task-role | Put landing, put inventory | Read silver/gold, invoke Bedrock |
| layout-task-role | Get landing, Textract/Bedrock, put artifacts/contracts | Put gold, Glue catalog mutate for gold |
| extractor-task-role / glue-extract-role | Get landing + contracts, put silver staging | Read other tenants; PutObject landing |
| glue-model-role | Read silver, write gold, Update catalog | GetObject landing |
| athena-analyst-role | Lake Formation gold (row filter tenant) | s3:ListBucket landing |
| render-pdf-role | Read gold, put serving-pdf | Read landing |
| ci-deploy-role | Push ECR, update task defs | GetObject landing |
| break-glass | time-bound raw read | standing grant |

SSO groups map to Lake Formation roles. Tableau uses a service role equivalent to analyst, scoped per tenant connection.

## PII

- Classify at extract time (rules + optional model on **fields**, not full pages in logs).
- Column tags in Glue; Lake Formation column filters for restricted attributes.
- Tokenization of government ids in gold if analysts do not need them; keep reversible tokens in a tighter vault if operations must reprint PDFs.
- Macie periodic scan on landing as detection-in-depth, not the primary catalog.
- Logs: job_id, page_range, confidence histograms, not strings.

## Glue catalog

- Databases: `bronze_inventory`, `silver`, `gold`, per env.
- Tables registered explicitly from the job (or Iceberg). Crawlers only for forensics.
- Partition projection or Iceberg hidden partitioning to avoid millions of partition objects.
- If Spark is only needed occasionally, Glue jobs beat a standing cluster. Athena for serving, not for heavy extract.

## Serving details

- **Tableau/Power BI**: Athena connector against gold views. Watch string vs decimal, timestamp timezone, partition filters, and SPILL. Extract to Hyper/PBIT only if SLA needs it — then the extract job is another publisher with its own freshness SLO.
- **New PDF**: template (ReportLab, Prince, Lambda container) filled from gold. This is the only way the “same PDF but readable” story is deterministic. Do not round-trip OCR text into a new PDF without a schema.
- **Website**: authenticated app → API Gateway → query a **serving store** (gold via Athena for low QPS, or projected OpenSearch/Dynamo for search). Direct S3 GET on landing is a data leak.

## Reliability

- Work id = hash(tenant, checksum, contract_version).
- Retries idempotent into staging prefixes named by `run_id`.
- Poison page: quarantine + continue siblings only if the publish policy allows partial documents (default: fail the document, not the whole tenant day).
- Verification reads **serialized silver**, not in-memory dicts.
- Replay: same contract version ⇒ same silver bytes (OCR noise: store Textract JSON as bronze derivative to make replay stable).

## SLA and cost sketch (order of magnitude)

Assumptions to challenge, not to memorize:

- Textract Detect: on the order of cents per page; 10k pages is a **cost event**, so only OCR pages that classify as scanned.
- Bedrock on 15 sample pages per unknown template, not 10k times.
- Glue DPU-hours for large Excel dominate that path.
- p95 800-page digital PDF: minutes on ECS without Textract.
- p99 10k scanned: hours acceptable if queued and reported; burst Textract TPS is the quota to file a ticket for.

State uncertainty: OCR retries, throttling, and layout-change splits can 2–5× the p99.

## v1 vs later

**v1:** landing, classify, Textract path, one contract language, ECS + Glue routing, silver Iceberg, Athena, Lake Formation tenant row filter, PDF render job, CloudTrail.

**Later:** per-tenant CMK, website search index, automatic layout clustering without humans, cross-region DR promote, streaming ingest.

Do not defer: tenant isolation, publish gate, no LLM-exec, quarantine accounting.
