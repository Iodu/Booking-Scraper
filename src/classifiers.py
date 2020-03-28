import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression as LogisticRegressionClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, ComplementNB, GaussianNB, MultinomialNB
from sklearn.svm import LinearSVC as LinearSVCClassifier

from data_handler_and_cleaner import cleaned_df as df

# Gaussian didn't work well; TypeError: A sparse matrix was passed, but dense data is required. Use X.toarray() to convert to a dense numpy array.
# I can probably fix this but its honestly not worth it.

nb_versions = {
    "Multinomial": MultinomialNB,
    # "Gaussian": GaussianNB,
    "Bernoulli": BernoulliNB,
    "Complement": ComplementNB,
}

# Minimal Example:
#   from data_handler_and_cleaner import cleaned_df as df
#   nb = NaiveBayes(df)
#   nb.describe_classifier()

MAX_FEATURES = 1000
TEST_SIZE = 0.2
class ClassifierBase:
    def __init__(self, df, model):
        self.df = df
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            df["review"], df["label"], test_size=TEST_SIZE
        )
        self.vect = CountVectorizer(
            stop_words={"english",}, max_features=MAX_FEATURES, binary=True
        )
        self.X_train_vect = self.vect.fit_transform(self.X_train)
        self.X_test_vect = self.vect.transform(self.X_test)
        self.model = model()

    def _calculate_balance(self):
        counts = self.df["label"].value_counts()
        self.balance = counts[0] / sum(counts) * 100
        print(f"Amount of negative reviews (balance) = {self.balance:.2f}%")

    def _calculate_fit_score(self):
        self.model.fit(self.X_train_vect, self.y_train)
        print(f"Fit score: {self.model.score(self.X_train_vect, self.y_train)}")

    def _predict(self):
        self.predictions = self.model.predict(self.X_test_vect)

    def _create_accuracy_score(self):
        self._predict()
        self.accuracy_score = accuracy_score(self.y_test, self.predictions)

    def _create_confusion_matrix(self):
        self.confusion_matrix = confusion_matrix(self.predictions, self.y_test)

    def describe_classifier(self):
        self._calculate_balance()
        self._calculate_fit_score()
        self._create_accuracy_score()
        self._create_confusion_matrix()
        self.outcome = pd.DataFrame(
            confusion_matrix(self.predictions, self.y_test),
            index=["P: Positive", "P: Negative"],
            columns=["Actual: Positive", "Actual: Negative"],
        )
        print(f"CM:  {self.outcome}")
        print(f"AS: {self.accuracy_score}")


class NaiveBayes(ClassifierBase):
    def __init__(self, df, version="Multinomial"):
        if version not in nb_versions.keys():
            raise Exception(
                f"Please either leave version empty or use either of: {[x for x in nb_versions.keys()]}"
            )
        model = nb_versions[version]
        super().__init__(df, model)


class LogisticRegression(ClassifierBase):
    def __init__(self, df):
        super().__init__(df, LogisticRegressionClassifier)


class LinearSVC(ClassifierBase):
    def __init__(self, df):
        super().__init__(df, LinearSVCClassifier)


class RandomForest(ClassifierBase):
    def __init__(self, df):
        super().__init__(df, RandomForestClassifier)


nb = RandomForest(df)
nb.describe_classifier()
