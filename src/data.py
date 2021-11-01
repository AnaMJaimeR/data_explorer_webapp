from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd


@dataclass
class Dataset:
    """
    Class for storing and show display information about a DataFrame.

    Attributes
    ----------
    name : str
        Name of the DataFrame.

    df : pd.DataFrame
        Pandas DataFrame.
    """

    name: str
    df: pd.DataFrame

    def get_name(self) -> str:
        """Return filename of loaded dataset."""
        return self.name

    def get_n_rows(self) -> int:
        """Return number of rows of loaded dataset."""
        return self.df.shape[0]

    def get_n_cols(self) -> int:
        """Return number of columns of loaded dataset."""
        return self.df.shape[1]

    def get_cols_list(self) -> List[str]:
        """Return list column names of loaded dataset"""
        return self.df.columns.tolist()

    def get_cols_dtype(self) -> Dict[str, str]:
        """Return dictionary with column name as keys and data type as values."""
        return self.df.dtypes.astype(str).to_dict()

    def get_n_duplicates(self) -> int:
        """Return number of duplicated rows of loaded dataset."""
        return int(self.df.duplicated().sum())

    def get_n_missing(self) -> int:
        """Return number of rows with missing values of loaded dataset."""
        return int(self.df.isnull().any(axis=1).sum())

    def get_head(self, n=5) -> pd.DataFrame:
        """Return Pandas Dataframe with top rows of loaded dataset."""
        return self.df.head(n)

    def get_tail(self, n=5) -> pd.DataFrame:
        """Return Pandas Dataframe with bottom rows of loaded dataset."""
        return self.df.tail(n)

    def get_sample(self, n=5):
        """Return Pandas Dataframe with random sampled rows of loaded dataset."""
        return self.df.sample(n)

    def get_numeric_columns(self) -> List[str]:
        """Return list column names of numeric type from loaded dataset."""
        return self.df.select_dtypes(np.number).columns.tolist()

    def get_text_columns(self) -> List[str]:
        """Return list column names of text type from loaded dataset."""
        return self.df.select_dtypes(object).columns.tolist()

    def get_date_columns(self) -> List[str]:
        """Return list column names of datetime type from loaded dataset."""
        return self.df.select_dtypes(np.datetime64).columns.tolist()

    def convert_to_datetime(self, columns: List[str]) -> pd.DataFrame:
        """Convert the given columns to datetime if possible."""
        return pd.concat(
            [
                self.df.drop(columns, axis=1),
                self.df[columns].apply(pd.to_datetime, errors="ignore"),
            ],
            axis=1,
        ).reindex(columns=self.df.columns)
