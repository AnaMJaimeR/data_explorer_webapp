from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from src.settings import FormatBarPlot


@dataclass
class DateColumn:
    """
    Class for storing and showing information about a date column.

     Attributes
     ----------
     col_name : str
         Name of the datetime pandas column.

     serie : pd.Series
         Series containing the data of the datetime pandas column.
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

    def get_weekend(self) -> int:
        """Return number of occurrence of days falling during weekend (Saturday and Sunday)."""
        return int(self.serie.dt.weekday.isin([5, 6]).sum())

    def get_weekday(self) -> int:
        """Return number of weekday days (not Saturday or Sunday)."""
        return int(self.serie.dt.weekday.isin([0, 1, 2, 3, 4]).sum())

    def get_future(self) -> int:
        """Return number of cases with future dates (after today)."""
        return int((self.serie > datetime.today()).sum())

    def get_empty_1900(self) -> int:
        """Return number of occurrence of 1900-01-01 value."""
        return int((self.serie.dt.date == pd.Timestamp(1900, 1, 1)).sum())

    def get_empty_1970(self) -> int:
        """Return number of occurrence of 1970-01-01 value."""
        return int((self.serie.dt.date == pd.Timestamp(1970, 1, 1)).sum())

    def get_min(self) -> datetime:
        """Return the minimum date."""
        return self.serie.min()

    def get_max(self) -> datetime:
        """Return the maximum date."""
        return self.serie.max()

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
        fig = px.bar(self._get_occurrences())
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
            showlegend=False,
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
