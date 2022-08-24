import sys, os
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.clean_data import clean_data


def build_features(X: pd.DataFrame, Y: pd.DataFrame):
    X, Y = clean_data(X, Y)

    # Feature selection using SelectKBest
    k_best = SelectKBest(score_func=chi2, k=50)
    k_best.fit(X, Y)
    features_list = list(X.columns[k_best.get_support()])
    for column in X:
        if column not in features_list:
            X.drop(columns=column, inplace=True)

    # Returning the list of features, modified X and Y sets
    return features_list, X, Y


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
