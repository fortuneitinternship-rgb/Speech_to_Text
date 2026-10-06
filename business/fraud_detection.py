import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


class FraudDetector:

    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.model = None
        self.feature_columns = []

    # --------------------------------
    # PREPARE DATA
    # --------------------------------

    def prepare_data(
        self,
        target_column
    ):

        if target_column not in self.df.columns:
            raise ValueError(
                f"Column '{target_column}' not found"
            )

        data = self.df.copy()

        X = data.drop(
            columns=[target_column]
        )

        y = data[target_column]

        # Convert categorical columns
        categorical_columns = X.select_dtypes(
            exclude=np.number
        ).columns

        for column in categorical_columns:

            encoder = LabelEncoder()

            X[column] = encoder.fit_transform(
                X[column].astype(str)
            )

        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        )

        X = X.fillna(0)

        # Convert target to numbers
        if y.dtype == "object":

            target_encoder = LabelEncoder()

            y = target_encoder.fit_transform(
                y.astype(str)
            )

        y = pd.Series(y).astype(int)

        self.feature_columns = X.columns.tolist()

        return X, y

    # --------------------------------
    # TRAIN FRAUD MODEL
    # --------------------------------

    def train_model(
        self,
        target_column,
        test_size=0.2
    ):

        X, y = self.prepare_data(
            target_column
        )

        if y.nunique() < 2:
            raise ValueError(
                "Target column must contain "
                "at least two classes."
            )

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=test_size,
                random_state=42,
                stratify=y
            )
        )

        self.model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        )

        self.model.fit(
            X_train,
            y_train
        )

        predictions = self.model.predict(
            X_test
        )

        return {
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

    # --------------------------------
    # PREDICT FRAUD
    # --------------------------------

    def predict(
        self,
        dataframe
    ):

        if self.model is None:
            raise ValueError(
                "Train the model before prediction."
            )

        data = dataframe.copy()

        for column in data.select_dtypes(
            exclude=np.number
        ).columns:

            encoder = LabelEncoder()

            data[column] = encoder.fit_transform(
                data[column].astype(str)
            )

        data = data.replace(
            [np.inf, -np.inf],
            np.nan
        )

        data = data.fillna(0)

        # Keep only trained features
        data = data.reindex(
            columns=self.feature_columns,
            fill_value=0
        )

        predictions = self.model.predict(
            data
        )

        probabilities = self.model.predict_proba(
            data
        )

        result = dataframe.copy()

        result["Fraud Prediction"] = predictions

        result["Fraud Probability"] = (
            probabilities[:, -1]
        )

        result["Risk Level"] = np.where(
            result["Fraud Probability"] >= 0.75,
            "High Risk",
            np.where(
                result["Fraud Probability"] >= 0.40,
                "Medium Risk",
                "Low Risk"
            )
        )

        return result

    # --------------------------------
    # FRAUD SUMMARY
    # --------------------------------

    def fraud_summary(
        self,
        dataframe,
        prediction_column="Fraud Prediction"
    ):

        if prediction_column not in dataframe.columns:
            raise ValueError(
                f"Column '{prediction_column}' not found"
            )

        total = len(dataframe)

        fraud_count = int(
            (dataframe[prediction_column] == 1)
            .sum()
        )

        normal_count = total - fraud_count

        fraud_percentage = (
            fraud_count / total * 100
            if total > 0
            else 0
        )

        return {
            "total_transactions": total,
            "fraud_transactions": fraud_count,
            "normal_transactions": normal_count,
            "fraud_percentage": fraud_percentage
        }

    # --------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------

    def feature_importance(self):

        if self.model is None:
            raise ValueError(
                "Train the model first."
            )

        importance = pd.DataFrame({
            "Feature": self.feature_columns,
            "Importance": (
                self.model.feature_importances_
            )
        })

        return importance.sort_values(
            "Importance",
            ascending=False
        ).reset_index(drop=True)