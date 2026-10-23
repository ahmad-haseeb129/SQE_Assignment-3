"""
Data-Driven Error Unit Tests for dateutil.parser using external CSV dataset
Author: M. Ahmad (Roll No: 24F-3040)
Task 3: Consume test data from an external resource.
"""
import pytest
from dateutil.parser import parse, ParserError
from assignment_tests.conftest import load_csv_data

CSV_ROWS = load_csv_data("parser_cases_ahmad.csv")


@pytest.mark.data_driven
@pytest.mark.parametrize("row", CSV_ROWS, ids=lambda r: r["test_id"])
def test_csv_parser_error_cases(row):
    """Data-Driven: Assert that malformed strings loaded from CSV raise ParserError."""
    with pytest.raises(ParserError):
        parse(row["input_string"])
