import pandas as pd
import streamlit as st
from data_explorer.domain.entities import Section
from src.data import Dataset
from src.datetime import DateColumn
from src.settings import ParamsSections


class DatetimeSection(Section):
    """
    Class that stores the content of the datetime section.

    Attributes
    ----------
    dataset : DataSet
        Dataset object with the transformed dataframe.
    params: ParamsSections
        Object with the parameters for the datetime section.
    header : str, default = "4. Information on datetime columns"
        Section header.
    """

    def __init__(
        self,
        dataset: Dataset,
        params: ParamsSections,
        header: str = "4. Information on datetime columns",
    ):
        self._name = "Datetime"
        self._header = header
        self._params = params
        self._dataset = dataset

    def render(self) -> None:
        """Render the datetime section."""

        # Header
        st.header(self._header)

        for n, col in enumerate(self._dataset.get_date_columns()):
            date_col = DateColumn(col, self._dataset.df[col])

            # Subheader
            st.subheader(f"4.{n} Field Name: {date_col.get_name()}")

            # Display table with metrics
            st.dataframe(
                pd.Series(
                    {
                        "Number of Unique Values": date_col.get_unique(),
                        "Number of Rows with Missing Values": date_col.get_missing(),
                        "Number of Weekend Dates": date_col.get_weekend(),
                        "Number of Weekday Dates": date_col.get_weekday(),
                        "Number of Dates in Future": date_col.get_future(),
                        "Number of Rows with 1900-01-01": date_col.get_empty_1900(),
                        "Number of Rows with 1970-01-01": date_col.get_empty_1970(),
                        "Minimun Value": date_col.get_min(),
                        "Maximun Value": date_col.get_max(),
                    },
                    name="value",
                )
            )

            # Display the Bar chart
            st.plotly_chart(date_col.get_barchart(self._params.PLOT))

            # Display most frequent values
            st.write("**Most Frequent Values**")
            st.dataframe(date_col.get_frequent(self._params.TOP_FREQUENCY))
