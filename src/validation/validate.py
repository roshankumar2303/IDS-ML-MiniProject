import sys, os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import StratifiedKFold

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.build_features import build_features
from src.features.clean_data import clean_data
from src.model.select_classifier import select_classifier


# Read the Interim Training Set
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
training_set = pd.read_csv(training_set_path, low_memory=False)

# Split training set into (X) and (Y)
xc, yc = training_set.shape
X = training_set.iloc[:, 0 : yc - 1]
Y = training_set.iloc[:, yc - 1]

# Cross Validation - Stratified K fold
skf = StratifiedKFold(n_splits=5)

# Choosing Classifier for Cross Validation
classifier_name, classifier = select_classifier()
classifier_scores = []
classifier_best_features = {}
print("\n{}".format(classifier_name))

# Splitting into 5 folds + Feature Selection for Training Fold + Validation
iter_count = 1
for train_idx, val_idx in skf.split(X, Y):
    print("\nSTRATIFIED K FOLD - ITERATION {}".format(iter_count))

    # Get Training fold (4/5 folds) and Validation fold (1/5 folds)
    train_X_fold = pd.DataFrame(X.iloc[train_idx])
    train_Y_fold = pd.DataFrame(Y.iloc[train_idx])
    val_X_fold = pd.DataFrame(X.iloc[val_idx])
    val_Y_fold = pd.DataFrame(Y.iloc[val_idx])

    # Clean data and Build features for the Training Fold
    print("Building features for Training fold...")
    feature_list, train_X_fold, train_Y_fold = build_features(
        train_X_fold, train_Y_fold
    )
    for ft in feature_list:
        if ft in classifier_best_features:
            classifier_best_features[ft] += 1
        else:
            classifier_best_features[ft] = 1

    # Train Model using the Classifier
    print("Training the model using Training Fold...")
    classifier.fit(train_X_fold, np.ravel(train_Y_fold))

    # Clean data and drop unwanted features from Validation fold
    val_X_fold, val_Y_fold = clean_data(val_X_fold, val_Y_fold)
    for column in val_X_fold:
        if column not in feature_list:
            val_X_fold.drop(columns=column, inplace=True)

    # Get the model score
    print("Getting Model Scores...")
    classifier_scores.append(classifier.score(val_X_fold, np.ravel(val_Y_fold)))

    # Increase Iteration Count
    iter_count += 1

# Dump the list of selected features into a JSON file
classifier_features_path = (
    Path.cwd() / "reports/{}_BEST_FEATURES.json".format(classifier_name)
).resolve()
with open(classifier_features_path, "w") as json_file:
    json.dump(classifier_best_features, json_file)

print("\nACCURACY SCORES of {}:".format(classifier_name), classifier_scores)

# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
