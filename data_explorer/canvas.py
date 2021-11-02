import streamlit as st
from src.settings import AppConfig

from data_explorer.domain.sections.data import OverallSection
from data_explorer.domain.sections.upload import UploadSection


class Canvas:
    """
    Class defining the structure of the application.

    Attributes
    ----------
    params : AppConfig
        Class with the parameters to create the application.

    Methods
    ----------
    build()
        Render each one of the sections.
    """

    def __init__(self, params: AppConfig):
        self._title = params.APP_NAME
        self._version = params.VERSION
        self._parameters = params

    def build(self) -> None:
        """Render each one of the sections."""
        st.title(self._title)
        upload_section = UploadSection()
        upload_section.render()

        if upload_section.loaded_file is None:
            return None

        overall_section = OverallSection(upload_section.loaded_file)
        overall_section.render()

        # numeric_section = NumericSection(
        #     df=overall_section.numeric_columns,
        #     params={**self._parameters.FORMAT_PLOTS, **self._parameters.NUMERIC_COLS},
        # )
        # numeric_section.render()

        # text_section = TextSection(
        #     df=overall_section.text_columns,
        #     params={**self._parameters.FORMAT_PLOTS, **self._parameters.TEXT_COLS},
        # )
        # text_section.render()

        # date_section = DateSection(
        #     df=overall_section.date_columns,
        #     params={**self._parameters.FORMAT_PLOTS, **self._parameters.DATE_COLS},
        # )
        # date_section.render()
