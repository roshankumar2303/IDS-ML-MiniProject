import sys, os
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.build_features import build_features
from src.model.select_classifier import select_classifier


# Read the Interim Training Set
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
training_set = pd.read_csv(training_set_path, low_memory=False)

# Split training set into (X) and (Y)
xc, yc = training_set.shape
X_train = training_set.iloc[:, 0 : yc - 1]
Y_train = training_set.iloc[:, yc - 1]

# Feature Selection
feature_list, X_train, Y_train = build_features(X_train, Y_train)

# Choosing Classifier for Model Training
classifier_name, classifier = select_classifier()
print("\nMODEL SELECTED - {}".format(classifier_name))

# Training the Model
model = classifier.fit(X_train, np.ravel(Y_train))

# Exporting the Model
model_path = (Path.cwd() / "models/{}_MODEL.sav".format(classifier_name)).resolve()
print("\nExporting {} MODEL to {}\n".format(classifier_name, model_path))
joblib.dump(model, model_path)


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
