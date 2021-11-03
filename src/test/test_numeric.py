import math
import unittest
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pandas.api.types as ptypes
from plotly.graph_objs._figure import Figure
from src.numeric import NumericColumn
from src.settings import FormatHistogram, ParamsSections


class TestMethodsNumeric(ABC):
    """Class containing the tests for the methods of the NumericColumn class."""

    @abstractmethod
    def setUp(self) -> None:
        pass

    @abstractmethod
    def tearDown(self) -> None:
        pass

    def test_init(self) -> None:
        """Test that the instantiated class is NumericColumn type."""

        # Assert: type of instantiated class
        self.assertIsInstance(self.numeric_class, NumericColumn)

    def test_get_column_name(self):
        """Test that the NumericColumn name is the correct one."""

        # Expected
        expected = self.expected_name

        # Act
        result = self.numeric_class.get_name()

        # Assert: type of output
        self.assertIsInstance(result, str)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_unique(self):
        """Test that the number of unique values for the NumericColumn is the correct one."""

        # Expected
        expected = self.expected_get_unique

        # Act
        result = self.numeric_class.get_unique()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_missing(self):
        """Test that the number of missing values for the NumericColumn is the correct one."""

        # Expected
        expected = self.expected_get_missing

        # Act
        result = self.numeric_class.get_missing()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_zeros(self):
        """Test that the number of zeros for the NumericColumn is the correct one."""

        # Expected
        expected = self.expected_get_zeros

        # Act
        result = self.numeric_class.get_zeros()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_negatives(self):
        """Test that the number of negative values for the NumericColumn is the correct one."""

        # Expected
        expected = self.expected_negatives

        # Act
        result = self.numeric_class.get_negatives()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_mean(self):
        """Test that the mean value for the NumericColumn is the correct one."""

        # Act
        result = self.numeric_class.get_mean()

        # Assert: type of output
        self.assertIsInstance(result, float)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(math.isnan(result))
        else:
            # Expected
            expected = self.expected_mean
            self.assertEqual(result, expected)

    def test_get_std(self):
        """Test that the standard deviation value for the NumericColumn is the correct one."""

        # Act
        result = self.numeric_class.get_std()

        # Assert: type of output
        self.assertIsInstance(result, float)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(math.isnan(result))
        else:
            # Expected
            expected = self.expected_std
            self.assertEqual(round(result, 4), expected)

    def test_get_min(self):
        """Test that the minimum value for the NumericColumn is the correct one."""

        # Act
        result = self.numeric_class.get_min()

        # Assert: type of output
        self.assertIsInstance(result, float)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(math.isnan(result))
        else:
            # Expected
            expected = self.expected_min
            self.assertEqual(result, expected)

    def test_get_max(self):
        """Test that the maximum value for the NumericColumn is the correct one."""

        # Act
        result = self.numeric_class.get_max()

        # Assert: type of output
        self.assertIsInstance(result, float)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(math.isnan(result))
        else:
            # Expected
            expected = self.expected_max
            self.assertEqual(result, expected)

    def test_get_median(self):
        """Test that the median value for the NumericColumn is the correct one."""

        # Act
        result = self.numeric_class.get_median()

        # Assert: type of output
        self.assertIsInstance(result, float)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(math.isnan(result))
        else:
            # Expected
            expected = self.expected_median
            self.assertEqual(result, expected)

    def test_get_histogram(self):
        """Test that the output class is Figure type."""

        # Act
        result = self.numeric_class.get_histogram(params=self.params.PLOT)

        # Assert: type of output
        self.assertIsInstance(result, Figure)

    def test_get_frequent(self):
        """Test that the generated dataframe is the correct one."""

        # Expected
        expected_columns = ["value", "occurrence", "percentage"]
        expected_length = self.expected_length

        # Act
        result = self.numeric_class.get_frequent(n_head=self.params.TOP_FREQUENCY)

        # Assert: type of output
        self.assertIsInstance(result, pd.DataFrame)
        # Assert: dtype of columns
        assert ptypes.is_numeric_dtype(result.value)
        assert ptypes.is_numeric_dtype(result.occurrence)
        assert ptypes.is_numeric_dtype(result.percentage)
        # Assert: column names
        self.assertListEqual(result.columns.tolist(), expected_columns)
        # Assert: length
        self.assertEqual(len(result), expected_length)


