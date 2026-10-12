# Samples

Finished jobs, end to end, so the work can be judged on files rather than promises.

## `books-demo/` — a public catalog turned into a clean workbook

Source: `books.toscrape.com`, a site published specifically for scraping practice.

| File | What it is |
|---|---|
| `raw.csv` | the extraction as it came off the pages — 100 rows, untyped, HTML entities intact |
| `clean.xlsx` | the deliverable: typed columns, native table, filter, frozen header, a summary sheet on formulas, and a print setup that does not clip long text |
| `build.py` | the script that produced the workbook from the raw file |

Re-run it (`python build.py`) and you get the same workbook back. Cleaning lives in the
script, not in the raw file, so every judgement call stays visible and re-playable.

## `pdf-vers-tableur/` — a printed PDF turned back into one table

A workbook exported to PDF splits into column slices across pages, and the layout clips
long text. Automatic extraction returns fragments; this returns a table.

| File | What it is |
|---|---|
| `source.pdf` | the source: a 3-page print of the catalog above |
| `extract.py` | the extraction and stitching script — fragments grouped by column set, re-stitched vertically then horizontally, clipped cells flagged rather than silently dropped |
| `result.csv` | the result: 100 rows × 6 columns, recovered from the fragments |
| `delivery-report.md` | the delivery report: 90/100 titles identical to the source, 10 flagged as clipped by the PDF itself, 0 price discrepancies |

The interesting part is not the extraction — it is that the result is **checked against the
source** and every unrecoverable cell is listed. Blind tools ship the damage quietly.
