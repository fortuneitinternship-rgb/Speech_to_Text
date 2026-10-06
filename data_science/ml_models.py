import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression
)

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor
)


class MLAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def prepare_data(self, target_column):

        X = self.df.drop(
            columns=[target_column]
        )

        y = self.df[target_column]

        X = pd.get_dummies(
            X,
            drop_first=True
        )

        if y.dtype == "object":

            encoder = LabelEncoder()

            y = encoder.fit_transform(y)

        return X, y

    def classification(
        self,
        target_column,
        model_name="Random Forest"
    ):

        X, y = self.prepare_data(
            target_column
        )

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        models = {
            "Logistic Regression":
                LogisticRegression(
                    max_iter=1000
                ),

            "Decision Tree":
                DecisionTreeClassifier(
                    random_state=42
                ),

            "Random Forest":
                RandomForestClassifier(
                    random_state=42
                )
        }

        model = models[model_name]

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        return {
            "model": model,
            "accuracy": accuracy_score(
                y_test,
                predictions
            ),
            "precision": precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            ),
            "recall": recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            ),
            "f1": f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )
        }

    def regression(
        self,
        target_column,
        model_name="Random Forest"
    ):

        X, y = self.prepare_data(
            target_column
        )

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        models = {
            "Linear Regression":
                LinearRegression(),

            "Random Forest":
                RandomForestRegressor(
                    random_state=42
                )
        }

        model = models[model_name]

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        mse = mean_squared_error(
            y_test,
            predictions
        )

        return {
            "model": model,
            "r2": r2_score(
                y_test,
                predictions
            ),
            "mae": mean_absolute_error(
                y_test,
                predictions
            ),
            "rmse": mse ** 0.5
        }