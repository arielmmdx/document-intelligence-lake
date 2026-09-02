# Work trial: Document Intelligence Lake (conceptual)

This repository is an **architecture work trial** for a **senior data engineer**. It does not ask the candidate to write a pipeline. It asks them to reason about a real problem: mixed documents (10,000-page scanned PDFs, Excel, Word, SQLite, text) that must become a queryable, governed data lake on AWS.

A separate coding trial (`cloud-data-anonymization`: Docker, eight hours, CSV/JSON/text/SQLite) was reviewed and **not modified**. That trial tests implementation. This trial tests another seniority signal: system design, security boundaries, work units, controlled AI, and serving.

## Why this format

A senior is not proven mainly by a coding test. They show up when they:

- Split an ambiguous problem into contracts, layers, and retryable work units.
- Choose Python on ECS vs PySpark/Glue from the shape of the data, not from fashion.
- Treat AI as a component with cost, hallucination, and an attack surface — not as magic that “writes a script.”
- Define IAM, PII, SSO/MFA, atomic publication, and the catalog before talking about dashboards.
- Can say what they would **not** build, with numbers and assumptions.

## How to run it

Use **one** track, not both on the same day.

| Track | Duration | Deliverable | When |
| --- | --- | --- | --- |
| **Live system design** | 75–90 min | Conversation + whiteboard / mermaid | Synchronous interview |
| **Take-home conceptual** | 4–6 hours calendar time | Written `SUBMISSION.md`, no code | Async / time zones |

| Audience | Folder | Send to candidate? |
| --- | --- | --- |
| Candidate brief | [`candidate/`](candidate/README.md) | Yes |
| Expected answers and solutions | [`expected-solutions/`](expected-solutions/README.md) | **No** |

## What the candidate receives

The brief includes a **naive architecture** (the first sketch): ingest to bronze → AI writes Python from the first 20 pages → run the script → silver → modeling → Glue/Athena → PDF / dashboard / website.

The exercise is to **critique and redesign it**. A strong senior does not implement that idea as-is; they turn it into versioned contracts, a closed runtime, compute routing, and data zones.

## What this trial is not

- No Python starter, Dockerfile, or hidden fixture.
- No single “correct” codebase.
- The candidate is not expected to deploy AWS.
- Do not mention the anonymization coding trial or its rubric to the candidate.

## Hiring recommendation

Holistic, same scale as the coding trial:

`Strong hire / Hire / Mixed / No hire / Strong no hire`

Score with [`expected-solutions/scoring-rubric.md`](expected-solutions/scoring-rubric.md).

## Package for the candidate

```bash
zip -r document-intelligence-lake-candidate.zip candidate
```

Do not include `expected-solutions/` or this root README (it points at the answer key).
