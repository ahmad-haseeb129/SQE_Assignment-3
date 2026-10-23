"""
Data-Driven Unit Tests for dateutil.rrule using external CSV dataset
Author: M. Ahmad (Roll No: 24F-3040)
Task 3: Consume test data from an external resource.
"""
import pytest
from datetime import datetime
from dateutil.rrule import (
    rrule, YEARLY, MONTHLY, WEEKLY, DAILY
)
from assignment_tests.conftest import load_csv_data

CSV_ROWS = load_csv_data("rrule_cases_ahmad.csv")

FREQ_MAP = {
    "DAILY": DAILY,
    "WEEKLY": WEEKLY,
    "MONTHLY": MONTHLY,
    "YEARLY": YEARLY,
}


@pytest.mark.data_driven
@pytest.mark.parametrize("row", CSV_ROWS, ids=lambda r: r["test_id"])
def test_csv_rrule_generation(row):
    """Data-Driven: Generate recurrence rules from CSV data rows and assert count."""
    freq_const = FREQ_MAP[row["freq"].strip()]
    start_dt = datetime(int(row["start_year"]), int(row["start_month"]), int(row["start_day"]))
    interval = int(row["interval"])
    count = int(row["count"])

    rule = rrule(freq_const, dtstart=start_dt, interval=interval, count=count)
    occurrences = list(rule)

    assert len(occurrences) == int(row["expected_count"])
