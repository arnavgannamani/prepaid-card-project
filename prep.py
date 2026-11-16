"""Shared data loading and preparation for the prepaid card project.

Everyone imports from here so that every model sees the same rows, the same
20 predictors and the same preparation steps.

    from prep import load_split, build_preprocessor

    X_train, X_test, y_train, y_test = load_split()
    model = make_pipeline(build_preprocessor(), LogisticRegression(class_weight="balanced"))
    model.fit(X_train, y_train)

Put the preprocessor INSIDE the model pipeline, as above. It is then fitted on
training data only, including inside each cross-validation fold, so nothing
about the test set leaks into the model.
"""
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_DIR = Path(__file__).resolve().parent / "data"
TARGET = "PRODUSE_3"
# Kept in train.csv / test.csv for describing groups. Never use these as predictors.
PROFILE_COLUMNS = ["PPETHM", "sample", "PRODUSE_1", "PRODUSE_2", "PRODUSE_4", "PRODUSE_5"]


# Plain-language names for the codes of the three unordered categories (from the CFPB codebook).
CATEGORY_LABELS = {
    "HOUSING": {1: "Owns home", 2: "Rents", 3: "Neither owns nor rents"},
    "EMPLOY": {1: "Self-employed", 2: "Works full-time", 3: "Works part-time", 4: "Homemaker", 5: "Full-time student",
               6: "Sick, disabled or unable to work", 7: "Unemployed or laid off", 8: "Retired"},
    "PPMARIT": {1: "Married", 2: "Widowed", 3: "Divorced / separated", 4: "Never married", 5: "Living with partner"},
}


def feature_table():
    """The 20 selected predictors with their label, theme and how each is prepared."""
    return pd.read_csv(DATA_DIR / "selected_features.csv", index_col="variable")


def feature_lists():
    """Predictor names grouped by the preparation they need: (scaled, binary, nominal)."""
    prep = feature_table()["preparation"]
    scaled = prep.index[prep == "Impute median, standardise"].tolist()
    binary = prep.index[prep == "Impute most frequent, keep as 0/1"].tolist()
    nominal = prep.index[prep == "Impute most frequent, one-hot encode"].tolist()
    assert len(scaled) + len(binary) + len(nominal) == len(prep), "A predictor has no preparation rule"
    return scaled, binary, nominal


def load_split():
    """Return X_train, X_test, y_train, y_test with the 20 selected predictors only."""
    features = feature_table().index.tolist()
    train = pd.read_csv(DATA_DIR / "train.csv", index_col="PUF_ID")
    test = pd.read_csv(DATA_DIR / "test.csv", index_col="PUF_ID")
    return train[features], test[features], train[TARGET].astype(int), test[TARGET].astype(int)


def load_profile():
    """Return (train, test) profiling columns: race/ethnicity, sample type and the other non-bank products."""
    train = pd.read_csv(DATA_DIR / "train.csv", index_col="PUF_ID")
    test = pd.read_csv(DATA_DIR / "test.csv", index_col="PUF_ID")
    return train[PROFILE_COLUMNS], test[PROFILE_COLUMNS]


def build_preprocessor(drop_first=False):
    """Unfitted preparation step for the 20 predictors.

    - ordered scales, counts and scores: fill gaps with the median, then standardise (mean 0, sd 1)
    - yes/no variables: fill gaps with the most frequent value, keep as 0/1
    - unordered categories: fill gaps with the most frequent value, then one-hot encode

    Set drop_first=True for an unpenalised regression, to avoid perfectly collinear dummy columns.
    """
    scaled, binary, nominal = feature_lists()
    encoder = OneHotEncoder(handle_unknown="ignore", drop="first" if drop_first else None, sparse_output=False)
    return ColumnTransformer(
        transformers=[
            ("scaled", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), scaled),
            ("binary", SimpleImputer(strategy="most_frequent"), binary),
            ("nominal", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", encoder)]), nominal),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def readable_names(fitted_preprocessor):
    """Plain-language name for every model column, e.g. 'HOUSING_2.0' becomes 'Housing: Rents'."""
    labels = feature_table()["label"]
    names = []
    for column in fitted_preprocessor.get_feature_names_out():
        variable, _, code = column.rpartition("_")
        if variable in CATEGORY_LABELS and code.replace(".", "", 1).isdigit():
            names.append(f"{labels[variable]}: {CATEGORY_LABELS[variable][int(float(code))]}")
        else:
            names.append(labels.get(column, column))
    return names
