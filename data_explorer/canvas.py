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
        dataset = overall_section.processed_dataset

        # numeric_section = NumericSection(
        #     dataset=dataset,
        #     params={**self._parameters.get("FORMAT_PLOTS"), **self._parameters.get("NUMERIC_COLS")},
        # )
        # numeric_section.render()

        # text_section = TextSection(
        #     dataset=dataset,
        #     params={**self._parameters.get("FORMAT_PLOTS"), **self._parameters.get("TEXT_COLS")},
        # )
        # text_section.render()

        # date_section = DateSection(
        #     dataset=dataset,
        #     params={**self._parameters.get("FORMAT_PLOTS"), **self._parameters.get("DATE_COLS")},
        # )
        # date_section.render()
