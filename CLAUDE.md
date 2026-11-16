# Project guide for Claude

This file is loaded automatically by Claude Code. It tells you what the project is and what is already done. **All four tasks are complete and merged; only the final integration remains.** The task briefs further down are kept for reference.

If the person has not said which member they are, ask once, then proceed.

## The project

Mini-Project 2 for a machine learning course: **prepaid card marketing**, using the CFPB National Financial Well-Being Survey.

The brief:
- Outcome variable is `PRODUSE_3` (used a reloadable prepaid card not linked to a checking or savings account).
- Select up to 20 predictors. Ignore survey weights. Standardize as necessary.
- Use three predictive models from: Random Forest, SVM, AdaBoost, Logit, XGBoost, ANN. Assess them and choose one.
- Answer two business questions with the chosen model:
  - **Card company:** who to target; a marketing and origination strategy; key insights on usage likelihood.
  - **CFPB:** given high fees and unsophisticated users, which groups are at risk, and what policies would protect them.

The audience is course leadership. Work must be thorough, correct and readable by a non-specialist.

## Who owns what

| Member | Task | Notebook | Status |
|---|---|---|---|
| Arnav (Member 1) | Part 1: load, clean, explore | `prepaid_card_analysis.ipynb` | Done |
| Arnav (Member 1) | Task A: predictors and data prep | `02_features_and_prep.ipynb` | Done |
| Jairaj (Member 2) | Task B: models and evaluation | `03_models.ipynb` | Done |
| Ethan (Member 3) | Task C: card company answer | `04_card_company.ipynb` | Done |
| Ani (Member 4) | Task D: CFPB answer and wrap-up | `05_cfpb.ipynb` | Done |
| Arnav (Member 1) | Final integration and review | all | Last |

`LAUNCH_PLAN.md` has the same plan for humans.

## What already exists

Read these before starting any task. Do not redo them.

- `prepaid_card_analysis.ipynb` — Part 1. Data verified against the CFPB codebook, cleaned, explored. Read its summary and Section 4 takeaways.
- `02_features_and_prep.ipynb` — Task A. The train/test split, the 17 predictors with reasons, validation, and the preparation pipeline. Read its summary and Section 7.
- `prep.py` — the shared interface. Always load data through it:
  - `load_split()` returns `X_train, X_test, y_train, y_test` (the 17 selected predictors only).
  - `build_preprocessor()` returns the unfitted preparation step (impute, one-hot, standardize).
  - `load_profile()` returns `(train, test)` profiling columns: `PPETHM` (race/ethnicity), `sample`, `PRODUSE_1/2/4/5`.
  - `readable_names(fitted_preprocessor)` gives plain-language names for the 26 model columns.
  - `feature_table()` returns `data/selected_features.csv` as a table.
