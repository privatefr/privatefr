#!/usr/bin/env python3
"""Construit le classeur livrable à partir du CSV brut.

Entrée  : demo-livres-bruts.csv   (extrait brut, tel que récupéré du site)
Sortie  : demo-livres.xlsx        (classeur propre : données typées + feuille de synthèse à formules)

C'est volontairement le script réel du livrable : le client reçoit le fichier ET l'outil
qui l'a produit, donc rien n'est une boîte noire et le traitement est rejouable.
"""
import csv
import statistics
from datetime import date
from html import unescape
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

SRC = Path("demo-livres-bruts.csv")
OUT = Path("demo-livres.xlsx")
SOURCE = "books.toscrape.com (site public d'entraînement au scraping)"

HEAD_FILL = PatternFill("solid", fgColor="2F5496")
HEAD_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="2F5496")
LABEL_FONT = Font(bold=True)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
MONEY = '"£"#,##0.00'


def load_rows():
    with SRC.open(encoding="utf-8") as fh:
        raw = list(csv.DictReader(fh))
    rows = []
    for r in raw:
        rows.append({
            # les attributs du site contiennent des entités HTML (&#39; pour l'apostrophe) :
            # décodées ici, et volontairement pas dans le fichier brut, pour que le nettoyage
            # reste visible et rejouable — c'est la valeur ajoutée du livrable.
            "titre": unescape(r["titre"]).strip(),
            "prix": float(r["prix_gbp"]),
            "dispo": r["disponibilite"].strip(),
            "note": int(r["note_sur_5"]) if r["note_sur_5"] else None,
            "url": r["url"].strip(),
            "page": int(r["page_source"]),
        })
    return rows


def build_catalogue(wb, rows):
    ws = wb.active
    ws.title = "Catalogue"
    headers = ["Titre", "Prix (GBP)", "Disponibilité", "Note /5", "URL source", "Page"]
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill, cell.font, cell.border = HEAD_FILL, HEAD_FONT, BORDER
        cell.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 22

    for r in rows:
        ws.append([r["titre"], r["prix"], r["dispo"], r["note"], r["url"], r["page"]])

    last = ws.max_row
    for row in ws.iter_rows(min_row=2, max_row=last, max_col=6):
        for cell in row:
            cell.border = BORDER
        row[1].number_format = MONEY                      # prix typé, mis en forme
        row[2].alignment = Alignment(horizontal="center")
        row[3].alignment = Alignment(horizontal="center")
        row[5].alignment = Alignment(horizontal="center")
        row[4].hyperlink = row[4].value                   # URL cliquable
        row[4].font = Font(color="0563C1", underline="single", size=10)

    for col, width in zip("ABCDEF", (46, 12, 16, 9, 58, 7)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:F{last}"
    table = Table(displayName="Catalogue", ref=f"A1:F{last}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
    ws.add_table(table)
    return last


def build_synthese(wb, last):
    ws = wb.create_sheet("Synthèse")
    rng_p = f"Catalogue!B2:B{last}"
    rng_s = f"Catalogue!C2:C{last}"
    rng_n = f"Catalogue!D2:D{last}"

    ws["A1"] = "Synthèse du catalogue"
    ws["A1"].font = TITLE_FONT
    ws["A3"] = "Source"
    ws["B3"] = SOURCE
    ws["A4"] = "Extrait le"
    ws["B4"] = date.today().isoformat()
    ws["A5"] = "Lignes livrées"
    ws["B5"] = f"=COUNTA(Catalogue!A2:A{last})"

    ws["A7"] = "Indicateurs prix (GBP)"
    ws["A7"].font = LABEL_FONT
    stats = [("Minimum", f"=MIN({rng_p})"), ("Maximum", f"=MAX({rng_p})"),
             ("Moyenne", f"=ROUND(AVERAGE({rng_p}),2)"), ("Médiane", f"=MEDIAN({rng_p})"),
             ("Écart-type", f"=ROUND(STDEV({rng_p}),2)")]
    for i, (label, formula) in enumerate(stats, start=8):
        ws[f"A{i}"] = label
        ws[f"B{i}"] = formula
        ws[f"B{i}"].number_format = MONEY

    ws["A14"] = "Disponibilité"
    ws["A14"].font = LABEL_FONT
    ws["A15"] = "En stock"
    ws["B15"] = f'=COUNTIF({rng_s},"In stock")'
    ws["A16"] = "Part en stock"
    ws["B16"] = "=IF(B5=0,0,B15/B5)"
    ws["B16"].number_format = "0.0%"

    ws["A18"] = "Répartition par note"
    ws["A18"].font = LABEL_FONT
    ws["B18"], ws["C18"] = "Titres", "Part"
    for cell in ("B18", "C18"):
        ws[cell].font = LABEL_FONT
    for i, note in enumerate(range(1, 6), start=19):
        ws[f"A{i}"] = f"{note} étoile(s)"
        ws[f"B{i}"] = f"=COUNTIF({rng_n},{note})"
        ws[f"C{i}"] = f"=IF($B$5=0,0,B{i}/$B$5)"
        ws[f"C{i}"].number_format = "0.0%"

    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 10
    ws["B3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[3].height = 30

    ws["A26"] = "Note de méthode"
    ws["A26"].font = LABEL_FONT
    ws["A27"] = ("Extraction des pages publiques, nettoyage des libellés de prix, typage "
                 "numérique des prix et des notes, dédoublonnage des URL. Les cellules de "
                 "cette feuille sont des formules : elles se recalculent à l'ouverture.")
    ws["A27"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A27:C30")


def main():
    rows = load_rows()
    wb = Workbook()
    last = build_catalogue(wb, rows)
    build_synthese(wb, last)
    wb.calculation.fullCalcOnLoad = True     # Excel/LibreOffice recalculent à l'ouverture
    wb.save(OUT)
    prix = [r["prix"] for r in rows]
    print(f"{OUT} écrit : {len(rows)} lignes, 2 feuilles (Catalogue, Synthèse à formules)")
    print(f"  prix  : min {min(prix):.2f} · max {max(prix):.2f} · médiane {statistics.median(prix):.2f}")
    print(f"  stock : {sum(1 for r in rows if r['dispo'] == 'In stock')}/{len(rows)} en stock")
    print(f"  notes : {sorted({r['note'] for r in rows})}")


if __name__ == "__main__":
    main()
