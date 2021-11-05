import unittest
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import pandas.api.types as ptypes
from plotly.graph_objs._figure import Figure
from src.datetime import DateColumn
from src.settings import FormatBarPlot, ParamsSections


class TestMethodsDate(ABC):
    """Class containing the tests for the methods of the DateColumn class."""

    @abstractmethod
    def setUp(self) -> None:
        pass

    @abstractmethod
    def tearDown(self) -> None:
        pass

    def test_init(self) -> None:
        """Test that the instantiated class is DateColumn type."""

        # Assert: type of instantiated class
        self.assertIsInstance(self.date_class, DateColumn)

    def test_get_column_name(self):
        """Test that the DateColumn name is the correct one."""

        # Expected
        expected = self.expected_name

        # Act
        result = self.date_class.get_name()

        # Assert: type of output
        self.assertIsInstance(result, str)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_unique(self):
        """Test that the number of unique values for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_unique

        # Act
        result = self.date_class.get_unique()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_missing(self):
        """Test that the number of missing values for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_missing

        # Act
        result = self.date_class.get_missing()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_weekend(self):
        """Test that the number of occurrence of days falling during weekend (Saturday and Sunday) for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_weekend

        # Act
        result = self.date_class.get_weekend()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_weekday(self):
        """Test that the number of weekday days (not Saturday or Sunday) for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_weekday

        # Act
        result = self.date_class.get_weekday()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_future(self):
        """Test that the number of cases with future dates (after today) for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_future

        # Act
        result = self.date_class.get_future()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_empty_1900(self):
        """Test that the number of occurrence of 1900-01-01 value for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_empty_1900

        # Act
        result = self.date_class.get_empty_1900()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_empty_1970(self):
        """Test that the number of occurrence of 1970-01-01 value for the DateColumn is the correct one."""

        # Expected
        expected = self.expected_get_empty_1970

        # Act
        result = self.date_class.get_empty_1970()

        # Assert: type of output
        self.assertIsInstance(result, int)
        # Assert: expected result
        self.assertEqual(result, expected)

    def test_get_min(self):
        """Test that the minimum date for the DateColumn is the correct one."""

        # Act
        result = self.date_class.get_min()

        # Assert: type of output
        self.assertIsInstance(result, datetime)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(pd.isna(result))
        else:
            # Expected
            expected = self.expected_get_min
            self.assertEqual(result, expected)

    def test_get_max(self):
        """Test that the maximum date for the DateColumn is the correct one."""

        # Act
        result = self.date_class.get_max()

        # Assert: type of output
        self.assertIsInstance(result, datetime)
        # Assert: expected result
        if self.assert_nan:
            self.assertTrue(pd.isna(result))
        else:
            # Expected
            expected = self.expected_get_max
            self.assertEqual(result, expected)

    def test_get_barchart(self):
        """Test that the output class is Figure type."""

        # Act
        result = self.date_class.get_barchart(params=self.params.PLOT)

        # Assert: type of output
        self.assertIsInstance(result, Figure)

    def test_get_frequent(self):
        """Test that the generated dataframe is the correct one."""

        # Expected
        expected_columns = ["value", "occurrence", "percentage"]
        expected_length = self.expected_length

        # Act
        result = self.date_class.get_frequent(n_head=self.params.TOP_FREQUENCY)

        # Assert: type of output
        self.assertIsInstance(result, pd.DataFrame)
        # Assert: dtype of columns
        assert ptypes.is_datetime64_dtype(result.value)
        assert ptypes.is_numeric_dtype(result.occurrence)
        assert ptypes.is_numeric_dtype(result.percentage)
        # Assert: column names
        self.assertListEqual(result.columns.tolist(), expected_columns)
        # Assert: length
        self.assertEqual(len(result), expected_length)


