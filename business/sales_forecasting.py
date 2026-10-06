import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression


class SalesForecaster:

    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.model = None

    # -----------------------------
    # PREPARE TIME SERIES DATA
    # -----------------------------

    def prepare_data(
        self,
        date_column,
        sales_column
    ):

        if date_column not in self.df.columns:
            raise ValueError(
                f"Column '{date_column}' not found"
            )

        if sales_column not in self.df.columns:
            raise ValueError(
                f"Column '{sales_column}' not found"
            )

        data = self.df[
            [date_column, sales_column]
        ].copy()

        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce"
        )

        data[sales_column] = pd.to_numeric(
            data[sales_column],
            errors="coerce"
        )

        data = data.dropna()

        data = (
            data
            .groupby(date_column)[sales_column]
            .sum()
            .reset_index()
            .sort_values(date_column)
        )

        return data

    # -----------------------------
    # MOVING AVERAGE
    # -----------------------------

    def moving_average(
        self,
        date_column,
        sales_column,
        window=3
    ):

        data = self.prepare_data(
            date_column,
            sales_column
        )

        data["Moving Average"] = (
            data[sales_column]
            .rolling(window=window)
            .mean()
        )

        return data

    # -----------------------------
    # TRAIN FORECAST MODEL
    # -----------------------------

    def train(
        self,
        date_column,
        sales_column
    ):

        data = self.prepare_data(
            date_column,
            sales_column
        )

        if len(data) < 2:
            raise ValueError(
                "At least two time points are "
                "required for forecasting."
            )

        data["Time Index"] = np.arange(
            len(data)
        )

        X = data[["Time Index"]]
        y = data[sales_column]

        self.model = LinearRegression()

        self.model.fit(
            X,
            y
        )

        return {
            "model": self.model,
            "data": data,
            "slope": float(
                self.model.coef_[0]
            ),
            "intercept": float(
                self.model.intercept_
            )
        }

    # -----------------------------
    # FORECAST FUTURE SALES
    # -----------------------------

    def forecast(
        self,
        date_column,
        sales_column,
        periods=7
    ):

        data = self.prepare_data(
            date_column,
            sales_column
        )

        if self.model is None:
            self.train(
                date_column,
                sales_column
            )

        last_index = len(data) - 1

        future_indices = np.arange(
            last_index + 1,
            last_index + periods + 1
        )

        # Keep the same feature name used
        # during model training.
        future_data = pd.DataFrame({
            "Time Index": future_indices
        })

        predictions = self.model.predict(
            future_data
        )

        last_date = data[
            date_column
        ].max()

        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=periods,
            freq="D"
        )

        forecast_data = pd.DataFrame({
            "Date": future_dates,
            "Forecast Sales": predictions
        })

        forecast_data["Forecast Sales"] = (
            forecast_data["Forecast Sales"]
            .clip(lower=0)
        )

        return forecast_data

    # -----------------------------
    # TREND ANALYSIS
    # -----------------------------

    def trend(
        self,
        date_column,
        sales_column
    ):

        result = self.train(
            date_column,
            sales_column
        )

        slope = result["slope"]

        if slope > 0:
            direction = "Increasing"

        elif slope < 0:
            direction = "Decreasing"

        else:
            direction = "Stable"

        return {
            "direction": direction,
            "slope": slope
        }

    # -----------------------------
    # FORECAST SUMMARY
    # -----------------------------

    def summary(
        self,
        date_column,
        sales_column,
        periods=7
    ):

        data = self.prepare_data(
            date_column,
            sales_column
        )

        forecast = self.forecast(
            date_column,
            sales_column,
            periods
        )

        return {
            "historical_records": len(data),
            "historical_sales": float(
                data[sales_column].sum()
            ),
            "forecast_periods": periods,
            "forecast_sales": float(
                forecast["Forecast Sales"].sum()
            ),
            "trend": self.trend(
                date_column,
                sales_column
            )["direction"]
        }