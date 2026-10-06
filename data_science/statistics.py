import numpy as np
import pandas as pd


class StatisticsAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def numeric_summary(self):

        numeric = self.df.select_dtypes(
            include=np.number
        )

        if numeric.empty:
            return pd.DataFrame()

        return pd.DataFrame({
            "Mean": numeric.mean(),
            "Median": numeric.median(),
            "Std Dev": numeric.std(),
            "Variance": numeric.var(),
            "Minimum": numeric.min(),
            "Maximum": numeric.max(),
            "25th Percentile": numeric.quantile(0.25),
            "50th Percentile": numeric.quantile(0.50),
            "75th Percentile": numeric.quantile(0.75)
        })

    def correlation(self):

        numeric = self.df.select_dtypes(
            include=np.number
        )

        if numeric.empty:
            return pd.DataFrame()

        return numeric.corr()

    def z_scores(self):

        numeric = self.df.select_dtypes(
            include=np.number
        )

        if numeric.empty:
            return pd.DataFrame()

        return (
            numeric - numeric.mean()
        ) / numeric.std()