"""
Data-Driven Unit Tests for dateutil.parser using external CSV dataset
Author: M. Ibrahim Asif (Roll No: 24F-3070)
Task 3: Consume test data from an external resource.
"""
import pytest
from dateutil.parser import parse
from assignment_tests.conftest import load_csv_data

CSV_ROWS = load_csv_data("parser_cases_ibrahim.csv")


@pytest.mark.data_driven
@pytest.mark.parametrize("row", CSV_ROWS, ids=lambda r: r["test_id"])
def test_csv_parser_valid_cases(row):
    """Data-Driven: Parse test vectors loaded dynamically from CSV."""
    timestr = row["input_string"]
    dayfirst = row["dayfirst"].strip().lower() == "true"
    yearfirst = row["yearfirst"].strip().lower() == "true"
    fuzzy = row["fuzzy"].strip().lower() == "true"

    result = parse(timestr, dayfirst=dayfirst, yearfirst=yearfirst, fuzzy=fuzzy)

    assert result.year == int(row["expected_year"])
    assert result.month == int(row["expected_month"])
    assert result.day == int(row["expected_day"])
    assert result.hour == int(row["expected_hour"])
    assert result.minute == int(row["expected_minute"])
    assert result.second == int(row["expected_second"])
