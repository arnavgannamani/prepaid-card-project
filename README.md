# Prepaid Card Marketing — Mini-Project 2

Which consumers are more likely to use a prepaid card? The analysis uses the CFPB National Financial Well-Being Survey to answer two questions:

- **Card company:** who to target, and what a marketing and origination strategy should look like.
- **CFPB:** which groups are at risk, and what policies would protect them.

## Status

| Part | Steps | Status |
|---|---|---|
| 1. Data foundation | Load, understand, clean, explore | Done |
| 2. Modelling | Select predictors, prepare data, build and compare three models | To do |
| 3. Business answers | Card company strategy, CFPB at-risk groups and policy | To do |

## How to run

1. Install the packages: `pip install -r requirements.txt`
2. Open `prepaid_card_analysis.ipynb` from this folder and run all cells.

The notebook reads from `data/` using relative paths, so it must be run from the project folder. All outputs and charts are already saved inside the notebook if you only want to read it.

## Contents

| Path | What it is |
|---|---|
| `prepaid_card_analysis.ipynb` | Part 1 notebook: load, understand, clean, explore |
| `data/CFPB-financial-wellness-data.csv` | Survey data as supplied (6,394 respondents, 217 variables) |
| `data/codebook_reference.csv` | Variable labels and published summary statistics from the CFPB codebook |
| `data/cfpb_clean.csv` | Cleaned data produced by the notebook (6,367 respondents, 204 columns) |
| `data/variable_roles.csv` | Label, group, measurement type, role and missing rate for every cleaned column |
| `figures/` | The notebook's 11 charts as PNG files |
| `docs/cfpb_nfwbs-puf-codebook.pdf` | Official CFPB codebook |

## Notes

- The outcome variable is `PRODUSE_3` (used a reloadable prepaid card not linked to a checking or savings account).
- Survey weights are ignored for the analysis, as the project brief requires. Figures describe this sample and are not national estimates.
- Data source: CFPB National Financial Well-Being Survey, Public Use File.