class TestMethodsValidNumericColumn(TestMethodsNumeric, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of valid serie as input."""

    def setUp(self) -> None:
        """Setting up a NumericColumn with regular series to run the tests."""

        # Instantiated NumericColumn class and parameters
        self.serie = pd.Series(
            [1.1, 2.2, 0, 3.3, 0, 4.4, 5.5, 5.5, np.nan], name="this_is_the_serie_name"
        )
        self.numeric_class = NumericColumn("this_is_the_serie_name", self.serie)
        self.params = ParamsSections(
            DROP_NA=True,
            TOP_FREQUENCY=5,
            PLOT=FormatHistogram(
                Y_AXIS_LABEL="y_axis_label",
                MAX_BINS=50,
                AXIS_FONT_SIZE=14,
                TICK_FONT_SIZE=16,
                TEMPLATE="simple_white",
                TITLE="title",
            ),
        )

        # Condition test
        self.assert_nan = False

        # Expected
        self.expected_name = "this_is_the_serie_name"
        self.expected_get_unique = 6
        self.expected_get_missing = 1
        self.expected_get_zeros = 2
        self.expected_negatives = 0
        self.expected_mean = 2.75
        self.expected_std = 2.2772
        self.expected_min = 0
        self.expected_max = 5.5
        self.expected_median = 2.75
        self.expected_length = 5

    def tearDown(self) -> None:
        """Delete the variables after each test."""

        del (
            self.serie,
            self.numeric_class,
            self.params,
            self.assert_nan,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_missing,
            self.expected_get_zeros,
            self.expected_negatives,
            self.expected_mean,
            self.expected_std,
            self.expected_min,
            self.expected_max,
            self.expected_median,
            self.expected_length,
        )

    def test_valid_get_frequent(self):
        """Test further conditions in the generated frequency dataframe."""

        # Expected
        expected_maximum_occurrence = 2
        expected_minimum_occurrence = 1
        expected_upper_bound_perc = 1

        # Act
        result = self.numeric_class.get_frequent(n_head=self.params.TOP_FREQUENCY)

        # Assert: sorted by occurrence (descending)
        self.assertEqual(result.occurrence.iloc[0], expected_maximum_occurrence)
        self.assertEqual(result.occurrence.iloc[-1], expected_minimum_occurrence)
        # Assert: upper bound for sum of percentages
        self.assertLessEqual(result.percentage.sum(), expected_upper_bound_perc)


class TestMethodsEmptyNumericColumn(TestMethodsNumeric, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of empty serie as input."""

    def setUp(self) -> None:
        """Setting up a NumericColumn with empty series to run the tests."""

        # Instantiated NumericColumn class and parameters
        self.serie = pd.Series([], name="this_is_the_serie_name", dtype="float64")
        self.numeric_class = NumericColumn("this_is_the_serie_name", self.serie)
        self.params = ParamsSections(
            DROP_NA=True,
            TOP_FREQUENCY=20,
            PLOT=FormatHistogram(
                Y_AXIS_LABEL="y_axis_label",
                MAX_BINS=50,
                AXIS_FONT_SIZE=14,
                TICK_FONT_SIZE=16,
                TEMPLATE="simple_white",
                TITLE="title",
            ),
        )

        # Condition test
        self.assert_nan = True

        # Expected
        self.expected_name = "this_is_the_serie_name"
        self.expected_get_unique = 0
        self.expected_get_missing = 0
        self.expected_get_zeros = 0
        self.expected_negatives = 0
        self.expected_length = 0

    def tearDown(self) -> None:
        """Delete the variables after each test."""

        del (
            self.serie,
            self.numeric_class,
            self.params,
            self.assert_nan,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_missing,
            self.expected_get_zeros,
            self.expected_negatives,
            self.expected_length,
        )


class TestMethodsNullNumericColumn(TestMethodsNumeric, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of null serie as input."""

    def setUp(self) -> None:
        """Setting up a NumericColumn with null series to run the tests."""

        # Instantiated NumericColumn class and parameters
        self.serie = pd.Series([np.nan, np.nan, np.nan], name="this_is_the_serie_name")
        self.numeric_class = NumericColumn("this_is_the_serie_name", self.serie)
        self.params = ParamsSections(
            DROP_NA=True,
            TOP_FREQUENCY=20,
            PLOT=FormatHistogram(
                Y_AXIS_LABEL="y_axis_label",
                MAX_BINS=50,
                AXIS_FONT_SIZE=14,
                TICK_FONT_SIZE=16,
                TEMPLATE="simple_white",
                TITLE="title",
            ),
        )

        # Condition test
        self.assert_nan = True

        # Expected
        self.expected_name = "this_is_the_serie_name"
        self.expected_get_unique = 0
        self.expected_get_missing = 3
        self.expected_get_zeros = 0
        self.expected_negatives = 0
        self.expected_length = 0

    def tearDown(self) -> None:
        """Delete the variables after each test."""

        del (
            self.serie,
            self.numeric_class,
            self.params,
            self.assert_nan,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_missing,
            self.expected_get_zeros,
            self.expected_negatives,
            self.expected_length,
        )


if __name__ == "__main__":
    unittest.main()
