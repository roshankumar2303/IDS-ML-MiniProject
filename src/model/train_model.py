import sys, os
import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.choose_feature_selector import choose_feature_selector
from src.model.select_classifier import select_classifier


# Report for model training statistics
report = {"clf_name": "", "feature_selector": "", "clf_features": []}

# Read the Interim Training Set
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
training_set = pd.read_csv(training_set_path, low_memory=False)

# Split training set into (X) and (Y)
xc, yc = training_set.shape
X_train = training_set.iloc[:, 0 : yc - 1]
Y_train = training_set.iloc[:, yc - 1]

# Choosing Classifier for Model Training
report["clf_name"], classifier = select_classifier()

# Choosing Selector for Feature selection
report["feature_selector"], feature_selector = choose_feature_selector()

# Feature Selection
report["clf_features"], X_train, Y_train = feature_selector(X_train, Y_train)

# Training the Model
classifier.fit(X_train, np.ravel(Y_train))

# Dump the model training report into a JSON file
report_path = (
    Path.cwd()
    / "reports/report-model-{}-{}.json".format(
        report["clf_name"], report["feature_selector"]
    )
).resolve()
with open(report_path, "w") as json_file:
    json.dump(report, json_file, indent=4)
print("\nModel Report generated at {}".format(report_path))

# Exporting the Model
model_path = (
    Path.cwd()
    / "models/{}-{}.sav".format(report["clf_name"], report["feature_selector"])
).resolve()
print("Exporting '{}' model as '.sav' to {}\n".format(report["clf_name"], model_path))
joblib.dump(classifier, model_path)


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