- `03_models.ipynb` — Task B. Three tuned models, the choice, the threshold and the test-set evaluation. Read its summary and Sections 8–9.
- `data/test_scores.csv` and `data/train_oof_scores.csv` — model scores per respondent (`score_chosen` is the one to use). The training file holds out-of-fold scores, so it is safe for profiling.
- `models/chosen_model.joblib` — the chosen pipeline fitted on the training set. It needs scikit-learn 1.9.1 to load; if it fails, refit it (see the model facts below).
- `04_card_company.ipynb` — Task C. Model weights as odds ratios, target segments, reachability with observable data, strategy, and who the rule reaches by race/ethnicity. Read its summary and Sections 2, 5 and 6.
- `05_cfpb.ipynb` — Task D. The at-risk definition and groups, the knowledge and confidence gap, the fairness audit, policies, and the project's conclusions and limitations.
- `data/train.csv` (5,093 rows), `data/test.csv` (1,274 rows), indexed by `PUF_ID`. Besides the predictors they hold describe-only columns: race/ethnicity, sample, the other non-bank products, and age, marital status and SNAP.
- `data/selected_features.csv` — the 17 predictors: label, theme, preparation, why selected, and `available_to_card_company` (the team's judgement on what a company could know about a prospect).
- `data/cfpb_clean.csv` — all 204 cleaned columns for every respondent. Join on `PUF_ID` if you need a variable outside the 17.
- `data/variable_roles.csv` — label, theme, type and role of every cleaned column.
- `docs/cfpb_nfwbs-puf-codebook.pdf` — the official codebook. Use it for value labels; do not guess what a code means.

Key facts established so far:
- 6,367 respondents after cleaning; 8.8% are prepaid users (about 1 to 10).
- Use rises with financial fragility (low income, no savings, hardship, no bank account) and with low financial knowledge. Most users are still mainstream: 68% have a bank account.
- **Predictors:** 17, chosen from 173 eligible variables. The brief allows up to 20. Age, marital status, sex and SNAP receipt are **not eligible** because they are protected categories under fair-lending law (ECOA); race/ethnicity and the other non-bank products (`PRODUSE_1/2/4/5`) are also excluded. Removing age, marital status and SNAP from the original 20 cost no accuracy. All of these remain available for describing groups, never for predicting.
- No single strong predictor. An untuned class-weighted logistic regression on the 17 predictors scores cross-validated ROC-AUC 0.729 and PR-AUC 0.224.
- **Chosen model (Task B):** class-weighted logistic regression, `C=0.3`. Random forest and XGBoost were statistically tied with it. Test ROC-AUC 0.746, PR-AUC 0.247.
- **Recommended rule:** flag the top 20% of scores, which is `score_chosen >= 0.602` (cut-off fixed on training scores). On the test set this flags 246 of 1,274 people, catches 60 of 112 users (53.6%), and 24.4% of those flagged are users (2.77 times the average). On training out-of-fold scores recall is 48.7% and lift 2.43, so plan on about half of users.
- **Scores are rankings, not probabilities** (class weights inflate them). Compare people by score rank or by actual usage rate within score groups.
- **Task C findings:** the largest model weights are bank-account status (odds ratio 0.58), debt-collector contact (1.47), credit rejection (1.30) and renting (1.63 against owning). Savings, ability to raise \$2,000, well-being and the hardship count carry almost no weight *inside the model*, although each is strongly related to prepaid use on its own; do not describe them as model drivers. Among people flagged (training set), 72.6% report a material hardship and 61.0% have under \$1,000 saved. 69.2% of all users have a bank account, and the users the rule misses are 89.1% banked.
- **Task D findings:** 996 people (19.6% of the training set) are at risk, meaning likely to use a card and vulnerable on at least two of five markers; they include 62.9% of all users. 90.3% of the people the rule flags are vulnerable. The rule flags Black and Hispanic respondents about three times as often as White respondents, and women more often than men with equal usage, although neither race nor sex is a predictor.
- **These figures replace the earlier 20-predictor results.** If a number here disagrees with a notebook, the notebook is right. The task briefs below still quote some 20-predictor figures (for example a baseline of 0.728 and a cut-off of 0.600); treat those as historical.

## Rules for every task

**Data and modelling**
1. Load data with `prep.load_split()`. Never re-split, re-clean or re-select predictors.
2. Put `build_preprocessor()` inside the model pipeline, so it is refitted in every cross-validation fold.
3. Tune and compare on the training set by cross-validation (`StratifiedKFold(5, shuffle=True, random_state=42)`). Use the test set once, at the end, to report final numbers.
4. Handle the class imbalance (class weights or equivalent). Report recall, precision, PR-AUC, ROC-AUC and lift. Never judge a model on accuracy alone: predicting "no one" scores 91%.
5. Never use profiling columns, `PRODUSE_6`, `sample`, `finalwt` or anything from `load_profile()` as a predictor.
6. Use `random_state=42` everywhere so results are reproducible.
7. Describe findings as associations. Do not claim a characteristic causes prepaid card use.

**Notebooks**
1. One notebook per task, named as in the table above. Do not edit another member's notebook or `prep.py`; if `prep.py` needs a change, tell the user to raise it with Arnav.
2. Follow the style of the existing notebooks: a summary at the top, numbered sections, a short markdown explanation before each code cell, and a "Takeaways" cell after each result with the actual numbers.
3. Every number written in markdown must match the notebook's output. Run the notebook top to bottom (Restart and Run All) and check before finishing.
4. Escape dollar signs in markdown as `\$`, or Jupyter renders them as maths.
5. Do not use `DataFrame.style` (it needs `jinja2`, which may not be installed). Copy the `fmt()` helper from `02_features_and_prep.ipynb`.
6. Reuse the chart style (colours and `rcParams`) from the setup cell of `02_features_and_prep.ipynb`. Save charts to `figures/` continuing the numbering (next is `15_...`). One measure per axis, no dual axes, label values directly.
7. Write for a non-specialist: define a metric the first time it appears, and say what each result means for the business question.

**Git**
1. Work on your own branch: `task-b-models`, `task-c-card-company` or `task-d-cfpb`. Do not commit to `main` directly.
2. Commit messages are plain. **Do not add Claude as a co-author or contributor** (no `Co-Authored-By` line, no "Generated with" line). This is the repository owner's rule.
3. Push the branch and open a pull request into `main` only when the user asks.
4. Pull `main` before starting, so you have the latest shared files.

**Setup**
- Install packages with `pip install -r requirements.txt`. If XGBoost will not install, use AdaBoost in its place and say so.

## Task B — Models and evaluation (Member 2) — DONE

This task is complete and merged. The brief is kept for reference. Do not redo it; if asked to change it, confirm with the user first.

**Goal.** Build three models, compare them fairly, choose one, and hand its predictions to Tasks C and D.

**Deliver** `03_models.ipynb` containing:
1. **Setup:** load with `prep.load_split()`; state the baseline to beat (ROC-AUC 0.728, PR-AUC 0.227).
2. **Three models**, each as a pipeline of `build_preprocessor()` plus the estimator. Default choice: Logistic Regression, Random Forest, XGBoost. All must come from the brief's list.
3. **Tuning:** a modest hyperparameter search per model by cross-validation on the training set, scored on PR-AUC. Show the grid, the best settings and the cross-validated scores with their fold-to-fold spread.
4. **Comparison on cross-validation:** ROC-AUC, PR-AUC, and recall and precision at a stated threshold, in one table and one chart. Say whether the differences are larger than the fold-to-fold noise.
5. **Choose one model** and justify it on performance, stability and interpretability (Tasks C and D must be able to explain it). If models are statistically tied, prefer the more interpretable one and say so.
6. **Final test-set evaluation**, once, for all three models: ROC-AUC, PR-AUC, confusion matrix at the chosen threshold, ROC and precision-recall curves, and a lift table by decile (share of all users captured in the top 10%, 20%, 30% of scores).
7. **Threshold:** explain the trade-off between recall and precision and recommend a threshold or a "top X%" rule.
8. **Honest reading:** expected performance is moderate. Say plainly what the model can and cannot do.

**Hand-off files**
- `data/test_scores.csv`: `PUF_ID`, `PRODUSE_3`, one score column per model (`score_logit`, `score_rf`, `score_xgb`), and `score_chosen`.
- `data/train_oof_scores.csv`: the same columns for the training set, using out-of-fold predictions (`cross_val_predict`), so Tasks C and D can profile 5,093 people without leakage.
- `models/chosen_model.joblib`: the chosen pipeline fitted on the full training set.
- Record the chosen model's name and threshold in a short table at the end of the notebook.

**Notes**
- Class-weighted models give scores that rank people correctly but are not true probabilities. Say this, and treat scores as rankings unless you calibrate them.
- Update `requirements.txt` if you add a package.

**Done when** the notebook runs top to bottom with no errors, the three hand-off files exist, and the test set was used only in the final evaluation section.

## Task C — Card company answer (Member 3) — DONE

This task is complete and merged. The brief is kept for reference. Do not redo it; if asked to change it, confirm with the user first.

**Goal.** Answer: "Can I establish a marketing and origination strategy around who to target for this product? Draw any key insights related to usage likelihood of prepaid cards."

**Inputs are ready.** Task B is merged: use `data/test_scores.csv`, `data/train_oof_scores.csv` and the chosen model. If those files are missing, tell the user to run `git pull`.

**Note on reading the weights.** The saved model keeps every category of housing, employment and marital status (no reference category), so a weight such as "Widowed +0.37" is not measured against a baseline group. For odds ratios, refit the same model with `build_preprocessor(drop_first=True)` on the training set and say which category is the reference; confirm its scores rank people the same way as `score_chosen`.

**Deliver** `04_card_company.ipynb` containing:
1. **What drives the score:** interpret the chosen model (coefficients or odds ratios for Logit; permutation importance and partial dependence for tree models). Use `readable_names()` for labels. Treat savings, ability to raise \$2,000 and the well-being score as one "liquidity" group; they overlap.
2. **Target segments:** profile the highest-scoring groups using `data/train_oof_scores.csv` and confirm on `data/test_scores.csv`. For each segment give its size, its actual usage rate and its lift over the 8.8% base rate.
3. **Reachability:** separate predictors a company can observe from survey-only ones (`available_to_card_company`). Build the targeting rules from observable variables, and show how much lift survives when only those are used.
4. **Strategy:** who to target, through which channels, with what message, and what origination criteria. Size the opportunity (for example, the top 20% of scores contains X% of users).
5. **Key insights**, including that most users are banked and mainstream, so "the unbanked" is only part of the market.
6. **Responsible marketing:** race/ethnicity is not a targeting variable. Note the overlap between the best prospects and the financially fragile groups in Task D, and what that implies for fees and disclosure.

**Done when** every recommendation is tied to a number in the notebook, and the notebook runs top to bottom.

## Task D — CFPB answer and wrap-up (Member 4) — DONE

This task is complete and merged. The brief is kept for reference. Do not redo it; if asked to change it, confirm with the user first.

**Goal.** Answer: "Given potential high fees, and concerns related to unsophisticated users, can we identify at-risk groups? What policies can we prescribe to protect such groups?" Then write the project's conclusions.

**Inputs are ready.** Task B is merged: use `data/test_scores.csv`, `data/train_oof_scores.csv` and the chosen model. If those files are missing, tell the user to run `git pull`.

**Lead for the fairness check.** `04_card_company.ipynb` Section 6 shows the top-20% rule flags 43.8% of Black and 38.5% of Hispanic respondents against 12.9% of White respondents in the training set (49.7%, 31.9% and 12.0% in the test set), even though race is not a predictor. Usage rates are 18.3%, 14.7% and 6.2%, and flagged Black and Hispanic respondents are more often actual users than flagged White respondents. Build on that table instead of repeating it: take it further (for example by knowledge level, fees exposure or hardship within each group) and report it plainly.

**Deliver** `05_cfpb.ipynb` containing:
1. **Define "at risk"** explicitly: likely to use a prepaid card (high model score, or an actual user) **and** vulnerable to fees or poor decisions (low financial knowledge, low income, no savings, material hardship, no bank account). Justify each criterion.
2. **Size and profile the at-risk groups:** how many people, their usage rate, and their demographics. Use `load_profile()` to describe them by race/ethnicity and join `data/cfpb_clean.csv` on `PUF_ID` for other variables.
3. **The knowledge and confidence gap:** users know measurably less (`KHscore`, `LMscore`) but rate their own skill almost as highly (`FSscore`, `SUBKNOWL1`). Quantify it; it is the core of the "unsophisticated user" concern.
4. **Fairness check on the model:** compare score distributions and "targeted" rates across race/ethnicity groups even though race is not a predictor. Report any disparity plainly.
5. **Policies:** propose specific protections (for example fee disclosure, fee caps, financial education, access to low-cost bank accounts) and tie each one to the evidence for the group it protects. Separate what the data supports from what is a reasoned suggestion.
6. **Conclusions and limitations for the whole project:** self-reported 2016 survey; the outcome records use, not fees paid or frequency; unweighted results are not national estimates; associations are not causes; model performance is moderate.

**Done when** each at-risk group has a size and a rate, each policy cites evidence, and the notebook runs top to bottom.

## Final integration (Arnav)

After Tasks B–D are merged: run all five notebooks in order, check that shared numbers agree across them (base rate, sample sizes, chosen model, headline lifts), update `README.md` and `LAUNCH_PLAN.md`, and confirm every requirement in the brief is met.
