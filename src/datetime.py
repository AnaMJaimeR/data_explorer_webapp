import streamlit as st
from dataclasses import dataclass
import pandas as pd

import plotly.express as px
from datetime import datetime

graph_title = "Quantity per Value"
x_axis_titlefont_size = 16
x_axis_tickfont_size = 14
category_order = "total descending"
y_axis_title = "Quantity"
y_axis_titlefont_size = 16
y_axis_tickfont_size = 14
template = "simple_white"


@dataclass
class DateColumn:
    """
    Class for storing and show information about a date columns.

     Parameters
     ----------
     col_name : str
         name of the column.

     serie : pd.Series
         Pandas Series.
    """

    col_name: str
    serie: pd.Series

    def get_name(self) -> str:
        """Return name of selected column"""
        return self.col_name

    def get_unique(self):
        """Return number of unique values for selected column"""
        return self.serie.nunique()

    def get_missing(self):
        """Return number of missing values for selected column"""
        return self.serie.isna().sum()

    def get_weekend(self):
        """Return number of occurrence of days falling during weekend (Saturday and Sunday)"""
        return self.serie.dt.weekday.isin([5, 6]).sum()

    def get_weekday(self):
        """Return number of weekday days (not Saturday or Sunday)"""
        return self.serie.dt.weekday.isin([1, 2, 3, 4, 5]).sum()

    def get_future(self):
        """Return number of cases with future dates (after today)"""
        return (self.serie > datetime.today()).sum()

    def get_empty_1900(self):
        """Return number of occurrence of 1900-01-01 value"""
        return (self.serie.dt.date == pd.Timestamp(1900, 1, 1)).sum()

    def get_empty_1970(self):
        """Return number of occurrence of 1970-01-01 value"""
        return (self.serie.dt.date == pd.Timestamp(1970, 1, 1)).sum()

    def get_min(self):
        """Return the minimum date"""
        return str(self.serie.min())

    def get_max(self):
        """Return the maximum date"""
        return str(self.serie.max())

    def get_barchart(self):
        """Return the generated bar chart for selected column"""
        fig = px.bar(
            self.serie.value_counts().reset_index(), x="index", y=self.col_name
        )
        fig.update_layout(
            title=graph_title,
            xaxis=dict(
                title=self.col_name,
                titlefont_size=x_axis_titlefont_size,
                tickfont_size=x_axis_tickfont_size,
                categoryorder=category_order,
            ),
            yaxis=dict(
                title=y_axis_title,
                titlefont_size=y_axis_titlefont_size,
                tickfont_size=y_axis_tickfont_size,
            ),
            template=template,
        )
        return fig.show()

    def get_frequent(self):
        """Return the Pandas dataframe containing the occurrences and percentage of the top 20 most frequent values"""
        counts = self.serie.value_counts().rename("ocurrences")
        percent = self.serie.value_counts(normalize=True).rename(
            "percentage"
        )  # dropna=True by default
        return (
            pd.concat([counts, percent], axis=1)
            .reset_index()
            .rename(columns={"index": "value"})
            .head(20)
        )
