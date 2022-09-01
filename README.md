# IDS-ML-MiniProject

Academic Mini Project - Training and Analysis of Machine Learning Models for an Intrusion Detection System

## The Team

-   Roshan [@roshankumar2303](https://github.com/roshankumar2303)

-   Shree Shrutha [@shruthareddy](https://github.com/shruthareddy)

-   Hruday Vikas [@SakivYadurh](https://github.com/SakivYadurh)

-   Yahwanth [@YahwanthSabbithi](https://github.com/YahwanthSabbithi)

-   Avinash [@avinashreddy-11105](https://github.com/avinashreddy-11105)

## Dataset used

ToN-IoT datasets (University of New South Wales) - https://research.unsw.edu.au/projects/toniot-datasets

## Requirements

-   Python 3.10 - https://www.python.org/downloads/

    > Packages required are included in `requirements.txt`. Refer below for setting up the packages

## Setting up the repo locally

-   To clone the repo, run the following command

    ```
    git clone https://github.com/roshankumar2303/IDS-ML-MiniProject.git
    ```

## Setting up Python Virtual Environment `venv`

-   It is highly recommended that you have Python 3.10 installed on your machine

-   To set up the python virtual environment, run the following command

    ```
    cd IDS-ML-MiniProject/
    python -m venv env
    ```

-   To activate the virtual environment, run the following command

    ```
    # In bash
    source <base-path>/IDS-ML-MiniProject/env/Scripts/activate

    # In CMD
    IDS-ML-MiniProject\env\Scripts\activate
    ```

> Note: VS Code automatically detects the python virtual environment and promts you to set it up as default Python interpreter for the workspace. Select "YES" so that the virtual environment is automatically activated when you open the project in VS Code

## Installing the Dependencies

-   After activating the virtual environment, to install all the required dependencies, run the following command

    ```
    pip install -r requirements.txt
    ```

## Updating the Dependencies

-   If any changes/updates are made to the dependencies (or) if new dependencies are added, run the following command before committing those changes

    ```
    pip freeze > requirements.txt
    ```

-   This updates `requirements.txt` file to include new dependencies as well

-   If possible, run the above command before every commit to ensure no dependecies are missed

## Running the Project

The following is the order in which the scripts are to be run (This order is mandatory):

### `src/data/get_dataset.py`

-   This script downloads the External dataset to the disk. If there's any non-network issue in downloading, please check if the dataset URL used in the script is still valid

### `src/data/train_test_split.py`

-   Before splitting into Training & Testing sets, the following data transformations are made by this script:

    -   The output columns `label` and `type` are merged into a single column `type`; with the string labels converted into numerics:

    ```
    "normal": 0
    "ddos": 1
    "dos": 2
    "injection": 3
    "mitm": 4
    "password": 5
    "scanning": 6
    "xss": 7
    ```

    -   Unknown datatypes are converted into numerics (In case of error during conversion, the respective cells are filled with `NaN` instead)

    -   The timestamp column: `ts` (1st column) is dropped since it is irrelevant

    -   All the constant columns (i.e., columns filled entirely with only a single value) are also dropped

-   After all the above steps, this script splits the External dataset into Training (80%) and Testing (20%) sets

### `src/validation/validate.py`

-   This script performs Stratified K-fold cross validation. i.e., each generated fold maintains the same o/p class ratio

-   The training set is split into k `(k = 5)` folds (or partitions); and the model (KNN / SVM / Naive Bayes) will be trained and tested over k `(k = 5)` iterations

-   In each iteration, a **_Training fold_** is made from `k - 1` (i.e., 4) folds of the original training set, and similarly, a **_Validation fold_** is made from one fold.

-   Throughout the process, in each iteration, Feature Selection (Select K Best / RFE) is performed on the **_Training fold_** seperately.

-   The Model (KNN / SVM / Naive Bayes) is then trained with the Processed **_Training Fold_** and Tested against the **_Validation fold_**.

-   At the end, the script generates a report with performance metrics of the model, and the list of features selected and used in the validation

### `src/model/train_model.py`

-   This script chooses a classifier (KNN / SVM / Naive Bayes) and feature selector (Select K Best / RFE) specified by the user to train a ML model

-   Feature selection (Select K Best / RFE) is performed on the Training Set, and the Model is then trained and exported as a `.sav` file using `joblib`

-   This script also generates a report containing the name of the classifier (KNN / SVM / Naive Bayes), the feature selector (Select K Best / RFE), and the list of features selected.

-   This report is important as it is needed for performing testing on the model using `src/test/test_model.py`

### `src/testing/test_model.py`

-   This script performs testing on all the models `(*.sav files)` found in `models/` folder

-   As output, this script generates heatmap of the confusion matrix obtained by using Testing set on the respective model

> Note: All the reports, heatmaps, etc., generated are stored in `reports/` folder
