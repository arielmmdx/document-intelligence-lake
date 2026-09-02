# Work trial: Document Intelligence Lake (conceptual)

Este directorio es un **work trial de arquitectura** para evaluar a un **senior data engineer**. No pide escribir un pipeline. Pide que la persona razone sobre un problema real: documentos heterogéneos (PDF escaneados de miles de páginas, Excel, Word, SQLite, texto) que deben convertirse en un data lake consultable, con gobernanza AWS.

El trial de código que el cliente preparó en `cloud-data-anonymization` (anonymization a escala, Docker, 8 horas) se analizó y **no se modificó**. Es un buen filtro de implementación. Este trial cubre otra señal de seniority: diseño de sistemas, fronteras de seguridad, unidades de trabajo, IA con control, y serving.

## Por qué este formato

Un senior no se demuestra principalmente con un test de código. Se demuestra cuando:

- Parte un problema ambiguo en contratos, capas y unidades retryables.
- Elige Python en ECS vs PySpark/Glue según forma del dato, no por moda.
- Trata a la IA como un componente con costo, alucinación y superficie de ataque, no como magia que “escribe un script”.
- Define IAM, PII, SSO/MFA, publicación atómica y catálogo antes de hablar de dashboards.
- Puede decir qué no haría, con números y supuestos.

## Cómo usarlo

Hay dos pistas. Usá **una**, no las dos el mismo día.

| Pista | Duración | Entrega | Cuándo |
| --- | --- | --- | --- |
| **Live system design** | 75–90 min | Conversación + pizarra / mermaid | Entrevista síncrona |
| **Take-home conceptual** | 4–6 h calendario | `SUBMISSION.md` escrito, sin código | Async, zona horaria |

Material:

- Candidato: [`candidate/`](candidate/README.md)
- Evaluador (no enviar): [`internal/`](internal/README.md)

## Qué recibe el candidato

El brief incluye una **arquitectura ingenua** (la que se pensó al inicio): ingest a bronze → IA genera Python a partir de las primeras 20 páginas → ejecutar script → silver → modelado → Glue/Athena → PDF/dashboard/web.

El ejercicio es **criticarla y rediseñarla**. Un senior fuerte no implementa esa idea tal cual; la convierte en contratos versionados, runtime cerrado, routing de cómputo y zonas de datos.

## Qué no es este trial

- No hay starter Python, Dockerfile ni fixture oculta.
- No hay “código correcto”.
- No se espera que el candidato despliegue AWS.
- No se menciona internamente el trial de anonymization ni su rúbrica.

## Recomendación de hiring

Holística, igual que el trial de código del cliente:

`Strong hire / Hire / Mixed / No hire / Strong no hire`

La rúbrica está en [`internal/RUBRIC.md`](internal/RUBRIC.md).

## Empaquetar para el candidato

```bash
cd /Users/macbook/Data/g2i/data_evaluation
zip -r document-intelligence-lake-candidate.zip candidate
```

No incluir `internal/` ni este README raíz si el README menciona material de evaluador.

