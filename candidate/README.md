# Document Intelligence Lake — candidate brief

You are designing a production data platform for a client that digitizes mixed business documents and needs them queryable, governable, and presentable. This is an **architecture exercise**. Do not write application code, Dockerfiles, Terraform, or notebooks.

Time box:

- Live interview: 75–90 minutes. Think out loud. Diagrams on a whiteboard, mermaid, or paper are enough.
- Take-home: 4–6 hours calendar time. Complete `SUBMISSION.md`. Stop when the time box ends and list what you would do next.

You may use search, vendor docs, and AI tools. Disclose them. Verify claims; do not paste an architecture you cannot defend.

## Read in this order

1. [SCENARIO.md](SCENARIO.md) — business problem and volumes
2. [NAIVE_ARCHITECTURE.md](NAIVE_ARCHITECTURE.md) — the team’s first sketch (you must critique it)
3. [CONSTRAINTS.md](CONSTRAINTS.md) — AWS, security, and delivery rules
4. Diagrams in [diagrams/](diagrams/) — copy the `.mmd` files into [mermaid.live](https://mermaid.live) if useful
5. [QUESTIONS.md](QUESTIONS.md) — discussion prompts (live) or writing prompts (take-home)
6. [SUBMISSION.md](SUBMISSION.md) — take-home template only

## What we evaluate

Judgment under incomplete information. We look for work-unit design, format-specific adapters, a controlled role for AI, compute routing (ECS Python vs Glue/Spark), medallion modeling, Glue/Athena serving, IAM and PII boundaries, and honest cost/SLA arithmetic. Naming every AWS service is not a signal.
