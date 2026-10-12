# Automation & data extraction

I turn messy sources into clean, checkable data. An AI assistant handles the repetitive
work; a human is accountable for what gets delivered.

## What I do

- **Documents → structured data.** PDFs, scans, invoices and reports become tidy Excel/CSV
  files, with the extraction rules written down so the job can be re-run on the next batch.
- **Web → spreadsheet.** Public pages, catalogs and listings become one clean table,
  refreshed on demand.
- **Recurring monitoring.** A daily or weekly digest of what changed on the pages you care
  about — prices, stock, wording, listings — delivered by email or chat, with a screenshot
  when the change is visual.
- **Small automation and repairs.** Scripts that fetch, clean, merge, rename and file things
  on a schedule, including fixing ones that stopped working.

## A complete sample, in this repository

[`samples/books-demo/`](samples/books-demo/) is a finished job end to end, from a public
catalog built for scraping practice:

| File | What it is |
|---|---|
| `raw.csv` | the extraction as it came off the pages — 100 rows, untyped |
| `clean.xlsx` | the deliverable: typed columns, native table, filter, frozen header, and a summary sheet built on formulas that recalculates when you open it |
| `build.py` | the script that produced the workbook from the raw file |

Nothing here is a black box: run `build.py` again and you get the same workbook back.

## How I work

- Scope agreed in writing before starting, and **a sample delivered first** so the format is
  validated on real rows while changes are still cheap.
- You receive the output file **and** the script that produced it.
- AI assistance is used in delivery and stated whenever a client or platform asks.

## Availability

Open to small paid jobs. Reach me by opening an issue in any of my repositories, or through
the platform you found me on.
