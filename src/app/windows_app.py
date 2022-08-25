import sys, os
import json
import joblib
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.app.performance_metrics import get_windows_metrics


# Selecting KNN - RFE Model for Prediction
model_path = (Path.cwd() / "models/knn-rfe.sav").resolve()
report_path = (Path.cwd() / "reports/report-model-knn-rfe.json").resolve()

# Exit if KNN - RFE model is not found
if model_path.is_file() == False:
    print("KNN - RFE Model NOT FOUND in ./models...")
    print("Please run src/model/train_model.py and train KNN - RFE model...")
    exit(0)

# Exit if KNN - RFE model report is not found
if report_path.is_file() == False:
    print("KNN - RFE Model Report NOT FOUND in ./reports...")
    print("Model Reports contain data such as list of features...")
    print("This data is necessary to use the Model...")
    print("Please run src/model/train_model.py and generate KNN - RFE model report...")
    exit(0)

# Load Model and Model Report from the disk
model = joblib.load(model_path)
with open(report_path, "r") as json_file:
    report = json.load(json_file)

# Load Windows Performance Monitor compatible feature names
windows_features_path = (Path.cwd() / "src/app/windows_features.json").resolve()
with open(windows_features_path, "r") as json_file:
    windows_features = json.load(json_file)

# Load Prediction Map, which can be used to map the output to a label/class
# (0 for Normal) or (1-7 for Attack)
pred_map_path = (Path.cwd() / "src/app/prediction_map.json").resolve()
with open(pred_map_path, "r") as json_file:
    pred_map = json.load(json_file)

values = []
columns = []
# Iterate over features required by the model
for feature in report["clf_features"]:
    object = windows_features[feature]["object"]
    counter = windows_features[feature]["counter"]
    instance = windows_features[feature]["instance"]

    # Capture/read the feature metric using Windows Performance Monitor API
    print("\nCapturing '{}' | '{}' ...".format(object, counter))
    columns.append(feature)
    values.append(
        get_windows_metrics(object=object, counter=counter, instance=instance)
    )

    # Print the Metrics captured in this iteration to the console
    print("Observed Value - {}".format(values[-1]))

# Prediction
model_input = pd.DataFrame(data=[values], columns=columns)
model_output = model.predict(model_input)
print(
    "\nPREDICTION MADE BY THE MODEL: {}".format(
        [pred_map[str(op)] for op in model_output]
    )
)

# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
