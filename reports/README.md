# IDS-ML-MiniProject - Reports

-   All generated observations in the form of graphs, data dictionaries, JSON files, log files, etc., can be stored in this folder

## File Naming Formats

-   For Validation Reports

    ```
    report-val-<model_name>-<feature_selector>.json
    ```

-   For Model Reports

    ```
    report-model-<model_name>-<feature_selector>.json
    ```

-   For Test Reports (Heatmaps of Confusion Matrices)

    ```
    report-test-hm-<model_name>-<feature_selector>.json
    ```

-   In the above formats:

    Where, `<model_name>` is one of the following

    -   `knn` for **_K Nearest Neighbors_**
    -   `naive_bayes` for **_Naive Bayes_**
    -   `svm` for **_SVM_**

    And, `<feature_selector>` is one of the following

    -   `skb` for **_Select K Best_**
    -   `rfe` for **_Recursive Feature Elimination with Decision Tree as Estimator_**
