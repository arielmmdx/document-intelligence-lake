# Diagrams

## Architecture (AWS icons)

Open [`architecture.drawio`](architecture.drawio) in [diagrams.net](https://app.diagrams.net) (**File → Open from device**) or with the Draw.io VS Code/Cursor extension.

Four sheets:

| Sheet | Contents |
| --- | --- |
| **01 Medallion architecture** | End-to-end with official AWS4 icons: landing → bronze → layout/AI → extract → silver → gold → serve, plus control plane |
| **02 Layer contracts** | What belongs in each medallion layer, who may access it, which AWS services |
| **03 Identity and zones** | SSO/MFA, job roles, KMS, VPC endpoints, S3 buckets |
| **04 Compute and AI** | ECS vs Glue vs Textract vs SQLite worker, and the AI boundary |

If an icon shows as a blank square, diagrams.net is not loading `mxgraph.aws4`. Open the file at app.diagrams.net (library is built in).

Mermaid files (`.mmd`) remain a lightweight paste into [mermaid.live](https://mermaid.live).
