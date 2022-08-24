# IDS-ML-MiniProject

Academic Mini Project - Training and Analysis of Machine Learning Models for an Intrusion Detection System

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

The following is the order in which the scripts are supposed to be run (This order is mandatory):

### `src/data/get_dataset.py`

-   This script downloads the External dataset to the disk. If there's any non-network issue in downloading, please verify the link provided in the script

### `src/data/train_test_split.py`

-   Before splitting into Train & Test sets, the following transformations are made by this script:

    -   The output columns `label` and `type` are merged into a single column `type`; with string labels converted into numbers as follows:

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

    -   Unknown datatypes are converted into numeric (In case the conversion fails, the cells are filled with `NaN` instead)

    -   The timestamp column `ts` (1st column) is dropped since it is irrelevant to the output

    -   All the constant columns (i.e., columns filled with a single value) are also dropped

-   After all the above steps, this script splits the External dataset into Training (0.8) and Testing (0.2) sets

### `src/validation/validate.py`

-   This script performs Stratified K fold cross validation. i.e., each fold maintains the same o/p class ratio

-   The training set is split into k `(k = 5)` folds (or partitions); and the model is trained and tested over k `(k = 5)` iterations

-   In each iteration, the **_Training fold_** is made of `k - 1` (i.e., 4) folds from the original training set, whereas the **_Validation fold_** is made of 1 fold from original training set

-   Throughout the process, in each iteration, feature selection is performed on the **_Training fold_** seperately.

-   The Model is then trained with the Processed **_Training Fold_** and Tested against the **_Validation fold_**.

-   At the end, the script provides the list of best features for the model, and the performance metrics of the model
