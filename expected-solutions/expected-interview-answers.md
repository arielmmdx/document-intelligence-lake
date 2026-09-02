# Expected interview answers

Crib sheet for the interviewer. Phrases need not match. This is what a **strong** vs **weak** answer sounds like — not a script the candidate must recite.

## 1. SLA and completeness

**Strong:** Completeness is a **batch + document** tuple. A document is not published until required fields and page accounting match. p95 and p99 have different SLOs. Consumers read a **published snapshot**.

**Weak:** “The file is done when the Lambda returns 200.”

## 2. Bronze

**Strong:** Immutable landing object + inventory table (checksum, tenant, pages, classifier). Optional derivative: Textract JSON in a bronze prefix, still raw-class.

**Weak:** Immediate OCR into a SQL table called bronze.

## 3. Formats

**Strong:** Probe PDF text layer; OCR only if needed. Excel → Spark when large; never OCR xlsx. SQLite integrity check + keyed paging. Word: native parser first; convert to PDF only if print-layout is the product.

**Weak:** “Everything becomes PDF then OCR.”

## 4. Layout / AI

**Strong:** Contract JSON, registry, fingerprint, stratified pages, mid-doc drift, human/CI gate, Bedrock/Textract on samples. Generated code only via ECR digest.

**Weak:** Cron that asks GPT to write `extract.py` and runs it on prod data.

**Follow-up if they are close:** “Who can change a contract, and how do old documents replay?”

Expect: contracts immutable; new version; replay is a new silver snapshot.

## 5. Compute

**Strong:** Explicit thresholds; Step Functions map; Glue when registry/compute of workers is not worth EMR; Fargate for bounded Python.

**Weak:** “We’ll use an EMR cluster for everything” or “Lambda 15 minutes for 10k pages.”

## 6. Model and catalog

**Strong:** Grain stated (e.g. invoice_line). `layout_version` as a dimension. Iceberg or manifest. Crawler skepticism.

**Weak:** One wide table of `key, value, page` forever, crawler nightly, no tenant column.

## 7. Serving

**Strong:** Gold is truth. PDF is a render. BI on Athena/LF. Website on API with authn matching SSO groups.

**Weak:** Tableau on `s3://landing`. Website `<img src=pre-signed raw pdf>`.

## 8. IAM / SSO / MFA

**Strong:** Identity Center, MFA, permission sets; task roles listed; CI cannot read PII; break-glass.

**Weak:** One instance profile `AdministratorAccess`. Access keys for analysts.

## 9. PII

**Strong:** Classify fields; column filters; tokenization story; logs without payloads; KMS per zone; quota if KMS is in the inner loop.

**Weak:** “S3 is encrypted so we are fine.”

## 10. Reliability

**Strong:** Idempotent work ids, staging, independent verify, quarantine with counts, retry limits.

**Weak:** Unlimited retries; DLQ as a folder nobody reads.

## Partial credit patterns

- They want generated Python but immediately add sandbox, allowlist imports, and promotion: **Hire-leaning** if the rest is solid.
- They insist on EKS: fine if they own the operational cost vs Fargate/Glue.
- They reject Lake Formation for Databricks Unity / Snowflake: acceptable if AWS constraint is addressed (e.g. still catalog + IAM) or they explicitly change the constraint.
