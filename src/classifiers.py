import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import \
    LogisticRegression as LogisticRegressionClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import (BernoulliNB, ComplementNB, GaussianNB,
                                 MultinomialNB)
from sklearn.svm import LinearSVC as LinearSVCClassifier
from datetime import datetime
import pickle

from matplotlib import pyplot 
import time
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

# Gaussian didn't work well; TypeError: A sparse matrix was passed, but dense data is required. Use X.toarray() to convert to a dense numpy array.
# I can probably fix this but its honestly not worth it.

nb_versions = {
    "Multinomial": MultinomialNB,
    # "Gaussian": GaussianNB,
    # "Bernoulli": BernoulliNB,
    "Complement": ComplementNB,
}

# Minimal Example:
#   from data_handler_and_cleaner import cleaned_df as df
#   nb = NaiveBayes(df)
#   nb.describe_classifier()

MAX_FEATURES = 2500
TEST_SIZE = 0.2


class ClassifierBase:
    def __init__(self, df, model):
        self.df = df
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.df["review"].map(str), self.df["label"], test_size=TEST_SIZE
        )
        self.vect = CountVectorizer(
            stop_words={"english",}, max_features=MAX_FEATURES,
        )
        print(self.X_train)
        self.X_train_vect = self.vect.fit_transform(self.X_train)
        self.X_test_vect = self.vect.transform(self.X_test)
        max_iter_models = ['LogisticRegression']
        if self.__class__.__name__ in max_iter_models:
            self.model = model(max_iter=600)
        max_iter_models = ['LinearSVC']
        if self.__class__.__name__ in max_iter_models:
            self.model = model(max_iter=6000)
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

    def _create_roc_curve(self):
        if self.model.__class__.__name__ == 'LinearSVC':
            probs= self.model._predict_proba_lr(self.X_test,self.y_test)
        else:
            self.model.__class__.__name__
            probs = self.model.predict_proba(self.X_test_vect)
        probs = probs[:, 1]
        auc = roc_auc_score(self.y_test, probs)
        print(f'AUC: {auc:.3f}%')
        fpr, tpr, thresholds = roc_curve(self.y_test, probs)
        pyplot.plot([0, 1], [0, 1], linestyle='--')
        pyplot.plot(fpr, tpr, marker='.')
        pyplot.show()


    def dump_model_to_pickle(self):
        pickle.dump(self.model, open(f'models/{self.__class__.__name__ }_vect.pickle', 'wb+'))
        pickle.dump(self.vect, open(f'models/{self.__class__.__name__}.pickle', 'wb+'))


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
        print(f"{self.outcome}")
        print(f"Accuracy: {self.accuracy_score}")
        print(self._create_roc_curve())


class NaiveBayes(ClassifierBase):
    def __init__(self, df, version="Multinomial"):
        if version not in nb_versions.keys():
            raise Exception(
                f"Please either leave version empty or use either of: {[x for x in nb_versions.keys()]}"
            )
        model = nb_versions[version]
        super().__init__(df, model)


class LogisticRegression(ClassifierBase):
    # lib linear solver
    def __init__(self, df):
        super().__init__(df, LogisticRegressionClassifier)


class LinearSVC(ClassifierBase):
    def __init__(self, df):
        super().__init__(df, LinearSVCClassifier)


class RandomForest(ClassifierBase):
    def __init__(self, df):
        super().__init__(df, RandomForestClassifier)


def _open_trained_model_from_pickle(pickle_file_name):
    loaded_vector = pickle.load(open(pickle_file_name + '_vect.pickle', 'rb'))
    loaded_model = pickle.load(open(pickle_file_name + '.pickle', 'rb'))
    return loaded_vector, loaded_model

def predict_from_df(df_to_predict, pickle_file_name):
    loaded_vector, loaded_model = _open_trained_model_from_pickle(pickle_file_name)
    df_to_predict_vect = loaded_vector.transform(df_to_predict)
    prediction = loaded_model.predict(df_to_predict_vect)


from data_handler_and_cleaner import df
from helper import current_milli_time

# start = current_milli_time()

# nb = LinearSVC(df)
# nb.describe_classifier()
# # nb.dump_model_to_pickle()

# end = current_milli_time()

# print(f"{(end - start) * 0.001} seconds")