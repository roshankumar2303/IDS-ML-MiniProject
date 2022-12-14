import sys, os
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.clean_data import clean_data


def select_k_best_features(X: pd.DataFrame, Y: pd.DataFrame):
    # Cleaning the Data
    X, Y = clean_data(X, Y)

    # Feature selection using SelectKBest
    k_best = SelectKBest(score_func=f_classif, k=50)
    k_best.fit(X, np.ravel(Y))
    features_list = list(X.columns[k_best.get_support()])
    for column in X:
        if column not in features_list:
            X.drop(columns=column, inplace=True)

    # Returning the list of features, modified X and Y sets
    return features_list, X, Y


def recursive_feature_elimination(X: pd.DataFrame, Y: pd.DataFrame):
    # Cleaning the Data
    X, Y = clean_data(X, Y)

    # Feature selection using RFE with Decision Tree as estimator
    rfe_selector = RFE(
        estimator=DecisionTreeClassifier(), n_features_to_select=50, step=1
    )
    rfe_selector.fit(X, np.ravel(Y))
    features_list = list(X.columns[rfe_selector.get_support()])
    for column in X:
        if column not in features_list:
            X.drop(columns=column, inplace=True)

    # Returning the list of features, modified X and Y sets
    return features_list, X, Y


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
