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
