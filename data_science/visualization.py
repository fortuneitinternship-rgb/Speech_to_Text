import plotly.express as px


class VisualizationEngine:

    @staticmethod
    def histogram(df, column):
        return px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}"
        )

    @staticmethod
    def bar_chart(df, column):
        counts = (
            df[column]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            column,
            "Count"
        ]

        return px.bar(
            counts,
            x=column,
            y="Count",
            title=f"{column} Distribution"
        )

    @staticmethod
    def scatter_plot(df, x, y):
        return px.scatter(
            df,
            x=x,
            y=y,
            title=f"{x} vs {y}"
        )

    @staticmethod
    def box_plot(df, column):
        return px.box(
            df,
            y=column,
            title=f"{column} Box Plot"
        )

    @staticmethod
    def line_chart(df, x, y):
        return px.line(
            df,
            x=x,
            y=y,
            title=f"{y} over {x}"
        )