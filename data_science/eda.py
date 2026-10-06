import pandas as pd
import numpy as np


class EDAAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def dataset_shape(self):
        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1]
        }

    def missing_values(self):
        result = self.df.isnull().sum()
        return result[result > 0].sort_values(ascending=False)

    def duplicate_count(self):
        return int(self.df.duplicated().sum())

    def numerical_columns(self):
        return self.df.select_dtypes(
            include=np.number
        ).columns.tolist()

    def categorical_columns(self):
        return self.df.select_dtypes(
            exclude=np.number
        ).columns.tolist()

    def descriptive_statistics(self):
        return self.df.describe(
            include="all"
        ).transpose()

    def correlation(self):
        numeric_df = self.df.select_dtypes(
            include=np.number
        )

        if numeric_df.empty:
            return pd.DataFrame()

        return numeric_df.corr()

    def data_types(self):
        return self.df.dtypes.astype(str)

    def summary(self):
        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "missing_values": int(
                self.df.isnull().sum().sum()
            ),
            "duplicate_rows": self.duplicate_count(),
            "numerical_columns": len(
                self.numerical_columns()
            ),
            "categorical_columns": len(
                self.categorical_columns()
            )
        }