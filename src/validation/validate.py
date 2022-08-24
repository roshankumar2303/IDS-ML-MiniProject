import sys, os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.build_features import build_features
from src.features.clean_data import clean_data


# Read the Interim Training Set
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
training_set = pd.read_csv(training_set_path, low_memory=False)

# Split training set into (X) and (Y)
xc, yc = training_set.shape
X = training_set.iloc[:, 0 : yc - 1]
Y = training_set.iloc[:, yc - 1]

# Cross Validation - Stratified K fold
skf = StratifiedKFold(n_splits=5)

# Classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn_scores = []
knn_best_features = {}

# Splitting into 5 folds + Feature Selection + Validation
iter_count = 1
for train_idx, test_idx in skf.split(X, Y):
    print("\nSTRATIFIED K FOLD - ITERATION {}".format(iter_count))

    # Get Training fold (4/5 folds) and Testing fold (1/5 folds)
    train_X_fold = pd.DataFrame(X.iloc[train_idx])
    train_Y_fold = pd.DataFrame(Y.iloc[train_idx])
    test_X_fold = pd.DataFrame(X.iloc[test_idx])
    test_Y_fold = pd.DataFrame(Y.iloc[test_idx])

    # Clean data and Build features for the Training Fold
    print("Building features for Training fold...")
    feature_list, train_X_fold, train_Y_fold = build_features(
        train_X_fold, train_Y_fold
    )
    for ft in feature_list:
        if ft in knn_best_features:
            knn_best_features[ft] += 1
        else:
            knn_best_features[ft] = 1

    # Train Model using the Classifier
    print("Training the model using Training Fold...")
    knn.fit(train_X_fold, np.ravel(train_Y_fold))

    # Clean data and drop unwanted features of the Testing fold
    test_X_fold, test_Y_fold = clean_data(test_X_fold, test_Y_fold)
    for column in test_X_fold:
        if column not in feature_list:
            test_X_fold.drop(columns=column, inplace=True)

    # Get the model score
    print("Calculating scores using the Training and Testing Folds...")
    knn_scores.append(knn.score(test_X_fold, np.ravel(test_Y_fold)))

    # Increase Iteration Count
    iter_count += 1

# Dump all the list of features selected into a JSON file
knn_features_path = (Path.cwd() / "data/processed/knn_features.json").resolve()
with open(knn_features_path, "w") as json_file:
    json.dump(knn_best_features, json_file)

print("\nACCURACY SCORES:", knn_scores)

# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
