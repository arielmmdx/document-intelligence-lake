# Internal — do not send to candidates

## Purpose

Evaluate senior data engineering **judgment** on a document-to-lake platform. No code is required. The candidate critiques a naive AI-generates-Python pipeline and produces a production design on AWS.

## Package vs candidate zip

Send only `candidate/`. This `internal/` directory, filenames, and the comparison to the anonymization coding trial stay private.

## Files

| File | Use |
| --- | --- |
| [FACILITATOR.md](FACILITATOR.md) | Minute-by-minute live interview |
| [RUBRIC.md](RUBRIC.md) | Hire recommendation |
| [EXPECTED_ANSWERS.md](EXPECTED_ANSWERS.md) | Signals, not a script the candidate must match |
| [IMPROVED_ARCHITECTURE.md](IMPROVED_ARCHITECTURE.md) | Reference design (improved vs the naive sketch) |
| [COMPARISON.md](COMPARISON.md) | This trial vs `cloud-data-anonymization` |
| [diagrams/](diagrams/) | Target draw.io + mermaid for debrief only |

## How to score

Holistic: `Strong hire / Hire / Mixed / No hire / Strong no hire`.

Do not require AWS certification vocabulary. Require work units, security zones, an AI boundary that is not `exec(llm)`, and a compute routing rule.
