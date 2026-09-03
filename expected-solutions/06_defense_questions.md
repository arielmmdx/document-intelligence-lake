# 06 — Questions to make the candidate defend their position

`02_expected_interview_answers.md` tells you what a strong answer sounds like when the candidate is talking. This file is for after they stop talking — pointed follow-ups that test whether the position holds up, not just whether it was stated. This is where the **data-architect** signal shows up most: can they reason about failure modes, governance, and what happens after the demo, not just draw the happy path.

Use 3–4 of these, picked from whichever section they were strongest or vaguest in. They fit the `0:70–0:85` block in `03_interview_facilitator_guide.md` if time remains. For a staff/architect-level backfill, this file can also be the spine of a dedicated second-round architecture conversation instead of a stretch add-on.

Do not run all nine sections in one sitting — that is an interrogation, not an interview.

## Orchestration & idempotency

- Two DAG runs fire for the same file (a retry racing a backfill). Walk me through what stops silver from being written twice.
- What is the idempotency key, exactly — file hash, S3 key + version, something else? What happens if the same file is re-uploaded with one field corrected?
- The ECS classify task crashes after writing bronze but before extraction starts. How does the DAG know to resume instead of silently skipping the file?

**Strong:** names a concrete key (e.g. `tenant_id + file_hash + recipe_version`), separates "same input → deterministic skip or overwrite" from "unknown state → alert," ties retries to Airflow's own run-id/task-instance semantics.
**Weak:** "it just re-runs," no key named; treats "idempotent" and "safe to retry blindly" as the same thing.

## Compute thresholds (Python/ECS vs PySpark/Glue)

- Where exactly is your Python-vs-Spark line, and what breaks first in each direction if you get it wrong?
- A 40-page PDF and a 9,000-page PDF hit the same DAG. Same code path, or different? Why?
- 3M-row Excel file lands on an ECS Fargate task. What fails first, and at what size would you have caught it before it does?

**Strong:** gives an actual number or heuristic, not just "it depends"; reasons about memory vs. parallelism vs. startup latency; admits the threshold is a judgment call they would tune against real data.
**Weak:** "Spark is always safer so I'd just use Spark everywhere" — no cost or latency trade-off.

## Recipe governance & schema evolution

- Six months in, the client changes their claim form. Old files used recipe v3, new ones need v4. How do rows extracted under both versions live in the same silver table?
- Who approves a new recipe before it touches production data — is the LLM's output ever trusted untested?
- How would you tell whether a recipe change is safe to auto-promote versus needing a human to look at it?

**Strong:** versioned recipes, `layout_version` carried through silver into gold, a promotion path (shadow-run the new recipe against a known-good sample before flipping it live), explicit human-in-the-loop for anything ambiguous.
**Weak:** "we'd just overwrite the recipe" — no versioning, no migration story for data already extracted under the old one.

## Distributed processing at scale

- A page range fails OCR 60% of the way through a 10,000-page job. Retry the whole file, or just that range? How do you know which pages already succeeded?
- How do you pick the page-range size — 50, 500, 5? What breaks if it is too big, or too small?
- Two workers accidentally claim overlapping page ranges. Does your design prevent that, or do you accept it and dedupe after?

**Strong:** partition-level checkpointing or a manifest of completed ranges, deliberate boundary overlap (to catch tables spanning pages) with a named dedup step, reasons about task overhead vs. parallelism.
**Weak:** "Spark handles that automatically," with no explanation of what Spark is actually doing to the PDF bytes.

## Data quality & testing

- How do you know silver is *correct*, not just *present*? What would catch a recipe silently extracting the wrong column?
- How would you test the extraction helpers without using real customer PII?
- A completeness check compares row count in gold against claim forms counted in bronze. Who runs that, and what happens on a mismatch?

**Strong:** names a concrete check (schema, row-count, or null-rate validation between layers; golden/synthetic fixture files; contract tests on the recipe schema); a failed check blocks publish or routes to quarantine, it does not just log a warning.
**Weak:** no answer, or "we'd eyeball it in Athena."

## Observability & incident response

- It's 3am and gold hasn't updated for tenant X. What paged someone, and what's the first dashboard or query they open?
- How do you tell "the pipeline is slow" from "the pipeline is stuck" before a customer complains?
- What do you log from inside the OCR/LLM steps — and what do you deliberately not log, given the PII rule?

**Strong:** concrete signals (DAG SLA misses, task-duration percentiles, quarantine-rate alarms), separates business metrics (rows per tenant per day) from infra metrics, ties back to "no OCR text in logs."
**Weak:** "CloudWatch has logs," with nothing about what is actually monitored or alerted on.

## Security, multi-tenancy & governance

- One sentence per role: why can't the Airflow EC2 role read gold, and why can't the analyst role read landing?
- Two tenants' files land in the same S3 prefix by a config mistake. What in the design makes that hard to do by accident, versus just a policy that says "don't"?
- Who owns the contract between silver and gold, and what happens when a downstream Tableau dashboard breaks because gold's schema changed?

**Strong:** least privilege stated per role, tenant isolation enforced structurally (prefix-per-tenant plus IAM condition keys, not convention alone), a real mechanism for schema-change communication (versioned views, deprecation window) rather than "we'd tell them."
**Weak:** one shared role "to keep it simple"; "we'd just fix the dashboard after."

## Cost, capacity & v1 scope

- Ballpark: what does the OCR+LLM sample cost per 10,000-page file, and what does full-file OCR cost if the sampling assumption turns out wrong?
- Name three things you are explicitly not building in v1. What is the cost of being wrong about deferring each one?
- Month-end volume (8,000 docs/day) triples for a quarter. What is the first thing that falls over?

**Strong:** order-of-magnitude reasoning even with rough numbers, names the actual bottleneck (ECS task concurrency, Glue DPUs, LLM rate limits), ties v1 cuts to a monitored trigger for revisiting them.
**Weak:** no numbers at all, or "we'd just autoscale" with no mechanism named.

## Ownership & roadmap (the clearest architect signal)

- Who signs off that a new tenant's pipeline is production-ready — a checklist, or "it ran once"?
- A new engineer joins in month two. What is the one document they read first so they don't break silver?
- If you handed this design to another team to build, what would you put in an ADR that isn't already obvious from the diagram?

**Strong:** talks about runbooks, ADRs, onboarding docs, a promotion gate for new tenants — evidence they think about the system's life after the demo.
**Weak:** nothing beyond the diagram; no notion of how the design survives contact with a team.

---

None of this is a "must show" to pass — see `04_scoring_rubric.md`. A candidate who never gets asked these because time ran out is not penalized. A candidate who gets asked and answers well is a **Strong hire**, not just a **Hire**.
