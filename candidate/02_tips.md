# 02 — Tips: improve the naive pipeline

The first whiteboard is in the [README](README.md). [diagrams/01_naive_pipeline.mmd](diagrams/01_naive_pipeline.mmd) is the same picture.

To improve it, take a clear position on each:

1. **Do not `exec` Python an LLM wrote** on real files. A recipe (JSON) plus a trusted program is safer.
2. **First 20 pages are not the whole packet.** Sample the start, middle, and end. If the layout changes at page 4,000, split or quarantine.
3. **One process cannot eat 10,000 pages or 50M Excel rows.** Split work (page ranges, Spark for big tables).
4. **Excel is not a scan.** Do not OCR `.xlsx`. Word and SQLite are not “the PDF brain.”
5. A **Glue crawler is not a data model.** Silver/gold need declared tables (or Iceberg), then Athena.
6. Copying files one by one into `silver/current/` is not a **publish**. You need one snapshot/manifest so readers never see a half write.

Keep: medallion layers, “layout is a signal,” S3 + catalog + Athena.
