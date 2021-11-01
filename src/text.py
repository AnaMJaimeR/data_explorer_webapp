import streamlit as st
from dataclasses import dataclass
import pandas as pd

import plotly.express as px

#parameters for the graph
graph_title = "Quantity per Value"
x_axis_titlefont_size = 16
x_axis_tickfont_size = 14
category_order = "total descending"
y_axis_title = "Quantity"
y_axis_titlefont_size = 16
y_axis_tickfont_size = 14
template = "simple_white"

@dataclass
class TextColumn:
    """
    Class for storing and showing information about a text column.

    Parameters
    ----------
    col_name : str
        name of the column.

    serie : pd.Series
        Series containing the data of a text column.
    """

    col_name: str
    serie: pd.Series

    def get_name(self) -> str:
        """Return name of selected column"""
        return self.col_name

    def get_unique(self) ->int:
        """Return number of unique values for selected column"""
        return self.serie.nunique()

    def get_missing(self) -> int:
        """Return number of missing values for selected column"""
        return self.serie.isna().sum()

    def get_empty(self) -> int:
        """Return number of rows with empty string for selected column"""
        return self.serie.str.fullmatch(
            ""
        ).sum()  # TODO: Check https://canvas.uts.edu.au/courses/19317/discussion_topics/195846

    def get_whitespace(self) -> int:
        """Return number of rows with only whitespaces for selected column"""
        return self.serie.str.isspace().sum()

    def get_lowercase(self) -> int:
        """Return number of rows with only lower case characters for selected column"""
        return self.serie.str.islower().sum()

    def get_uppercase(self) -> int:
        """Return number of rows with only upper case characters for selected column"""
        return self.serie.str.isupper().sum()

    def get_alphabet(self) -> int:
        """Return number of rows with only alphabet characters for selected column"""
        return self.serie.str.isalpha().sum()

    def get_digit(self) -> int:
        """Return number of rows with only numbers as characters for selected column"""
        return self.serie.str.isdigit().sum()

    def get_mode(self,dropna: bool = True) -> str:
        """Return the mode value for selected column"""
        return self.serie.mode(dropna=dropna)[0]

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

    def get_frequent(self,n_head: int = 20,dropna: bool = True) -> pd.DataFrame:
        """Return the Pandas dataframe containing the occurrences and percentage of the top 20 most frequent values"""
        counts = self.serie.value_counts().rename("ocurrences")
        percent = self.serie.value_counts(normalize=True, dropna = dropna).round(decimals = 4).rename(
            "percentage"
        )
        return (
            pd.concat([counts, percent], axis=1)
            .reset_index()
            .rename(columns={"index": "value"})
            .head(n_head)
        )
