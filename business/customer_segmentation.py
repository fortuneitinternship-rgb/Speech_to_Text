import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerSegmentation:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def calculate_rfm(
        self,
        customer_column,
        date_column,
        value_column,
        reference_date=None
    ):

        required_columns = [
            customer_column,
            date_column,
            value_column
        ]

        for column in required_columns:
            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found"
                )

        self.df[date_column] = pd.to_datetime(
            self.df[date_column],
            errors="coerce"
        )

        self.df[value_column] = pd.to_numeric(
            self.df[value_column],
            errors="coerce"
        )

        self.df = self.df.dropna(
            subset=[
                customer_column,
                date_column,
                value_column
            ]
        )

        if reference_date is None:
            reference_date = (
                self.df[date_column].max()
                + pd.Timedelta(days=1)
            )
        else:
            reference_date = pd.to_datetime(
                reference_date
            )

        rfm = self.df.groupby(
            customer_column
        ).agg(
            Recency=(
                date_column,
                lambda x: (
                    reference_date - x.max()
                ).days
            ),
            Frequency=(
                date_column,
                "count"
            ),
            Monetary=(
                value_column,
                "sum"
            )
        ).reset_index()

        return rfm

    def create_segments(
        self,
        rfm,
        number_of_clusters=4
    ):

        if rfm.empty:
            return rfm

        features = [
            "Recency",
            "Frequency",
            "Monetary"
        ]

        data = rfm[features].copy()

        scaler = StandardScaler()

        scaled_data = scaler.fit_transform(
            data
        )

        model = KMeans(
            n_clusters=number_of_clusters,
            random_state=42,
            n_init=10
        )

        rfm["Cluster"] = model.fit_predict(
            scaled_data
        )

        return rfm

    def label_segments(self, rfm):

        if rfm.empty:
            return rfm

        cluster_summary = (
            rfm.groupby("Cluster")
            [["Recency", "Frequency", "Monetary"]]
            .mean()
        )

        cluster_summary["Score"] = (
            cluster_summary["Frequency"]
            + cluster_summary["Monetary"]
            - cluster_summary["Recency"]
        )

        sorted_clusters = (
            cluster_summary["Score"]
            .sort_values(ascending=False)
            .index
            .tolist()
        )

        labels = [
            "High Value",
            "Loyal",
            "At Risk",
            "Low Engagement"
        ]

        cluster_labels = {}

        for index, cluster in enumerate(
            sorted_clusters
        ):
            if index < len(labels):
                cluster_labels[
                    cluster
                ] = labels[index]
            else:
                cluster_labels[
                    cluster
                ] = "Other"

        rfm["Segment"] = rfm[
            "Cluster"
        ].map(cluster_labels)

        return rfm

    def run(
        self,
        customer_column,
        date_column,
        value_column,
        number_of_clusters=4
    ):

        rfm = self.calculate_rfm(
            customer_column,
            date_column,
            value_column
        )

        rfm = self.create_segments(
            rfm,
            number_of_clusters
        )

        rfm = self.label_segments(
            rfm
        )

        return rfm

    def segment_summary(self, rfm):

        if rfm.empty:
            return pd.DataFrame()

        return (
            rfm.groupby("Segment")
            .agg(
                Customers=(
                    "Segment",
                    "count"
                ),
                Average_Recency=(
                    "Recency",
                    "mean"
                ),
                Average_Frequency=(
                    "Frequency",
                    "mean"
                ),
                Average_Monetary=(
                    "Monetary",
                    "mean"
                )
            )
            .reset_index()
            .sort_values(
                "Customers",
                ascending=False
            )
        )