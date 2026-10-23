"""
CSV-Driven Automated Unit Tests
SQE Assignment 3 - Task 3: Data-Driven Testing via External CSV Resources
Contributions:
- M. Ibrahim Asif (24F-3070)
- M. Ahmad (24F-3040)
"""
import pytest
from datetime import datetime, date
from dateutil.parser import parse, ParserError
from dateutil.relativedelta import relativedelta
from dateutil.rrule import (
    rrule, YEARLY, MONTHLY, WEEKLY, DAILY
)
from tests.conftest import load_csv_data

# Load CSV data rows
PARSER_CSV_DATA = load_csv_data("parser_test_data.csv")
RELATIVEDELTA_CSV_DATA = load_csv_data("relativedelta_test_data.csv")
RRULE_CSV_DATA = load_csv_data("rrule_test_data.csv")

FREQ_MAP = {
    "DAILY": DAILY,
    "WEEKLY": WEEKLY,
    "MONTHLY": MONTHLY,
    "YEARLY": YEARLY,
}


# ==============================================================================
# Ibrahim's CSV-Driven Tests (24F-3070)
# ==============================================================================

@pytest.mark.csv_driven
@pytest.mark.parser
@pytest.mark.order(2)
@pytest.mark.parametrize("row", [r for r in PARSER_CSV_DATA if r["should_raise"] == "False"], ids=lambda r: r["test_id"])
def test_csv_driven_parser_valid_cases(row):
    """
    Test parsing valid date/time strings loaded dynamically from external CSV.
    Author: M. Ibrahim Asif (24F-3070)
    """
    input_str = row["input_string"]
    fuzzy = row["fuzzy"].strip().lower() == "true"
    dayfirst = row["dayfirst"].strip().lower() == "true"
    yearfirst = row["yearfirst"].strip().lower() == "true"

    result = parse(input_str, fuzzy=fuzzy, dayfirst=dayfirst, yearfirst=yearfirst)

    assert result.year == int(row["expected_year"])
    assert result.month == int(row["expected_month"])
    assert result.day == int(row["expected_day"])
    assert result.hour == int(row["expected_hour"])
    assert result.minute == int(row["expected_minute"])
    assert result.second == int(row["expected_second"])


@pytest.mark.csv_driven
@pytest.mark.relativedelta
@pytest.mark.order(2)
@pytest.mark.parametrize("row", RELATIVEDELTA_CSV_DATA, ids=lambda r: r["test_id"])
def test_csv_driven_relativedelta_operations(row):
    """
    Test date arithmetic applying relativedeltas loaded from external CSV.
    Author: M. Ibrahim Asif (24F-3070)
    """
    start_dt = date(int(row["start_year"]), int(row["start_month"]), int(row["start_day"]))
    delta = relativedelta(
        years=int(row["rel_years"]),
        months=int(row["rel_months"]),
        days=int(row["rel_days"])
    )

    result = start_dt + delta

    expected_dt = date(int(row["expected_year"]), int(row["expected_month"]), int(row["expected_day"]))
    assert result == expected_dt


# ==============================================================================
# Ahmad's CSV-Driven Tests (24F-3040)
# ==============================================================================

@pytest.mark.csv_driven
@pytest.mark.parser
@pytest.mark.order(2)
@pytest.mark.parametrize("row", [r for r in PARSER_CSV_DATA if r["should_raise"] == "True"], ids=lambda r: r["test_id"])
def test_csv_driven_parser_error_cases(row):
    """
    Test error handling for invalid/empty date strings loaded from external CSV.
    Author: M. Ahmad (24F-3040)
    """
    input_str = row["input_string"]
    with pytest.raises(ParserError):
        parse(input_str)


@pytest.mark.csv_driven
@pytest.mark.rrule
@pytest.mark.order(2)
@pytest.mark.parametrize("row", RRULE_CSV_DATA, ids=lambda r: r["test_id"])
def test_csv_driven_rrule_generation(row):
    """
    Test recurrence occurrence counts and intervals loaded from external CSV.
    Author: M. Ahmad (24F-3040)
    """
    freq_const = FREQ_MAP[row["freq"].strip()]
    start_dt = datetime(int(row["start_year"]), int(row["start_month"]), int(row["start_day"]))
    interval = int(row["interval"])
    count = int(row["count"])

    rule = rrule(freq_const, dtstart=start_dt, interval=interval, count=count)
    occurrences = list(rule)

    assert len(occurrences) == int(row["expected_count"])
