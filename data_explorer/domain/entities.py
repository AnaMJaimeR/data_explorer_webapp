from abc import ABC, abstractmethod


class Section(ABC):
    """Section of the application."""

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def render(self) -> None:
        """Render the content of the sections."""
        pass

    @property
    def name(self) -> str:
        """Return the name of the section."""
        return self._name
