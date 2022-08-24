import sys, os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# ------------------------------------------------------------
# Adding CWD to path, for local module imports
sys.path.insert(0, os.getcwd())
# ------------------------------------------------------------


# Ask User to select a Classifier
def select_classifier():
    while True:
        print("\nCHOOSE A CLASSIFIER:\n")
        print("1. KNN")
        print("2. Naive Bayes Classifier")
        print("3. SVM")
        print("\nEnter Your Choice:", end=" ")
        choice = int(input())

        if choice == 1:
            name = "knn"
            classifier = KNeighborsClassifier(n_neighbors=5)
            print("\nMODEL SELECTED - {}".format(name))
            return name, classifier
        if choice == 2:
            name = "naive_bayes"
            classifier = GaussianNB()
            print("\nMODEL SELECTED - {}".format(name))
            return name, classifier
        if choice == 3:
            name = "svm"
            classifier = SVC(kernel="poly", degree=8)
            print("\nMODEL SELECTED - {}".format(name))
            return name, classifier


# ------------------------------------------------------------
# Reset - Removing CWD from path
sys.path.remove(os.getcwd())
# ------------------------------------------------------------