class TestMethodsValidDateColumn(TestMethodsDate, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of valid serie as input."""

    def setUp(self) -> None:
        """Setting an empty dataframe to be tested before each test"""

        # Instantiated DateColumn class and parameters
        self.serie = pd.to_datetime(
            pd.Series(
                [
                    "2021-10-03",
                    "",
                    "2021-10-03",
                    "s",
                    datetime.today() + timedelta(1),
                    "1900-01-01",
                    "1970-01-01",
                    " ",
                    np.nan,
                ],
                name="this_is_the_serie_name",
            ),
            errors="coerce",
        )
        self.date_class = DateColumn("this_is_the_serie_name", self.serie)
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

        # Condition test
        self.assert_nan = False

        # Expected
        self.expected_name = "this_is_the_serie_name"
        self.expected_get_unique = 4
        self.expected_get_missing = 4
        self.expected_get_weekend = 3
        self.expected_get_weekday = 2
        self.expected_get_future = 1
        self.expected_get_empty_1900 = 1
        self.expected_get_empty_1970 = 1
        self.expected_get_min = date(1900, 1, 1)
        self.expected_get_max = date.today() + timedelta(1)
        self.expected_length = 4

    def tearDown(self) -> None:
        """Delete the variables after each test"""
        del (
            self.serie,
            self.date_class,
            self.params,
            self.assert_nan,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_missing,
            self.expected_get_weekend,
            self.expected_get_weekday,
            self.expected_get_future,
            self.expected_get_empty_1900,
            self.expected_get_empty_1970,
            self.expected_get_min,
            self.expected_get_max,
            self.expected_length,
        )

    def test_valid_get_frequent(self):

        # Expected
        expected_maximum_occurrence = 2
        expected_minimum_occurrence = 1
        expected_upper_bound_perc = 1

        # Act
        result = self.date_class.get_frequent(n_head=self.params.TOP_FREQUENCY)

        # Assert: sorted by occurrence (descending)
        self.assertEqual(result.occurrence.iloc[0], expected_maximum_occurrence)
        self.assertEqual(result.occurrence.iloc[-1], expected_minimum_occurrence)
        # Assert: upper bound for sum of percentages
        self.assertLessEqual(result.percentage.sum(), expected_upper_bound_perc)


class TestMethodsEmptyDateColumn(TestMethodsDate, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of empty serie as input."""

    def setUp(self) -> None:
        """Setting an empty dataframe to be tested before each test"""

        # Instantiated DateColumn class and parameters
        self.serie = pd.Series(
            [], name="this_is_the_serie_name", dtype="datetime64[ns]"
        )
        self.date_class = DateColumn("this_is_the_serie_name", self.serie)
        self.params = ParamsSections(
            DROP_NA=True,
            TOP_FREQUENCY=20,
            PLOT=FormatBarPlot(
                Y_AXIS_LABEL="y_axis_label",
                AXIS_FONT_SIZE=14,
                TICK_FONT_SIZE=16,
                CATEGORY_ORDER="total descending",
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
        self.expected_get_weekend = 0
        self.expected_get_weekday = 0
        self.expected_get_future = 0
        self.expected_get_empty_1900 = 0
        self.expected_get_empty_1970 = 0
        self.expected_length = 0

    def tearDown(self) -> None:
        """Delete the variables after each test"""
        del (
            self.serie,
            self.date_class,
            self.params,
            self.assert_nan,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_weekend,
            self.expected_get_weekday,
            self.expected_get_future,
            self.expected_get_empty_1900,
            self.expected_get_empty_1970,
            self.expected_length,
        )


class TestMethodsNullDateColumn(TestMethodsDate, unittest.TestCase):
    """Class containing the setup and customised tests for the scenario of null serie as input."""

    def setUp(self) -> None:
        """Setting an empty dataframe to be tested before each test"""

        # Instantiated DateColumn class and parameters
        self.serie = pd.Series(
            [np.nan, np.nan, np.nan],
            name="this_is_the_serie_name",
            dtype="datetime64[ns]",
        )
        self.date_class = DateColumn("this_is_the_serie_name", self.serie)
        self.params = ParamsSections(
            DROP_NA=True,
            TOP_FREQUENCY=20,
            PLOT=FormatBarPlot(
                Y_AXIS_LABEL="y_axis_label",
                AXIS_FONT_SIZE=14,
                TICK_FONT_SIZE=16,
                CATEGORY_ORDER="total descending",
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
        self.expected_get_weekend = 0
        self.expected_get_weekday = 0
        self.expected_get_future = 0
        self.expected_get_empty_1900 = 0
        self.expected_get_empty_1970 = 0
        self.expected_length = 0

    def tearDown(self) -> None:
        """Delete the variables after each test"""
        del (
            self.serie,
            self.date_class,
            self.params,
            self.assert_nan,
            self.expected_name,
            self.expected_get_unique,
            self.expected_get_weekend,
            self.expected_get_weekday,
            self.expected_get_future,
            self.expected_get_empty_1900,
            self.expected_get_empty_1970,
            self.expected_length,
        )


if __name__ == "__main__":
    unittest.main()
