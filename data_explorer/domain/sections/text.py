import pandas as pd
import streamlit as st
from data_explorer.domain.entities import Section
from src.data import Dataset
from src.settings import ParamsSections
from src.text import TextColumn


class TextSection(Section):
    """
    Class that stores the content of the text section.

    Attributes
    ----------
    dataset : DataSet
        Dataset object with the transformed dataframe.
    params: ParamsSections
        Object with the parameters for the datetime section.
    header : str, default = "3. Information on text columns"
        Section header.
    """

    def __init__(
        self,
        dataset: Dataset,
        params: ParamsSections,
        header: str = "3. Information on text columns",
    ):
        self._name = "Text"
        self._header = header
        self._params = params
        self._dataset = dataset

    def render(self) -> None:
        """Render the text section."""

        # Header
        st.header(self._header)

        for n, col in enumerate(self._dataset.get_text_columns()):
            text_col = TextColumn(col, self._dataset.df[col])

            # Subheader
            st.subheader(f"3.{n} Field Name: {text_col.get_name()}")

            # Display table with metrics
            st.dataframe(
                pd.Series(
                    {
                        "Number of Unique Values": text_col.get_unique(),
                        "Number of Rows with Missing Values": text_col.get_missing(),
                        "Number of Empty Rows": text_col.get_empty(),
                        "Number of Rows with Only Whitespace": text_col.get_whitespace(),
                        "Number of Rows with Only Lowercases": text_col.get_lowercase(),
                        "Number of Rows with Only Uppercases": text_col.get_uppercase(),
                        "Number of Rows with Only Alphabet": text_col.get_alphabet(),
                        "Number of Rows with only Digitss": text_col.get_digit(),
                        "Mode Value": text_col.get_mode(dropna=self._params.DROP_NA),
                    },
                    name="value",
                )
            )

            # Display the Bar chart
            st.plotly_chart(text_col.get_barchart(self._params.PLOT))

            # Display most frequent values
            st.write("**Most Frequent Values**")
            st.dataframe(text_col.get_frequent(self._params.TOP_FREQUENCY))
