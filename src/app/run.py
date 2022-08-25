import sys, os
import json
import joblib
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------
from src.app.get_performance_attributes import get_performance_attributes

model_path = (Path.cwd() / "models/knn-rfe.sav").resolve()
model = joblib.load(model_path)

report_path = (Path.cwd() / "reports/report-model-knn-rfe.json").resolve()
report = ""
with open(report_path, "r") as json_file:
    report = json.load(json_file)

perf_mon_path = (Path.cwd() / "reports/perf_mon_data.json").resolve()
perf_mon = ""
with open(perf_mon_path, "r") as json_file:
    perf_mon = json.load(json_file)

inp = {}
for feature in report["clf_features"]:
    print(
        "\n{} - {}:".format(perf_mon[feature]["object"], perf_mon[feature]["counter"])
    )
    inp[feature] = [
        get_performance_attributes(
            perf_mon[feature]["object"],
            perf_mon[feature]["counter"],
            perf_mon[feature]["instance"],
        )
    ]
    print("{} - {}".format(feature, inp[feature]))


inp = pd.DataFrame(inp)
pred_out = model.predict(inp)
print("Output: {}".format(pred_out))

# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
