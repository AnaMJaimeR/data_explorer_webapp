import pandas as pd
import streamlit as st
from data_explorer.domain.entities import Section
from data_explorer.domain.sections.data import Dataset
from src.text import TextColumn


class TextSection(Section):
    """
    Class that stores the content of the text section.

    Attributes (TODO!!)
    ----------

    header : str, default = "3. Information on text columns"
        Section header.
    """

    def __init__(
        self,
        dataset: Dataset,
        params: dict,
        header: str = "3. Information on text columns",
    ):
        self._header = header
        self._processed_df = dataset
        self._n_head = params.get("TOP_FREQUENCY")
        self._dropna = params.get("DROP_NA")
        self._plot_params = params.get("PLOT")

    def render(self) -> None:
        """Render the text section."""

        # Header
        st.header(self._header)

        for col in self._processed_df.get_text_columns():
            textcol = TextColumn(col, self._processed_df.df[col])

            # Display name of column as subtitle
            st.markdown(
                f"**3.3 Field Name:** {textcol.get_name()}"
            )  # TODO: check subtitle

            # Display information about the text column
            text_column_values = {
                "Number of unique values": textcol.get_unique(),
                "Number of rows with missing values": textcol.get_missing(),
                "Number of empty rows": textcol.get_empty(),
                "Number of rows with only whitespaces": textcol.get_whitespace(),
                "Number of rows with only lowercases": textcol.get_lowercase(),
                "Number of rows with only uppercases": textcol.get_uppercase(),
                "Number of rows with only alphabet": textcol.get_alphabet(),
                "Number of rows with only digitss": textcol.get_digit(),
                "Mode Value": textcol.get_mode(dropna=self._dropna),
            }
            st.dataframe(
                pd.Series(text_column_values, name="value")
            )  # TODO: check if possible to pass a serie
            # st.dataframe(pd.DataFrame(pd.Series(text_column_values, name="value")))

            # Display a bar chart showing the number of occurrence for each value
            st.plotly_chart(textcol.get_barchart(self, params=self._plot_params))

            # Display a table listing the frequencies and percentage for each value
            st.write("**Most Frequent values**")
            st.dataframe(textcol.get_frequent(n_head=self._n_head))
