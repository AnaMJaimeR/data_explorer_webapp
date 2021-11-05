from typing import Union

from driconfig import DriConfig
from pydantic import BaseModel

from src import __version__


class FormatPlot(BaseModel):
    """Model for plots configuration."""

    AXIS_FONT_SIZE: int
    TICK_FONT_SIZE: int
    TEMPLATE: str
    TITLE: str

    class Config:
        """Configuring BaseModel"""

        allow_mutation = False


class FormatBarPlot(FormatPlot):
    """Model for the barplot configuration."""

    CATEGORY_ORDER: str
    Y_AXIS_LABEL: str


class FormatHistogram(FormatPlot):
    """Model for the histogram configuration."""

    Y_AXIS_LABEL: str
    MAX_BINS: int


class ParamsSections(BaseModel):
    """Model for the `TEXT_COLS`, `DATE_COLS` and `NUMERIC_COLS` configuration."""

    TOP_FREQUENCY: int
    DROP_NA: bool
    PLOT: Union[FormatBarPlot, FormatHistogram]

    class Config:
        """Configuring BaseModel"""

        allow_mutation = False


class AppConfig(DriConfig):
    """Interface for the settings.yml file."""

    class Config:
        """Configure the YML file location."""

        config_folder = "./config"
        config_file_name = "parameters.yml"
        allow_mutation = False

    VERSION: str = __version__
    APP_NAME: str
    TEXT_COLS: ParamsSections
    DATE_COLS: ParamsSections
    NUMERIC_COLS: ParamsSections
