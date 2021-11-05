import unittest
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pandas.api.types as ptypes
from plotly.graph_objs._figure import Figure
from src.settings import FormatBarPlot, ParamsSections
from src.text import TextColumn


class TestMethodsText(ABC):
    """Class containing the tests for the methods of the TextColumn class."""

    @abstractmethod
    def setUp(self) -> None:
        pass

    @abstractmethod
    def tearDown(self) -> None:
        pass

    def test_init(self) -> None:
        """Test that the instantiated class is TextColumn type."""

        # Assert: type of instantiated class
        self.assertIsInstance(self.text_class, TextColumn)

    def test_get_column_name(self):
        """Test that the TextColumn name is the correct one."""

        # Expected
        expected = self.expected_name

        # Act
        result = self.text_class.get_name()

        # Assert: type of output
        self.assertIsInstance(result, str)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_unique(self):
        """Test that the number of unique values for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_unique

        # Act
        result = self.text_class.get_unique()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_missing(self):
        """Test that the number of missing values for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_missing

        # Act
        result = self.text_class.get_missing()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_empty(self):
        """Test that the number of empty rows for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_empty

        # Act
        result = self.text_class.get_empty()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_whitespace(self):
        """Test that the number of rows with only whitespace for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_whitespace

        # Act
        result = self.text_class.get_whitespace()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_lowercase(self):
        """Test that the number of rows with only lower cases characters for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_lowercase

        # Act
        result = self.text_class.get_lowercase()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_uppercase(self):
        """Test that the number of rows with only upper cases characters for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_uppercase

        # Act
        result = self.text_class.get_uppercase()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_alphabet(self):
        """Test that the number of rows with only alphabet characters for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_alphabet

        # Act
        result = self.text_class.get_alphabet()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_digit(self):
        """Test that the number of rows with only numbers as characters for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_digit

        # Act
        result = self.text_class.get_digit()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_mode(self):
        """Test that the mode value for the TextColumn is the correct one."""

        # Expected
        expected = self.expected_get_mode

        # Act
        result = self.text_class.get_mode()

        # Assert: type of output
        self.assertIsInstance(result, str)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_barchart(self):
        """Test that the output class is Figure type."""

        # Act
        result = self.text_class.get_barchart(params=self.params.PLOT)

        # Assert: type of output
        self.assertIsInstance(result, Figure)

    def test_get_frequent(self):
        """Test that the generated dataframe is the correct one."""

        # Expected
        expected_columns = ["value", "occurrence", "percentage"]
        expected_length = self.expected_length

        # Act
        result = self.text_class.get_frequent(n_head=self.params.TOP_FREQUENCY)

        # Assert: type of output
        self.assertIsInstance(result, pd.DataFrame)
        # Assert: dtype of columns
        assert ptypes.is_string_dtype(result.value)
        assert ptypes.is_numeric_dtype(result.occurrence)
        assert ptypes.is_numeric_dtype(result.percentage)
        # Assert: column names
        self.assertListEqual(result.columns.tolist(), expected_columns)
        # Assert: length
        self.assertEqual(len(result), expected_length)


class TestMethodsValidTextColumn(TestMethodsText, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of valid serie as input."""

    def setUp(self) -> None:
        """Setting an empty dataframe to be tested before each test"""

        # Instantiated TextColumn class and parameters
        self.serie = pd.Series(
            [
                "",
                "cc",
                "cc",
                "  ",
                "saaS",
                "DDWW",
                "cccc ccc",
                "123",
                "ff",
                "ff",
                " ",
                np.nan,
            ],
            name="this_is_the_serie_name",
        )
        self.text_class = TextColumn("this_is_the_serie_name", self.serie)
        self.params = ParamsSections(
            DROP_NA=True,
            TOP_FREQUENCY=5,
            PLOT=FormatBarPlot(
                Y_AXIS_LABEL="y_axis_label",
                AXIS_FONT_SIZE=14,
                TICK_FONT_SIZE=16,
                CATEGORY_ORDER="total descending",
                TEMPLATE="simple_white",
                TITLE="title",
            ),
        )

        # Expected
        self.expected_name = "this_is_the_serie_name"
        self.expected_get_unique = 9
        self.expected_get_missing = 1
        self.expected_get_empty = 1
        self.expected_get_whitespace = 2
        self.expected_get_lowercase = 5
        self.expected_get_uppercase = 1
        self.expected_get_alphabet = 6
        self.expected_get_digit = 1
        self.expected_get_mode = "cc"
        self.expected_length = 5

    def tearDown(self) -> None:
        """Delete the variables after each test"""

        del (
            self.serie,
            self.text_class,
            self.params,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_missing,
            self.expected_get_empty,
            self.expected_get_whitespace,
            self.expected_get_lowercase,
            self.expected_get_uppercase,
            self.expected_get_alphabet,
            self.expected_get_digit,
            self.expected_get_mode,
            self.expected_length,
        )

    def test_valid_get_frequent(self):

        # Expected
        expected_maximum_occurrence = 2
        expected_minimum_occurrence = 1
        expected_upper_bound_perc = 1

        # Act
        result = self.text_class.get_frequent(n_head=self.params.TOP_FREQUENCY)

        # Assert: sorted by occurrence (descending)
        self.assertEqual(result.occurrence.iloc[0], expected_maximum_occurrence)
        self.assertEqual(result.occurrence.iloc[-1], expected_minimum_occurrence)
        # Assert: upper bound for sum of percentages
        self.assertLessEqual(result.percentage.sum(), expected_upper_bound_perc)


if __name__ == "__main__":
    unittest.main()
