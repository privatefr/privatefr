# Samples

A finished job, end to end, so the work can be judged on files rather than promises.

## `books-demo/` — a public catalog turned into a clean workbook

Source: `books.toscrape.com`, a site published specifically for scraping practice.

| File | What it is |
|---|---|
| `raw.csv` | the extraction as it came off the pages — 100 rows, untyped |
| `clean.xlsx` | the deliverable: typed columns, native table, filter, frozen header, and a summary sheet built on formulas that recalculates when you open it |
| `build.py` | the script that produced the workbook from the raw file |
