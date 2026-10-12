# Rapport de livraison — extraction PDF vers tableur

- **Source** : `demo-livres.pdf` (100 lignes attendues)
- **Livré** : `demo-depuis-pdf.csv` — 100 lignes × 6 colonnes
- **Extrait le** : 2026-10-12

## Contrôle qualité

| Contrôle | Résultat |
|---|---|
| Lignes récupérées | 100 / 100 |
| Titres identiques à la source | 90 / 100 |
| Prix conformes à la source | 90 / 90 comparables |
| Titres rognés dans le PDF source | 10 |

## Points à connaître

Les 10 titres ci-dessous dépassent la largeur de colonne de la mise en page d'origine :
**le PDF les a coupés**, l'information est perdue dans le fichier source lui-même. Elle a été
signalée et non inventée.

- `The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhul…`
- `The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Oly…`
- `Foolproof Preserving: A Guide to Small Batch Jams, Jellies, Pickles, Condiments, and More:…`
- `America's Cradle of Quarterbacks: Western Pennsylvania's Football Factory from Johnny Un…`
- `Unseen City: The Majesty of Pigeons, the Discreet Charm of Snails & Other Wonders of the…`
- `Unbound: How Eight Technologies Made Us Human, Transformed Society, and Brought Our…`
- `The Pioneer Woman Cooks: Dinnertime: Comfort Classics, Freezer Food, 16-Minute Meals,…`
- `The Mindfulness and Acceptance Workbook for Anxiety: A Guide to Breaking Free from An…`
- `The Bulletproof Diet: Lose up to a Pound a Day, Reclaim Energy and Focus, Upgrade Your…`
- `Political Suicide: Missteps, Peccadilloes, Bad Calls, Backroom Hijinx, Sordid Pasts, Rotten…`
