# 01 — Expected architecture (solution)

Plain story (same as the root README). Invariants: Airflow on EC2 only starts work; the **LLM reads a sample**; a **Python or Spark job** writes silver; 10,000 pages are split into page-range tasks; no `exec` of model-written Python.

## Does the LLM scrape the whole PDF?

**No**, when the packet is a repeating form.

1. PDF → S3 landing (original kept).
2. ECS classifier: page count, scanned vs not.
3. ECS **sample**: pages 1–20, a few in the middle, last few. Not 10,000.
4. OCR on that sample if needed. **LLM** (any vendor; on AWS often Bedrock) writes a **recipe JSON**.
5. **Extract job** (ECS Python batches or Spark partitions of page ranges) applies the recipe to **every** page. **The LLM is not in this loop.**
6. That job writes **silver**. The LLM never writes the lake.

**If there is no repeating layout**, you cannot copy a recipe. Then OCR every page in parallel; LLM only for pages that fail or look new. Say the cost out loud.

Spark does not “load a PDF as a DataFrame.” Spark (or Airflow mapped ECS) runs the **same function** on many **page ranges**.

Excel/Word: same split (sample → recipe → Spark/Python on the rest). Do not OCR Excel. Do not LLM every row.

## DAG on EC2

```text
T1 sensor S3
T2 classify ECS (image from ECR)
T3 branch: known recipe / unknown / quarantine
T4a sample + LLM recipe (PDF, Excel, Word)
T4b extract at scale (ECS and/or Glue Spark) — this writes silver staging
T5 silver verify
T6 gold Spark
T7 publish snapshot; optional PDF from gold
```

Airflow EC2: no OCR, no LLM on 10k pages, no Spark driver for 50M rows.

## Medallion

Landing = bytes. Bronze = inventory. Silver = extracted fields + `layout_version`. Gold = business entities. Serve = Athena/Tableau/website/new PDF from **gold**.

## Python we expect them to *describe* (not paste a repo)

Helpers in a library: `sample_pdf_pages`, `build_recipe`, `extract_page_range`, `write_iceberg`. Docstrings on DAG, on each task callable, on helpers. Imports named (why `pypdf` vs OCR API vs `pyspark`). ECR image pins those libraries.
