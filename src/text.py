# To be filled by students
import streamlit as st
from dataclasses import dataclass
import pandas as pd

# import matplotlib.pyplot as plt
import plotly.express as px


@dataclass
class TextColumn:
    col_name: str
    serie: pd.Series

    def get_name(self):  # TODO: we aware that the "" is not present in the app
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
        # return self.serie.isnull().sum() #should be the same

    def get_empty(self):
        """
        Return number of rows with empty string for selected column
        """
        return (
            self.serie.str.strip().values == ""
        ).sum()  # CHECK: https://canvas.uts.edu.au/courses/19317/discussion_topics/195846

    def get_whitespace(self):
        """
        Return number of rows with only whitespaces for selected column
        """
        return self.serie.str.isspace().sum()

    def get_lowercase(self):
        """
        Return number of rows with only lower case characters for selected column
        """
        return self.serie.str.islower().sum()

    def get_uppercase(self):
        """
        Return number of rows with only upper case characters for selected column
        """
        return self.serie.str.isupper().sum()

    def get_alphabet(self):
        """
        Return number of rows with only alphabet characters for selected column
        """
        return self.serie.str.isalpha().sum()

    def get_digit(self):
        """
        Return number of rows with only numbers as characters for selected column
        """
        return self.serie.str.isdigit().sum()

    def get_mode(self):
        """
        Return the mode value for selected column
        """
        return self.serie.mode(dropna=True)  # TODO: choose is we want to drop na or not

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
        )  # TODO: choose to drop na? True by default, dropna=False
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
