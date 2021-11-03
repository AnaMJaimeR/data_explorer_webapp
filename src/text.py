from dataclasses import dataclass

import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from src.settings import FormatBarPlot


@dataclass
class TextColumn:
    """
    Class for storing and showing information about a text column.

    Attributes
    ----------
    col_name : str
        Name of the text pandas column.

    serie : pd.Series
        Series containing the data of the text pandas column.
    """

    col_name: str
    serie: pd.Series

    def get_name(self) -> str:
        """Return name of selected column."""
        return self.col_name

    def get_unique(self) -> int:
        """Return number of unique values for selected column."""
        return self.serie.nunique()

    def get_missing(self) -> int:
        """Return number of missing values for selected column."""
        return int(self.serie.isna().sum())

    def get_empty(self) -> int:
        """Return number of rows with empty string for selected column."""
        return int(self.serie.str.fullmatch("").sum())

    def get_whitespace(self) -> int:
        """Return number of rows with only whitespaces for selected column."""
        return int(self.serie.str.isspace().sum())

    def get_lowercase(self) -> int:
        """Return number of rows with only lower case characters for selected column."""
        return int(self.serie.str.islower().sum())

    def get_uppercase(self) -> int:
        """Return number of rows with only upper case characters for selected column."""
        return int(self.serie.str.isupper().sum())

    def get_alphabet(self) -> int:
        """Return number of rows with only alphabet characters for selected column."""
        return int(self.serie.str.isalpha().sum())

    def get_digit(self) -> int:
        """Return number of rows with only numbers as characters for selected column."""
        return int(self.serie.str.isdigit().sum())

    def get_mode(self, dropna: bool = True) -> str:
        """Return the mode value for selected column."""
        return self.serie.mode(dropna=dropna)[0]

    def _get_occurrences(self) -> pd.Series:
        """Return the occurrences per value for selected column."""
        return self.serie.value_counts().rename("occurrence")

    def _get_percentages(self) -> pd.Series:
        """Return the normalised occurrences per value for selected column."""
        return (
            self.serie.value_counts(normalize=True)
            .round(decimals=4)
            .rename("percentage")
        )

    def get_barchart(
        self,
        params: FormatBarPlot,
    ) -> Figure:
        """Return the generated bar chart for selected column."""
        fig = px.bar(self._get_occurrences(), x="index", y=self.col_name)
        fig.update_layout(
            title=params.TITLE,
            xaxis=dict(
                title=self.col_name,
                titlefont_size=params.AXIS_FONT_SIZE,
                tickfont_size=params.TICK_FONT_SIZE,
            ),
            yaxis=dict(
                title=params.Y_AXIS_LABEL,
                titlefont_size=params.AXIS_FONT_SIZE,
                tickfont_size=params.TICK_FONT_SIZE,
            ),
            template=params.TEMPLATE,
        )
        return fig

    def get_frequent(self, n_head: int = 20) -> pd.DataFrame:
        """Return the Pandas dataframe containing the occurrences and percentage of the top n_head most frequent values."""
        return (
            pd.concat([self._get_occurrences(), self._get_percentages()], axis=1)
            .rename_axis("value")
            .sort_values(by="occurrence", ascending=False)
            .head(n_head)
            .reset_index()
        )
