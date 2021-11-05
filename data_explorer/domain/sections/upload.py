import streamlit as st
from data_explorer.domain.entities import Section


class UploadSection(Section):
    """
    Class that stores the content of the upload section.

    Attributes
    ----------
    button_text : str
        Text to be displayed in the upload button.
    """

    def __init__(self, button_text: str = "Choose a CSV file"):
        self._name = "Upload"
        self._button_text = button_text
        self._loaded_file = None

    def render(self) -> None:
        """Render the upload section."""
        self._loaded_file = st.file_uploader(self._button_text, type="csv")

    @property
    def loaded_file(self) -> st.uploaded_file_manager.UploadedFile:
        """Return the uploaded file object."""
        return self._loaded_file
