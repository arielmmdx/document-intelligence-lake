# Cómo facilitar (resumen)

Envía solo `candidate/`. Este archivo y `internal/` no viajan con el candidato.

## Formato

- **Live 75–90 min:** crítica del pipeline ingenuo → dibujo → IAM/PII → serving/SLA.
- **Take-home 4–6 h:** `candidate/SUBMISSION.md`, sin código.

## Qué tiene que salir de un senior

1. Rechaza `exec` de Python generado por un LLM sobre datos reales. Propone un **contrato de extracción** versionado y un runtime en **ECR**.
2. No cree que las primeras 20 páginas bastan: sample estratificado + fingerprint + cuarentena si el layout cambia.
3. Separa PDF escaneado, Excel grande y SQLite. **Glue Spark** cuando hay filas/archivos partibles y grandes; **ECS** para Python acotado; **Step Functions + Textract** para PDFs enormes.
4. Publicación atómica (Iceberg/manifiesto). Crawlers no son el modelo.
5. SSO + MFA para humanos, task roles para jobs, KMS por zona, Lake Formation por tenant, PII fuera de logs.

## Debrief

Si querés enseñar al final, abrí `internal/diagrams/architecture.drawio` o `internal/IMPROVED_ARCHITECTURE.md`. No lo muestres al arrancar.

Rúbrica: `internal/RUBRIC.md`.
