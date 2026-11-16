# Prepaid Card Marketing — Mini-Project 2

Which consumers are more likely to use a prepaid card? The analysis uses the CFPB National Financial Well-Being Survey to answer two questions:

- **Card company:** who to target, and what a marketing and origination strategy should look like.
- **CFPB:** which groups are at risk, and what policies would protect them.

## Status

| Part | Steps | Status |
|---|---|---|
| 1. Data foundation | Load, understand, clean, explore | Done |
| 2. Predictors and data prep | Train/test split, 20 predictors, preparation pipeline | Done |
| 3. Models | Build and compare three models, choose one | Done (logistic regression chosen) |
| 4. Card company answer | Target segments, marketing and origination strategy | Done |
| 5. CFPB answer | At-risk groups, policy recommendations, conclusions | To do |

See `LAUNCH_PLAN.md` for who owns what. If you use Claude Code, `CLAUDE.md` briefs it on the project and each task.

## How to run

1. Install the packages: `pip install -r requirements.txt`
2. Open the notebooks from this folder and run them in order: `prepaid_card_analysis.ipynb`, `02_features_and_prep.ipynb`, `03_models.ipynb`, then `04_card_company.ipynb`.

The notebook reads from `data/` using relative paths, so it must be run from the project folder. All outputs and charts are already saved inside the notebook if you only want to read it.

## Contents

| Path | What it is |
|---|---|
| `prepaid_card_analysis.ipynb` | Part 1 notebook: load, understand, clean, explore |
| `data/CFPB-financial-wellness-data.csv` | Survey data as supplied (6,394 respondents, 217 variables) |
| `data/codebook_reference.csv` | Variable labels and published summary statistics from the CFPB codebook |
| `data/cfpb_clean.csv` | Cleaned data produced by the notebook (6,367 respondents, 204 columns) |
| `data/variable_roles.csv` | Label, group, measurement type, role and missing rate for every cleaned column |
| `02_features_and_prep.ipynb` | Part 2 notebook: train/test split, selection of 20 predictors, preparation pipeline |
| `prep.py` | Shared functions: `load_split()`, `build_preprocessor()`, `load_profile()` |
| `data/train.csv`, `data/test.csv` | The fixed 80/20 split (5,093 and 1,274 respondents) |
| `data/selected_features.csv` | The 20 predictors with labels, preparation rules and reasons |
| `03_models.ipynb` | Part 3 notebook: three models tuned and compared, one chosen, final test-set evaluation |
| `data/test_scores.csv`, `data/train_oof_scores.csv` | Model scores for the test set and (out-of-fold) the training set |
| `models/chosen_model.joblib` | The chosen model, fitted on the training set (needs scikit-learn 1.9.1 to load) |
| `04_card_company.ipynb` | Part 4 notebook: what drives the score, target segments, reachability, marketing and origination strategy |
| `LAUNCH_PLAN.md` | Task assignments and order of work |
| `CLAUDE.md` | Project guide and task briefs for Claude Code |
| `figures/` | The notebooks' charts as PNG files |
| `docs/cfpb_nfwbs-puf-codebook.pdf` | Official CFPB codebook |

## Notes

- The outcome variable is `PRODUSE_3` (used a reloadable prepaid card not linked to a checking or savings account).
- Survey weights are ignored for the analysis, as the project brief requires. Figures describe this sample and are not national estimates.
- Data source: CFPB National Financial Well-Being Survey, Public Use File.
