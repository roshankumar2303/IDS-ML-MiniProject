import sys, os
import pandas as pd

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------


def clean_data(X: pd.DataFrame, Y: pd.DataFrame):
    # Filling the missing values
    X.fillna(method="ffill", inplace=True)

    # Returning the modified X and Y sets
    return X, Y


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
