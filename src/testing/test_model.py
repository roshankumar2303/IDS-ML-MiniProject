import sys, os
import json
import joblib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import confusion_matrix

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.features.clean_data import clean_data


# Check for Generated Model Reports
report_glob = (Path.cwd() / "reports").glob("report-model-*.json")
report_paths = [r.resolve() for r in report_glob if r.is_file()]
if len(report_paths) == 0:
    print("No Model Reports Found in ./reports...")
    print("Model Reports contain data such as classifier name and list of features...")
    print("This data is necessary to test the Model...")
    print(
        "Please run src/model/train_model.py to train models and generate model reports..."
    )
    exit(0)

# Load all Generated Model Reports
reports = []
for path in report_paths:
    with open(path, "r") as json_file:
        reports.append(json.load(json_file))

# Iteration over Reports to test each model
for report in reports:
    # Loading the Model
    model_path = (
        Path.cwd()
        / "models/{}-{}.sav".format(report["clf_name"], report["feature_selector"])
    ).resolve()
    if model_path.is_file() == False:
        print(
            "Corresponding Model for '{}-{}' NOT FOUND in ./models...".format(
                report["clf_name"], report["feature_selector"]
            )
        )
        print("Please try running src/model/train_model.py to train the model...")
        continue
    model = joblib.load(model_path)
    print("\nTesting model ({}) found at {}".format(report["clf_name"], model_path))

    # Read the Interim Testing Set
    testing_set_path = (Path.cwd() / "data/interim/testing-set.csv").resolve()
    testing_set = pd.read_csv(testing_set_path, low_memory=False)

    # Split Testing Set into (X) and (Y)
    xc, yc = testing_set.shape
    X_test = testing_set.iloc[:, 0 : yc - 1]
    Y_test = testing_set.iloc[:, yc - 1]

    # Clean data and drop unwanted features from Testing Set (X)
    X_test, Y_test = clean_data(X_test, Y_test)
    for column in X_test:
        if column not in report["clf_features"]:
            X_test.drop(columns=column, inplace=True)

    # Predict output of Testing Set (X)
    Y_pred = model.predict(X_test)

    # Generate metrics from Predicted output and True output (Testing (Y))
    c_mat = confusion_matrix(Y_test, Y_pred)

    # Create Heatmap of Confusion Matrix
    heatmap_path = (
        Path.cwd()
        / "reports/report-test-hm-{}-{}.png".format(
            report["clf_name"], report["feature_selector"]
        )
    ).resolve()
    print("Exporting CM heatmap to {}".format(heatmap_path))
    heatmap = sns.heatmap(c_mat, cmap="rocket_r", annot=True, fmt="d")
    plt.savefig(heatmap_path, dpi=300)
    plt.clf()

print("\nTesting Complete")


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
