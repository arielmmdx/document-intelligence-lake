# Work trial: Document Intelligence Lake

Architecture interview for a **senior data engineer**. No application code.

We test: **Apache Airflow on EC2** as orchestrator, **Bedrock LLM** for layout on a **sample** (not 10,000 pages), **Python** on ECS (images in ECR), **PySpark** on Glue, medallion layers, and governed serving. Not a Lambda-driven pipeline.

| Track | Time | Output |
| --- | --- | --- |
| Live system design | 75–90 min | Conversation + diagram |
| Take-home | 4–6 hours | `candidate/05_submission.md` |

| Folder | Send to candidate? |
| --- | --- |
| [`candidate/`](candidate/README.md) — numbered `01`–`05` | Yes |
| [`expected-solutions/`](expected-solutions/README.md) — numbered answer key | **No** |

One solution diagram: [`expected-solutions/diagrams/01_expected_architecture.drawio`](expected-solutions/diagrams/01_expected_architecture.drawio).

```bash
zip -r document-intelligence-lake-candidate.zip candidate
```
