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
from src.features.build_features import select_k_best_features
from src.model.select_classifier import select_classifier


# Report for model training stats
report = {"clf_name": "", "clf_features": []}

# Read the Interim Training Set
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
training_set = pd.read_csv(training_set_path, low_memory=False)

# Split training set into (X) and (Y)
xc, yc = training_set.shape
X_train = training_set.iloc[:, 0 : yc - 1]
Y_train = training_set.iloc[:, yc - 1]

# Feature Selection
report["clf_features"], X_train, Y_train = select_k_best_features(X_train, Y_train)

# Choosing Classifier for Model Training
report["clf_name"], classifier = select_classifier()

# Training the Model
classifier.fit(X_train, np.ravel(Y_train))

# Dump the model training report into a JSON file
report_path = (
    Path.cwd() / "reports/model_report_{}.json".format(report["clf_name"])
).resolve()
with open(report_path, "w") as json_file:
    json.dump(report, json_file, indent=4)
print("\nModel Report generated at {}".format(report_path))

# Exporting the Model
model_path = (Path.cwd() / "models/{}.sav".format(report["clf_name"])).resolve()
print("Exporting '{}' model as '.sav' to {}\n".format(report["clf_name"], model_path))
joblib.dump(classifier, model_path)


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
