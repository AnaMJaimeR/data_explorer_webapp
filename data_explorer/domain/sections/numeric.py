import pandas as pd
import streamlit as st
from data_explorer.domain.entities import Section
from src.data import Dataset
from src.numeric import NumericColumn
from src.settings import ParamsSections


class NumericSection(Section):
    """
    Class that stores the content of the numeric section.

    Attributes
    ----------
    dataset : DataSet
        Dataset object with the transformed dataframe.

    params: ParamsSections
        Object with the parameters for the numeric section.

    header : str, default = "1. Overall Information"
        Section header.
    """

    def __init__(
        self,
        dataset: Dataset,
        params: ParamsSections,
        header: str = "2. Numeric Column Information",
    ):

        self._name = "Numeric"
        self._header = header
        self._params = params
        self._dataset = dataset

    def render(self) -> None:
        """Render the numeric section."""

        # Header
        st.header(self._header)

        for n, col in enumerate(self._dataset.get_numeric_columns()):
            num_col = NumericColumn(col, self._dataset.df[col])

            # Subheader
            st.subheader(f"2.{n} Field Name: *{num_col.get_name()}*")

            # Display table with metrics
            st.dataframe(
                pd.Series(
                    {
                        "Number of Unique Values": num_col.get_unique(
                            self._params.DROP_NA
                        ),
                        "Number of Rows with Missing Values": num_col.get_missing(),
                        "Number of Rows with 0": num_col.get_zeros(),
                        "Number of Rows with Negative Values": num_col.get_negatives(),
                        "Average Value": num_col.get_mean(),
                        "Standard Deviation Value": num_col.get_std(),
                        "Minimum Value": num_col.get_min(),
                        "Maximum Value": num_col.get_max(),
                        "Median Value": num_col.get_median(),
                    },
                    name="value",
                )
            )

            # Display histogram
            st.plotly_chart(num_col.get_histogram(self._params.PLOT))

            # Display most frequent values
            st.write("**Most Frequent Values**")
            st.dataframe(
                num_col.get_frequent(self._params.TOP_FREQUENCY, self._params.DROP_NA)
            )

            # Add a horizontal rule
            st.markdown("---")
