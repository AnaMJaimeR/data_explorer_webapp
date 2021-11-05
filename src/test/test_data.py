import unittest
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pandas.testing as pd_testing
from src.data import Dataset


class TestMethodsDataset(ABC):
    """Test the methods of Dataset with a given input dataframe."""

    @abstractmethod
    def setUp(self) -> None:
        pass

    @abstractmethod
    def tearDown(self) -> None:
        pass

    def test_init(self) -> None:
        """Test that the dataset is Dataset type."""
        self.assertIsInstance(self.dataset, Dataset)

    def test_get_name(self) -> None:
        """Test that the Dataset name is the correct one."""

        # Expected
        expected = self.df_name

        # Act
        result = self.dataset.get_name()

        # Assert: type of output
        self.assertIsInstance(result, str)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_n_rows(self) -> None:
        """Test that the Dataset number of rows is the correct one."""

        # Expected
        expected = self.rows

        # Act
        result = self.dataset.get_n_rows()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_n_cols(self) -> None:
        """Test that the Dataset number of columns is the correct one."""

        # Expected
        expected = self.columns

        # Act
        result = self.dataset.get_n_cols()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_cols_dtypes(self) -> None:
        """Test that the Dataset dtypes are the correct ones."""

        # Expected
        expected = self.dtypes

        # Act
        result = self.dataset.get_cols_dtype()

        # Assert: type of output
        self.assertIsInstance(result, dict)
        # Assert: expected result
        self.assertDictEqual(result, expected)

    def test_get_n_duplicates(self) -> None:
        """Test that the Dataset number of duplicates is the correct one."""

        # Expected
        expected = self.duplicates

        # Act
        result = self.dataset.get_n_duplicates()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_n_missing(self) -> None:
        """Test that the number of rows with missing values is the correct one."""

        # Expected
        expected = self.missings

        # Act
        result = self.dataset.get_n_missing()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_df_get_head(self) -> None:
        """Test that the Dataset head is the correct one."""

        # Expected
        if len(self.df) < self.n:
            expected = self.df
        else:
            expected = self.df.iloc[: self.n, :]

        # Act
        result = self.dataset.get_head(self.n)

        # Assert: type of output
        self.assertIsInstance(result, pd.DataFrame)
        # Assert: expected result
        pd_testing.assert_frame_equal(result, expected)

    def test_len_get_head(self) -> None:
        """Test that the Dataset head shape is the correct one."""

        # Expected
        if len(self.df) < self.n:
            expected = self.df.shape
        else:
            expected = self.df.iloc[: self.n].shape

        # Act
        result = self.dataset.get_head(self.n).shape

        # Assert: type of output
        self.assertIsInstance(result, tuple)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_df_get_tail(self) -> None:
        """Test that the Dataset tail is the correct one."""

        # Expected
        if len(self.df) < self.n:
            expected = self.df
        else:
            expected = self.df.iloc[-self.n :]

        # Act
        result = self.dataset.get_tail(self.n)

        # Assert: type of output
        self.assertIsInstance(result, pd.DataFrame)
        # Assert: expected result
        pd_testing.assert_frame_equal(result, expected)

    def test_len_get_tail(self) -> None:
        """Test that the Dataset tail shape is the correct one."""

        # Expected
        if len(self.df) < self.n:
            expected = self.df.shape
        else:
            expected = self.df.iloc[-self.n :].shape

        # Act
        result = self.dataset.get_tail(self.n).shape

        # Assert: type of output
        self.assertIsInstance(result, tuple)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_df_get_sample(self) -> None:
        """Test that the Dataset sample type is the correct one."""

        # Act
        result = self.dataset.get_sample(self.n)

        # Assert: type of output
        self.assertIsInstance(result, pd.DataFrame)

    def test_len_get_sample(self) -> None:
        """Test that the Dataset sample shape is the correct one."""

        # Expected
        if len(self.df) < self.n:
            expected = (len(self.df), len(self.df.columns))
        else:
            expected = (self.n, len(self.df.columns))

        # Act
        result = self.dataset.get_sample(self.n).shape

        # Assert: type of output
        self.assertIsInstance(result, tuple)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_numeric_colums(self) -> None:
        """Test that the Dataset numeric columns are the correct ones."""

        # Expected
        expected = self.num_cols

        # Act
        result = self.dataset.get_numeric_columns()

        # Assert: type of output
        self.assertIsInstance(result, list)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_text_colums(self) -> None:
        """Test that the Dataset text columns are the correct ones."""

        # Expected
        expected = self.text_cols

        # Act
        result = self.dataset.get_text_columns()

        # Assert: type of output
        self.assertIsInstance(result, list)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_date_colums(self) -> None:
        """Test that the Dataset date columns are the correct ones."""

        # Expected
        expected = self.date_cols

        # Act
        result = self.dataset.get_date_columns()

        # Assert: type of output
        self.assertIsInstance(result, list)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_type_convert_to_datetime(self):
        """Test that the output DataFrame after conversion has the columns as datetime."""

        # Expected
        expected = {col: np.dtype("M8[ns]") for col in self.string_to_date_cols}

        result = self.dataset.convert_to_datetime(self.string_to_date_cols)[
            self.string_to_date_cols
        ].dtypes.to_dict()

        # Assert: expected result
        self.assertDictEqual(result, expected)

    def test_output_convert_to_datetime(self):
        """Test that the output DataFrame is equal to the raw one without the converted datetime column."""

        # Expected
        expected = self.df.drop(self.string_to_date_cols, axis=1)

        result = self.dataset.convert_to_datetime(self.string_to_date_cols).drop(
            self.string_to_date_cols, axis=1
        )

        # Assert: expected result
        pd_testing.assert_frame_equal(result, expected)


