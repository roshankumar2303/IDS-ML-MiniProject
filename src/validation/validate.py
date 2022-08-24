import sys, os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    precision_recall_fscore_support,
    confusion_matrix,
)

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.build_features import select_k_best_features
from src.features.clean_data import clean_data
from src.model.select_classifier import select_classifier


# Read the Interim Training Set
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
training_set = pd.read_csv(training_set_path, low_memory=False)

# Split training set into (X) and (Y)
xc, yc = training_set.shape
X = training_set.iloc[:, 0 : yc - 1]
Y = training_set.iloc[:, yc - 1]

# CROSS VALIDATION - STRATIFIED K-FOLD - (k = 5)
skf = StratifiedKFold(n_splits=5)
report = {
    "clf_name": "",
    "clf_precision": [],
    "clf_recall": [],
    "clf_fbeta": [],
    "clf_support": [],
    "clf_confusion_matrix": [],
    "clf_features": {},
}

# Choosing Classifier for Cross Validation
report["clf_name"], classifier = select_classifier()

# K-ITERATIONS OF STRATIFIED K-FOLD CROSS VALIDATION
iter_count = 1
for train_idx, val_idx in skf.split(X, Y):
    print("\nSTRATIFIED K FOLD - ITERATION {}".format(iter_count))

    # Get Training fold (4/5 folds) (X, Y) and Validation fold (1/5 folds) (X, Y)
    train_X_fold = pd.DataFrame(X.iloc[train_idx])
    train_Y_fold = pd.DataFrame(Y.iloc[train_idx])
    val_X_fold = pd.DataFrame(X.iloc[val_idx])
    val_Y_fold = pd.DataFrame(Y.iloc[val_idx])

    # Clean data and perform feature selection on Training-X data
    print("Performing feature selection on training data...")
    features, train_X_fold, train_Y_fold = select_k_best_features(train_X_fold, train_Y_fold)
    for feature in features:
        if feature in report["clf_features"]:
            report["clf_features"][feature] += 1
        else:
            report["clf_features"][feature] = 1

    # Train the model with the Training-X data
    print("Training the model...")
    classifier.fit(train_X_fold, np.ravel(train_Y_fold))

    # Clean data and drop unwanted features from Validation-X data
    val_X_fold, val_Y_fold = clean_data(val_X_fold, val_Y_fold)
    for column in val_X_fold:
        if column not in features:
            val_X_fold.drop(columns=column, inplace=True)

    # Predict-Y using Validation-X
    pred_Y_fold = classifier.predict(val_X_fold)

    # Generate model metrics
    print("Generating model metrics...")
    precision, recall, fbeta, support = precision_recall_fscore_support(
        val_Y_fold, pred_Y_fold, average="weighted", zero_division=0
    )
    c_mat = confusion_matrix(val_Y_fold, pred_Y_fold).tolist()
    report["clf_precision"].append(precision)
    report["clf_recall"].append(recall)
    report["clf_fbeta"].append(fbeta)
    report["clf_support"].append(support)
    report["clf_confusion_matrix"].append(c_mat)

    # Increase Iteration Count
    iter_count += 1

# Dump the validation report into a JSON file
report_path = (
    Path.cwd() / "reports/validation_report_{}.json".format(report["clf_name"])
).resolve()
with open(report_path, "w") as json_file:
    json.dump(report, fp=json_file, indent=4)
print("\nValidation Report generated at {}".format(report_path))


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
