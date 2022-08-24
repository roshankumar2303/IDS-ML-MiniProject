import sys, os

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.build_features import (
    select_k_best_features,
    recursive_feature_elimination,
)


# Ask User to choose a Selector for Feature Selection
def choose_feature_selector():
    while True:
        print("\nCHOOSE A SELECTOR FOR FEATURE SELECTION:\n")
        print("1. Select K Best")
        print("2. Recursive Feature Elimination with Decision Tree as Estimator")
        print("\nEnter Your Choice:", end=" ")
        choice = int(input())

        if choice == 1:
            name = "skb"
            print("\nSELECTOR CHOSEN FOR FEATURE SELECTION - {}".format(name))
            return name, select_k_best_features
        if choice == 2:
            name = "rfe"
            print("\nSELECTOR CHOSEN FOR FEATURE SELECTION - {}".format(name))
            return name, recursive_feature_elimination


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
