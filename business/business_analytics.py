import pandas as pd
import numpy as np


class BusinessAnalytics:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # -----------------------------
    # BASIC BUSINESS SUMMARY
    # -----------------------------

    def summary(self):

        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "total_numeric_columns": len(
                self.df.select_dtypes(
                    include=np.number
                ).columns
            ),
            "total_categorical_columns": len(
                self.df.select_dtypes(
                    exclude=np.number
                ).columns
            )
        }

    # -----------------------------
    # KPI CALCULATOR
    # -----------------------------

    def calculate_kpi(
        self,
        column
    ):

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found"
            )

        series = pd.to_numeric(
            self.df[column],
            errors="coerce"
        ).dropna()

        if series.empty:
            return {}

        return {
            "total": float(series.sum()),
            "average": float(series.mean()),
            "minimum": float(series.min()),
            "maximum": float(series.max()),
            "median": float(series.median()),
            "standard_deviation": float(
                series.std()
            )
        }

    # -----------------------------
    # GROUP ANALYSIS
    # -----------------------------

    def group_analysis(
        self,
        category_column,
        value_column
    ):

        if category_column not in self.df.columns:
            raise ValueError(
                f"Column '{category_column}' not found"
            )

        if value_column not in self.df.columns:
            raise ValueError(
                f"Column '{value_column}' not found"
            )

        result = (
            self.df
            .groupby(category_column)[value_column]
            .agg([
                "sum",
                "mean",
                "count"
            ])
            .reset_index()
        )

        return result.sort_values(
            "sum",
            ascending=False
        )

    # -----------------------------
    # TOP PERFORMERS
    # -----------------------------

    def top_performers(
        self,
        category_column,
        value_column,
        top_n=10
    ):

        result = self.group_analysis(
            category_column,
            value_column
        )

        return result.head(top_n)

    # -----------------------------
    # SALES ANALYSIS
    # -----------------------------

    def sales_analysis(
        self,
        sales_column
    ):

        if sales_column not in self.df.columns:
            raise ValueError(
                f"Column '{sales_column}' not found"
            )

        sales = pd.to_numeric(
            self.df[sales_column],
            errors="coerce"
        ).dropna()

        return {
            "total_sales": float(
                sales.sum()
            ),
            "average_sales": float(
                sales.mean()
            ),
            "highest_sale": float(
                sales.max()
            ),
            "lowest_sale": float(
                sales.min()
            ),
            "number_of_transactions": int(
                sales.count()
            )
        }

    # -----------------------------
    # CUSTOMER ANALYSIS
    # -----------------------------

    def customer_analysis(
        self,
        customer_column,
        value_column
    ):

        if customer_column not in self.df.columns:
            raise ValueError(
                f"Column '{customer_column}' not found"
            )

        if value_column not in self.df.columns:
            raise ValueError(
                f"Column '{value_column}' not found"
            )

        result = (
            self.df
            .groupby(customer_column)[value_column]
            .agg([
                "sum",
                "mean",
                "count"
            ])
            .reset_index()
        )

        result.columns = [
            customer_column,
            "Total Value",
            "Average Value",
            "Transactions"
        ]

        return result.sort_values(
            "Total Value",
            ascending=False
        )

    # -----------------------------
    # OUTLIER DETECTION
    # -----------------------------

    def detect_outliers(
        self,
        column
    ):

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found"
            )

        values = pd.to_numeric(
            self.df[column],
            errors="coerce"
        )

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = self.df[
            (values < lower_bound)
            | (values > upper_bound)
        ].copy()

        return {
            "outliers": outliers,
            "count": len(outliers),
            "lower_bound": float(
                lower_bound
            ),
            "upper_bound": float(
                upper_bound
            )
        }

    # -----------------------------
    # AUTOMATIC INSIGHTS
    # -----------------------------

    def generate_insights(
        self,
        value_column
    ):

        if value_column not in self.df.columns:
            raise ValueError(
                f"Column '{value_column}' not found"
            )

        values = pd.to_numeric(
            self.df[value_column],
            errors="coerce"
        ).dropna()

        if values.empty:
            return [
                "No numeric data available."
            ]

        total = values.sum()
        average = values.mean()
        maximum = values.max()
        minimum = values.min()

        insights = [
            f"Total value: {total:.2f}",
            f"Average value: {average:.2f}",
            f"Highest value: {maximum:.2f}",
            f"Lowest value: {minimum:.2f}",
            f"Number of records: {len(values)}"
        ]

        if maximum > average * 2:
            insights.append(
                "A high-value outlier may exist."
            )

        if minimum < average * 0.25:
            insights.append(
                "Some transactions are significantly "
                "below the average."
            )

        return insights