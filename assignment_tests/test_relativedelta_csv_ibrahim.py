"""
Data-Driven Unit Tests for dateutil.relativedelta using external CSV dataset
Author: M. Ibrahim Asif (Roll No: 24F-3070)
Task 3: Consume test data from an external resource.
"""
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta
from assignment_tests.conftest import load_csv_data

CSV_ROWS = load_csv_data("relativedelta_cases_ibrahim.csv")


@pytest.mark.data_driven
@pytest.mark.parametrize("row", CSV_ROWS, ids=lambda r: r["test_id"])
def test_csv_relativedelta_operations(row):
    """Data-Driven: Apply relative deltas loaded from CSV and assert result."""
    start_dt = date(int(row["start_year"]), int(row["start_month"]), int(row["start_day"]))
    delta = relativedelta(
        years=int(row["rel_years"]),
        months=int(row["rel_months"]),
        days=int(row["rel_days"])
    )

    result = start_dt + delta

    expected_dt = date(int(row["expected_year"]), int(row["expected_month"]), int(row["expected_day"]))
    assert result == expected_dt
