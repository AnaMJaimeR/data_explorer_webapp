# To be filled by students
import streamlit as st
from dataclasses import dataclass
import pandas as pd

# import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


@dataclass
class DateColumn:
    col_name: str
    serie: pd.Series

    def get_name(self):
        """
        Return name of selected column
        """
        return self.col_name

    def get_unique(self):
        """
        Return number of unique values for selected column
        """
        return self.serie.nunique()

    def get_missing(self):
        """
        Return number of missing values for selected column
        """
        return self.serie.isna().sum()

    def get_weekend(self):
        """
        Return number of occurrence of days falling during weekend (Saturday and Sunday)
        """
        return self.serie.dt.weekday.isin([5, 6]).sum()

    def get_weekday(self):
        """
        Return number of weekday days (not Saturday or Sunday)
        """
        return self.serie.dt.weekday.isin([1, 2, 3, 4, 5]).sum()

    def get_future(self):
        """
        Return number of cases with future dates (after today)
        """
        return (self.serie > datetime.today()).sum()

    def get_empty_1900(self):
        """
        Return number of occurrence of 1900-01-01 value
        """
        return (self.serie.dt.date == pd.Timestamp(1900, 1, 1)).sum()

    def get_empty_1970(self):
        """
        Return number of occurrence of 1970-01-01 value
        """
        return (self.serie.dt.date == pd.Timestamp(1970, 1, 1)).sum()

    def get_min(self):
        """
        Return the minimum date
        """
        return str(self.serie.min())

    def get_max(self):
        """
        Return the maximum date
        """
        return str(self.serie.max())

    def get_barchart(self):
        """
        Return the generated bar chart for selected column
        """
        # matplotlib
        # return self.serie.value_counts().plot.bar(x='values', y='quantity', rot=0)
        # plotly
        fig = px.bar(
            self.serie.value_counts().reset_index(), x="index", y=self.col_name
        )
        fig.update_layout(
            title="Quantity per Value",
            xaxis=dict(
                title=self.col_name,
                titlefont_size=16,
                tickfont_size=14,
                categoryorder="total descending",
            ),
            yaxis=dict(
                title="Quantity",
                titlefont_size=16,
                tickfont_size=14,
            ),
            template="simple_white",
        )
        return fig.show()

    def get_frequent(self):
        """
        Return the Pandas dataframe containing the occurrences and percentage of the top 20 most frequent values
        """
        counts = self.serie.value_counts()
        percent = self.serie.value_counts(
            normalize=True
        )  # TODO: choose if we drop na or not. True by default, dropna=False
        percent100 = (
            self.serie.value_counts(normalize=True).mul(100).round(1).astype(str) + "%"
        )
        df = pd.DataFrame(
            {"counts": counts, "per": percent, "per100": percent100}
        ).reset_index()
        df.columns = [
            "value",
            "occurrence",
            "percentage",
            "percentage100",
        ]  # if we dont want to rename columns, we can delete this step
        return df.head(20)