class TestEmptyDataFrame(TestMethodsDataset, unittest.TestCase):
    """Test the methods of Dataset with an empty dataframe as input."""

    def setUp(self) -> None:
        """Setting an empty dataframe to be tested before each test"""

        # Instantiated Dataset class and parameters
        self.df = pd.DataFrame()
        self.df_name = "this_is_the_dataframe_filename"
        self.dataset = Dataset(self.df_name, self.df)

        # Condition test
        self.string_to_date_cols = []
        self.n = 5

        # Expected
        self.dtypes = {}
        self.rows = 0
        self.columns = 0
        self.duplicates = 0
        self.missings = 0
        self.num_cols = []
        self.text_cols = []
        self.date_cols = []

    def tearDown(self) -> None:
        """Delete the variables after each test"""
        del (
            self.df,
            self.df_name,
            self.dataset,
            self.string_to_date_cols,
            self.n,
            self.dtypes,
            self.rows,
            self.columns,
            self.duplicates,
            self.missings,
            self.num_cols,
            self.text_cols,
            self.date_cols,
        )


class TestCompleteDataFrame(TestMethodsDataset, unittest.TestCase):
    """Test the methods of Dataset with a regular dataframe as input."""

    def setUp(self) -> None:
        """Setting a regular dataframe to be tested before each test"""

        # Instantiated Dataset class and parameters
        self.df = pd.DataFrame(
            {
                "int_col": pd.array([1, 1, 3, 2, 4, np.nan], dtype="Int64"),
                "float_col": pd.array(
                    [0.1, 0.1, 0.4, np.nan, 1.0, 3.0], dtype="float64"
                ),
                "object_col": pd.array(
                    ["a", "a", "1a", "1", np.nan, "b"], dtype="object"
                ),
                "date_raw_col": pd.array(
                    [
                        "2021-01-01",
                        "2021-01-01",
                        "2020-03-02",
                        np.nan,
                        "2020-02-01",
                        "2020-12-01",
                    ],
                    dtype="object",
                ),
                "date_col": pd.array(
                    [
                        "2021-01-01",
                        "2021-01-01",
                        "2020-03-02",
                        np.nan,
                        "2020-02-01",
                        "2020-12-01",
                    ],
                    dtype="datetime64[ns]",
                ),
            }
        )
        self.df_name = "this_is_the_dataframe_filename"
        self.dataset = Dataset(self.df_name, self.df)

        # Condition test
        self.string_to_date_cols = ["date_raw_col"]
        self.n = 5

        # Expected
        self.dtypes = {
            "int_col": "Int64",
            "float_col": "float64",
            "object_col": "object",
            "date_raw_col": "object",
            "date_col": "datetime64[ns]",
        }
        self.rows = 6
        self.columns = 5
        self.duplicates = 1
        self.missings = 3
        self.num_cols = ["int_col", "float_col"]
        self.text_cols = ["object_col", "date_raw_col"]
        self.date_cols = ["date_col"]

    def tearDown(self) -> None:
        """Delete the variables after each test"""
        del (
            self.df,
            self.df_name,
            self.dataset,
            self.string_to_date_cols,
            self.n,
            self.dtypes,
            self.rows,
            self.columns,
            self.duplicates,
            self.missings,
            self.num_cols,
            self.text_cols,
            self.date_cols,
        )


if __name__ == "__main__":
    unittest.main()
