# Expected answers and solutions — do not send to candidates

This folder is the **answer key**. It is the expected architecture, expected interview signals, facilitator script, and scoring rubric.

Send only `candidate/` to the person being interviewed.

## What is in here

| File | What it is |
| --- | --- |
| [expected-architecture.md](expected-architecture.md) | **Expected solution** — production architecture vs the naive sketch |
| [expected-interview-answers.md](expected-interview-answers.md) | **Expected answers** — strong vs weak signals per question (not a script they must recite) |
| [interview-facilitator-guide.md](interview-facilitator-guide.md) | Minute-by-minute live interview |
| [scoring-rubric.md](scoring-rubric.md) | Hire recommendation template |
| [comparison-with-coding-trial.md](comparison-with-coding-trial.md) | This trial vs the anonymization coding trial |
| [diagrams/expected-architecture.drawio](diagrams/expected-architecture.drawio) | Expected AWS architecture (debrief only) |
| [diagrams/expected-architecture-overview.mmd](diagrams/expected-architecture-overview.mmd) | Compact mermaid of the expected design |
| [examples/expected-extraction-contract.json](examples/expected-extraction-contract.json) | Example of the artifact AI should emit (not generated Python) |

## How to score

Holistic: `Strong hire / Hire / Mixed / No hire / Strong no hire`.

Do not require AWS certification vocabulary. Require work units, security zones, an AI boundary that is not `exec(llm)`, and a compute routing rule.

Show `expected-architecture.md` or the draw.io **only in the last five minutes**, and only if you want a teaching debrief.
