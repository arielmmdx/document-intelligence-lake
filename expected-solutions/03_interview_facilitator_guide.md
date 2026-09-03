# 03 — Take-home review & debrief guide

Use the Mermaid in this folder's README, or the root README, if you want to walk a candidate through the reasoning after the fact.

## Before

Send `candidate/` (zipped) with an offline, at-home, **8-hour** deadline. The problem is `candidate/README.md`; `01_tips`–`05_tips` are prompts. Use `expected-solutions/README.md` as your own full explanation.

## Reviewing the write-up

Read it against `05_tips.md`'s structure:

- **Critique** of the naive design — generated Python, first 20 pages, one process, crawler as model.
- **Airflow + Python + PySpark + distribution** — what runs on Airflow EC2 vs ECS vs Glue, how the LLM sees a 10k-page PDF (sample, not the whole file), mapped ECS tasks vs Spark partitions, the idempotency key.
- **Medallion, publish, security** — landing vs bronze vs silver vs gold, snapshot commit, SSO/MFA, task roles, landing not for analysts.
- **Serving, SLA, v1 cuts** — p95 vs p99, order-of-magnitude cost, three deferrals and why they're safe to defer.

Score against `04_scoring_rubric.md`. `02_expected_interview_answers.md` has strong/weak phrasing to compare the write-up against. `README.md`'s "Engineering practices to evaluate" section tells you what to look for on Python/PySpark/Airflow craft, logging, and IAM.

If they reach for Lambda or Step Functions without addressing the constraint, or never critique `exec()` of LLM-written Python: that is the rubric's negative signal, not a stylistic choice — do not read past it as a minor omission.

## Optional debrief call (30–45 min)

For a **Hire** or **Mixed** write-up, a short call confirms the reasoning is theirs and not copy-pasted. Pull 3–4 questions from `06_defense_questions.md`, matched to whichever section of the write-up was vaguest.

This is a spot check, not a re-run of the exercise. Do not rescue the LLM-exec point or the IAM-roles point if they freeze on it — a freeze is itself the signal.
