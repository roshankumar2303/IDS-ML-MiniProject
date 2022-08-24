import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

external_dataset_path = (Path.cwd() / "data/external/ton-iot-windows-10.csv").resolve()
external_dataset = pd.read_csv(external_dataset_path)

# Merging Label and Type columns into a single column
new_labels = {
    "normal": 0,
    "ddos": 1,
    "dos": 2,
    "injection": 3,
    "mitm": 4,
    "password": 5,
    "scanning": 6,
    "xss": 7,
}
external_dataset.drop(columns="label", inplace=True)
external_dataset["type"].replace(to_replace=new_labels, inplace=True)

# Splitting into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(
    external_dataset.iloc[:, 0:125],
    external_dataset.iloc[:, 125],
    test_size=0.2,
    random_state=1,
)

# Exporting Train and Test sets
training_set_path = (Path.cwd() / "data/interim/training-set.csv").resolve()
testing_set_path = (Path.cwd() / "data/interim/testing-set.csv").resolve()

training_set = pd.DataFrame(X_train.join(Y_train))
training_set.to_csv(training_set_path, index=False)

testing_set = pd.DataFrame(X_test.join(Y_test))
testing_set.to_csv(testing_set_path, index=False)
