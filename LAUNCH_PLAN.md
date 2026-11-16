# Launch plan — Mini-Project 2

Part 1 (load, clean, explore) and Task A (predictors and data prep) are done. This plan covers everything left and who owns it.

**Using Claude Code?** Open this folder in Claude Code and say "do the task for Member 2" (or 3, or 4). `CLAUDE.md` tells it the project, the rules and your task.

Names below are placeholders. Replace "Member 2–4" with real names.

## Who does what

| Owner | Task | Delivers | Depends on |
|---|---|---|---|
| **Arnav** | **A. Predictors and data prep** (Steps 5–6), then final integration | `02_features_and_prep.ipynb`, `prep.py`, `data/train.csv`, `data/test.csv`, `data/selected_features.csv` | **Done** |
| **Member 2** | **B. Models and evaluation** (Steps 7–8) | `03_models.ipynb`, `data/test_scores.csv`, the chosen model | Task A |
| **Member 3** | **C. Card company answer** (Steps 9–10) | `04_card_company.ipynb`, target segments, marketing and origination strategy | Task B for final numbers |
| **Member 4** | **D. CFPB answer and wrap-up** (Steps 11–12) | `05_cfpb.ipynb`, at-risk groups, policy recommendations, conclusions and limitations | Task B for final numbers |

## Task details

### A. Predictors and data prep — Arnav
- Choose up to 20 predictors from the 178 candidates in `data/variable_roles.csv`.
- Take one variable per correlated cluster (Part 1, Section 4.7) and cover resources, strain, knowledge, banking and demographics.
- Make a stratified train/test split and save both halves so everyone uses the same rows.
- Build one preparation pipeline: impute, one-hot encode the unordered categories, standardize. Fit it on training data only.
- At the end: merge everyone's work, check the notebooks run top to bottom, and check the numbers agree across sections.

### B. Models and evaluation — Member 2
- Fit three models on the shared training set. Proposed: Logit, Random Forest, XGBoost (swap in AdaBoost if XGBoost is a problem to install).
- Tune each with cross-validation and weight the classes for the 1-to-10 imbalance.
- Compare on the test set using recall, precision, precision-recall AUC, ROC-AUC and lift by decile. Do not use accuracy alone: predicting "no one" scores 91%.
- Pick one model, justify it, and save each test respondent's predicted probability to `data/test_scores.csv` for Tasks C and D.

### C. Card company answer — Member 3
- Interpret the chosen model: which predictors matter and in which direction.
- Define target segments from the highest-scoring groups and size them (how many people, what usage rate, what lift over 8.8%).
- Turn that into a marketing and origination strategy: who to target, through what channel, with what message.
- Note that 68% of users already have a bank account, so "the unbanked" is not the whole market.

### D. CFPB answer and wrap-up — Member 4
- Identify at-risk groups: high predicted use combined with low financial knowledge, low income, no savings or no bank account.
- Use the knowledge-versus-confidence gap from Part 1, Section 4.4 (users know less but rate their skills almost as highly).
- Propose policies to protect those groups, such as fee disclosure, fee caps or financial education, and tie each to the evidence.
- Write the overall conclusions and limitations.

## Order of work

1. **Done:** Task A.
2. **Now:** Member 2 builds and compares the models. Members 3 and 4 start drafting from the Part 1 findings (segments, at-risk groups, policy research) so they are not waiting.
3. **When Task B lands:** Members 3 and 4 swap in the final model numbers.
4. **Last:** Arnav integrates, everyone reviews the whole thing once.

## Working in GitHub

- Clone the repo, then work on your own branch: `git checkout -b task-b-models` (or `task-c`, `task-d`).
- Each task has its **own notebook file**. Do not edit someone else's notebook; two people editing one notebook causes merge conflicts that are painful to fix.
- Load the shared files from `data/`. Do not re-clean or re-split the data yourself.
- When your part works, push your branch and open a pull request into `main`. One other person reads it before it is merged.

## Decide as a group first

1. **Deadline**, and a date for each hand-off above.
2. **Final deliverable:** notebooks only, or slides or a report as well? If slides are needed, assign an owner.
3. **Other alternative-finance items** (`PRODUSE_1`, `2`, `4`, `5`) and **race/ethnicity** are left out as predictors in Task A. Testing showed neither improves accuracy. Both stay available for describing groups. Say so if you disagree.
4. **The three models:** confirm Logit, Random Forest and XGBoost.
