import pandas as pd
import streamlit as st
from data_explorer.domain.entities import Section
from src.data import Dataset


class OverallSection(Section):
    """
    Class that stores the content of the overall section.

    Attributes
    ----------
    loaded_file : st.uploaded_file_manager.UploadedFile.
        Uploaded file object to use as the dataframe source.

    header : str, default = "1. Overall Information"
        Section header.

    slider_text: str, default = "Select the number of rows to be displayed"
        Text to be displayed on the slider widget.

    min_slider: int, default 5
        Min value of the slider.

    max_slider: int, default 50
        Max value of the slider.

    multiselect_title: str, default = "Which columns do you want to convert to dates?"
        Text to be displayed on the multiselect widget.
    """

    def __init__(
        self,
        loaded_file: st.uploaded_file_manager.UploadedFile,
        header: str = "1. Overall Information",
        slider_text: str = "Select the number of rows to be displayed",
        min_slider: int = 5,
        max_slider: int = 50,
        multiselect_title: str = "Which columns do you want to convert to dates?",
    ):
        self._name = "Overall"
        self._header = header
        self._slider_text = slider_text
        self._min_slider = min_slider
        self._max_slider = max_slider
        self._multiselect_title = multiselect_title
        self._raw_df = Dataset(loaded_file.name, pd.read_csv(loaded_file))
        self._processed_df = None

    def render(self) -> None:
        """Render the overall section."""

        # Header
        st.header(self._header)

        # Description
        st.write(f"**Name of Table:** {self._raw_df.get_name()}")
        st.write(f"**Number of Rows:** {self._raw_df.get_n_rows():,.0f}")
        st.write(f"**Number of Columns:** {self._raw_df.get_n_cols():,.0f}")
        st.write(
            f"**Number of Duplicated Rows:** {self._raw_df.get_n_duplicates():,.0f}"
        )
        st.write(
            f"**Number of Rows with Missing Values:** {self._raw_df.get_n_missing():,.0f}"
        )

        # List of columns
        st.write("**List of Columns:**")
        st.write(", ".join(self._raw_df.get_cols_list()))

        # Type of columns
        st.write("**Type of Columns:**")
        st.dataframe(pd.Series(self._raw_df.get_cols_dtype(), name="type"))

        # Select number of rows
        n_rows = st.slider(
            label=self._slider_text,
            min_value=self._min_slider,
            max_value=self._max_slider,
        )

        # Display top n rows of dataframe
        st.write("**Top Rows of Table**")
        st.dataframe(self._raw_df.get_head(n=n_rows))

        # Display bottom n rows of dataframe
        st.write("**Bottom Rows of Table**")
        st.dataframe(self._raw_df.get_tail(n=n_rows))

        # Display sample n rows of dataframe
        st.write("**Random Sample Rows of Table**")
        st.dataframe(self._raw_df.get_sample(n=n_rows))

        # Select datetime columns
        selection = st.multiselect(
            label=self._multiselect_title, options=self._raw_df.get_text_columns()
        )
        self._processed_df = self._raw_df.convert_to_datetime(selection)

    @property
    def processed_df(self) -> pd.DataFrame:
        """Return the dataframe with the selected columns as datetime type."""
        return self._processed_df
