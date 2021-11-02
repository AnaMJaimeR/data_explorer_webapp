from dataclasses import dataclass
from typing import Union

import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from src.settings import FormatHistogram


@dataclass
class NumericColumn:
    """
    Class for storing and displaying information of a numeric column

    Attributes
    ----------
    col_name: str
        Name of the numeric pandas column

    serie: pd.Series
        Series containing the data of the numeric pandas column
    """

    col_name: str
    serie: pd.Series

    def get_name(self) -> str:
        """Return name of selected column"""
        return self.col_name

    def get_unique(self) -> int:
        """Return number of unique values for selected column"""
        return self.serie.nunique()

    def get_missing(self) -> int:
        """Return number of missing values for selected column"""
        return int(self.serie.isna().sum())

    def get_zeros(self) -> int:
        """Return number of occurrence of 0 value for selected column"""
        return int((self.serie == 0).sum())

    def get_negatives(self) -> int:
        """Return number of negative values for selected column"""
        return int((self.serie < 0).sum())

    def get_mean(self) -> float:
        """Return the average value for selected column"""
        return self.serie.mean()

    def get_std(self) -> float:
        """Return the standard deviation value for selected column"""
        return self.serie.std()

    def get_min(self) -> Union[int, float]:
        """Return the minimum value for selected column"""
        return self.serie.min()

    def get_max(self) -> Union[int, float]:
        """Return the maximum value for selected column"""
        return self.serie.max()

    def get_median(self) -> Union[int, float]:
        """Return the median value for selected column"""
        return self.serie.median()

    def _get_occurrences(self) -> pd.Series:
        """Return the occurrences per value for selected column"""
        return self.serie.value_counts().rename("occurrence")

    def _get_percentages(self) -> pd.Series:
        """Return the normalised occurrences per value for selected column"""
        return (
            self.serie.value_counts(normalize=True)
            .round(decimals=4)
            .rename("percentage")
        )

    def get_histogram(
        self,
        params: FormatHistogram,
    ) -> Figure:
        """Return the generated histogram for selected column"""
        fig = px.histogram(
            self._get_occurrences(), x="occurrence", nbins=params.MAX_BINS
        )
        fig.update_layout(
            title=params.TITLE,
            xaxis=dict(
                title=f"{self.col_name} (binned)",
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
        """Return the Pandas dataframe containing the occurrences and percentage of the top n_head most frequent values"""
        return (
            pd.concat([self._get_occurrences(), self._get_percentages()], axis=1)
            .rename_axis("value")
            .sort_values(by="occurrence", ascending=False)
            .head(n_head)
            .reset_index()
        )
