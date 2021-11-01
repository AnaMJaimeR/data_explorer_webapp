from typing import Dict, Union

from driconfig import DriConfig
from pydantic import BaseModel

from src import __version__


class FormatPlots(BaseModel):
    """Model for the `FORMAT_PLOTS` configuration."""

    AXIS_FONT_SIZE: int
    TICK_FONT_SIZE: int
    TEMPLATE: str


class ParamsSections(BaseModel):
    """Model for the `TEXT_COLS`, `DATE_COLS` and `NUMERIC_COLS` configuration."""

    TOP_FREQUENCY: int
    DROP_NA: bool
    PLOT: Dict[str, Union[str, int]]


class AppConfig(DriConfig):
    """Interface for the settings.yml file."""

    class Config:
        """Configure the YML file location."""

        config_folder = "./config"
        config_file_name = "parameters.yml"

    VERSION: str = __version__
    APP_NAME: str
    FORMAT_PLOTS: FormatPlots
    TEXT_COLS: ParamsSections
    DATE_COLS: ParamsSections
    NUMERIC_COLS: ParamsSections
