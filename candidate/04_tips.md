# 04 — Tips: questions that raise the bar

Use these in the live interview or take-home. Strength is **Airflow, Python helpers, Spark, and the 10,000-page story**, not a list of AWS logos.

## Airflow

Sketch the DAG (sensors, retries, pools, mapped tasks). What must **never** run on the Airflow EC2? How do you key a run so a retry does not duplicate silver?

## Python you would write (describe, do not paste a product)

Helper module: function names, **imports**, **docstring** on each function (`sample_pages`, `extract_page_range`, …). DAG file: docstring (purpose, owner, retries). Which libraries sit in the **ECR image** vs on EC2? **Who writes silver** — the LLM or those helpers? What is the LLM’s only output?

## Python vs Spark vs 10k pages

When ECS Python vs Glue Spark (thresholds). How a 10,000-page PDF becomes page-range tasks. Is the LLM in that loop? 50M-row Excel: header row without driver OOM. SQLite: why Spark may be the wrong default.

## Layout

Why “LLM writes Python we exec” is an incident. Why first-20-pages is weak. Excel/Word still need a **sample recipe**, then scale extract — not OCR every cell, not LLM every row.

## Lake and access

Grain of bronze / silver / gold. When silver is published. Tableau on Athena. Airflow EC2 role vs ECS vs Glue vs analyst. Landing is not for analysts.

## v1

Three things you would **not** build first, and the risk of waiting.

## Depth (if you have time)

Not required, but it separates a senior data engineer from a data **architect**: How would you know silver is *correct*, not just present? What would page someone at 3am if gold stopped updating for one tenant? What happens to already-extracted data when the client changes their form and you need a new recipe version?
