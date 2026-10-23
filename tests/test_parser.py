"""
Unit Tests for dateutil.parser module
SQE Assignment 3

Contributors:
    - M. Ibrahim Asif (24F-3070): Standard format parsing, date boundaries, dayfirst/yearfirst
    - M. Ahmad (24F-3040): Edge cases, invalid inputs, time boundaries, fuzzy parsing

Testing Techniques:
    - ECP (Equivalence Class Partitioning): Tests representative values from distinct input classes
    - BVA (Boundary Value Analysis): Tests boundary/edge values at the limits of valid ranges
"""
import pytest
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse, ParserError


# =============================================================================
# Ibrahim's Tests (24F-3070) — Standard Format Parsing (ECP)
# =============================================================================


@pytest.mark.order(1)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.smoke
@pytest.mark.parametrize("date_string, expected", [
    ("2024-01-15", datetime(2024, 1, 15)),
    ("2024-06-30", datetime(2024, 6, 30)),
    ("2024-12-25", datetime(2024, 12, 25)),
    ("2020-02-29", datetime(2020, 2, 29)),
])
def test_parse_iso8601_format(date_string, expected):
    """Test parsing of ISO 8601 format dates (YYYY-MM-DD).

    Verifies that the parser correctly interprets standard ISO 8601 date strings
    covering different months, end-of-month dates, and leap year dates.
    """
    result = parse(date_string)
    assert result.date() == expected.date()


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("date_string, expected", [
    ("01/15/2024", datetime(2024, 1, 15)),
    ("12/31/2024", datetime(2024, 12, 31)),
    ("06/15/2023", datetime(2023, 6, 15)),
])
def test_parse_us_format(date_string, expected):
    """Test parsing of US-style MM/DD/YYYY format dates.

    Verifies that the parser correctly interprets the common US date format
    with slashes, covering the start, middle, and end of the year.
    """
    result = parse(date_string)
    assert result.date() == expected.date()


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("date_string, expected", [
    ("January 15, 2024", datetime(2024, 1, 15)),
    ("March 1, 2020", datetime(2020, 3, 1)),
    ("December 25, 2023", datetime(2023, 12, 25)),
])
def test_parse_written_month_names(date_string, expected):
    """Test parsing of dates with full written month names.

    Verifies that the parser handles human-readable date strings where
    the month is spelled out completely (e.g., 'January 15, 2024').
    """
    result = parse(date_string)
    assert result.date() == expected.date()


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("date_string, expected", [
    ("Jan 15, 2024", datetime(2024, 1, 15)),
    ("Dec 25, 2023", datetime(2023, 12, 25)),
    ("Mar 1, 2020", datetime(2020, 3, 1)),
    ("Jul 4, 2024", datetime(2024, 7, 4)),
])
def test_parse_abbreviated_month_names(date_string, expected):
    """Test parsing of dates with abbreviated (3-letter) month names.

    Verifies that the parser correctly interprets shortened month names
    like 'Jan', 'Dec', 'Mar', and 'Jul'.
    """
    result = parse(date_string)
    assert result.date() == expected.date()


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("date_string, expected_date, expected_hour, expected_minute, expected_second", [
    ("2024-01-15 14:30:00", datetime(2024, 1, 15), 14, 30, 0),
    ("2024-06-15 23:59:59", datetime(2024, 6, 15), 23, 59, 59),
    ("2024-03-01 08:15:45", datetime(2024, 3, 1), 8, 15, 45),
])
def test_parse_dates_with_times(date_string, expected_date, expected_hour, expected_minute, expected_second):
    """Test parsing of datetime strings that include time components.

    Verifies that both date and time portions (hour, minute, second) are
    correctly extracted from combined datetime strings.
    """
    result = parse(date_string)
    assert result.date() == expected_date.date()
    assert result.hour == expected_hour
    assert result.minute == expected_minute
    assert result.second == expected_second


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("date_string, dayfirst, expected", [
    ("01/02/2024", True,  datetime(2024, 2, 1)),   # DD/MM/YYYY
    ("01/02/2024", False, datetime(2024, 1, 2)),    # MM/DD/YYYY
    ("13/02/2024", True,  datetime(2024, 2, 13)),   # Unambiguous — day > 12
])
def test_parse_dayfirst_flag(date_string, dayfirst, expected):
    """Test the dayfirst parameter for ambiguous date formats.

    When dayfirst=True, '01/02/2024' is interpreted as DD/MM/YYYY (Feb 1).
    When dayfirst=False (default), it is interpreted as MM/DD/YYYY (Jan 2).
    Also tests an unambiguous case where day > 12.
    """
    result = parse(date_string, dayfirst=dayfirst)
    assert result.date() == expected.date()


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("date_string, yearfirst, expected", [
    ("01/02/03", True,  datetime(2001, 2, 3)),   # YY/MM/DD
    ("01/02/03", False, datetime(2003, 1, 2)),    # MM/DD/YY (default)
])
def test_parse_yearfirst_flag(date_string, yearfirst, expected):
    """Test the yearfirst parameter for ambiguous short date formats.

    When yearfirst=True, '01/02/03' is interpreted as YY/MM/DD (2001-02-03).
    When yearfirst=False (default), it is interpreted as MM/DD/YY (2003-01-02).
    """
    result = parse(date_string, yearfirst=yearfirst)
    assert result.date() == expected.date()


# =============================================================================
# Ibrahim's Tests (24F-3070) — Date Boundaries (BVA)
# =============================================================================


@pytest.mark.order(3)
@pytest.mark.parser
@pytest.mark.bva
@pytest.mark.parametrize("date_string, expected", [
    ("0001-01-01", datetime(1, 1, 1)),      # Minimum representable date
    ("9999-12-31", datetime(9999, 12, 31)),  # Maximum representable date
])
def test_parse_year_boundaries(date_string, expected):
    """Test parsing at the absolute minimum and maximum year boundaries.

    BVA: Validates that the parser can handle the smallest (0001) and
    largest (9999) years representable by Python's datetime.
    """
    result = parse(date_string)
    assert result.date() == expected.date()


@pytest.mark.order(3)
@pytest.mark.parser
@pytest.mark.bva
@pytest.mark.parametrize("date_string, expected_month", [
    ("2024-01-15", 1),   # First month boundary
    ("2024-12-15", 12),  # Last month boundary
])
def test_parse_month_boundaries(date_string, expected_month):
    """Test parsing at month boundaries (first and last months of the year).

    BVA: Validates correct parsing when month is at its minimum (1) and
    maximum (12) valid values.
    """
    result = parse(date_string)
    assert result.month == expected_month


@pytest.mark.order(3)
@pytest.mark.parser
@pytest.mark.bva
@pytest.mark.parametrize("date_string, expected_day", [
    ("2024-01-01", 1),   # First day of month
    ("2024-01-31", 31),  # Last day of 31-day month
    ("2024-04-30", 30),  # Last day of 30-day month
    ("2024-02-29", 29),  # Last day of Feb in leap year
    ("2023-02-28", 28),  # Last day of Feb in non-leap year
])
def test_parse_day_boundaries(date_string, expected_day):
    """Test parsing at day-of-month boundaries for various month lengths.

    BVA: Validates day=1 (minimum), day=28 (Feb non-leap), day=29 (Feb leap),
    day=30 (30-day month), and day=31 (31-day month).
    """
    result = parse(date_string)
    assert result.day == expected_day


@pytest.mark.order(3)
@pytest.mark.parser
@pytest.mark.bva
def test_parse_invalid_leap_year_date():
    """Test that Feb 29 on a non-leap year raises ParserError.

    BVA: 2023 is not a leap year, so '2023-02-29' is an invalid calendar
    date. The parser should raise a ParserError.
    """
    with pytest.raises(ParserError):
        parse("2023-02-29")


# =============================================================================
# Ahmad's Tests (24F-3040) — Edge Cases & Invalid Inputs (ECP)
# =============================================================================


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
@pytest.mark.parametrize("invalid_input, expected_exception", [
    ("",            ParserError),  # Empty string
    ("hello world", ParserError),  # Non-date text
    (None,          TypeError),    # None input
])
def test_parse_invalid_inputs(invalid_input, expected_exception):
    """Test that invalid inputs raise the appropriate exceptions.

    ECP — Invalid equivalence classes:
    - Empty string → ParserError (no date information)
    - Random text  → ParserError (cannot extract a date)
    - None         → TypeError (wrong argument type)
    """
    with pytest.raises(expected_exception):
        parse(invalid_input)


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
def test_parse_numeric_only_string():
    """Test parsing a compact numeric-only date string (YYYYMMDD).

    Verifies that '20240115' is correctly interpreted as January 15, 2024,
    demonstrating that the parser handles dates without any separators.
    """
    result = parse("20240115")
    assert result.date() == datetime(2024, 1, 15).date()


@pytest.mark.order(2)
@pytest.mark.parser
@pytest.mark.ecp
def test_parse_fuzzy_date_extraction():
    """Test fuzzy parsing to extract dates embedded in natural language text.

    Verifies that with fuzzy=True, the parser can locate and extract the date
    'January 15, 2024' from a surrounding sentence of non-date text.
    """
    result = parse("The meeting is on January 15, 2024 at noon", fuzzy=True)
    assert result.date() == datetime(2024, 1, 15).date()


# =============================================================================
# Ahmad's Tests (24F-3040) — Time & Timezone Boundaries (BVA)
# =============================================================================


@pytest.mark.order(3)
@pytest.mark.parser
@pytest.mark.bva
@pytest.mark.parametrize("date_string, expected_hour, expected_minute, expected_second", [
    ("2024-01-15 00:00:00", 0,  0,  0),   # Midnight — start of day
    ("2024-01-15 23:59:59", 23, 59, 59),   # Last second — end of day
])
def test_parse_time_boundaries(date_string, expected_hour, expected_minute, expected_second):
    """Test parsing at the minimum and maximum time-of-day boundaries.

    BVA: Validates the lower boundary (00:00:00 — midnight) and the upper
    boundary (23:59:59 — last second of the day) for time components.
    """
    result = parse(date_string)
    assert result.hour == expected_hour
    assert result.minute == expected_minute
    assert result.second == expected_second


@pytest.mark.order(3)
@pytest.mark.parser
@pytest.mark.bva
def test_parse_date_with_timezone_offset():
    """Test parsing an ISO 8601 datetime string that includes a UTC offset.

    BVA: Verifies that the parser correctly extracts both the datetime and
    the +05:00 timezone offset, confirming timezone-aware datetime creation.
    """
    result = parse("2024-01-15T14:30:00+05:00")
    assert result.date() == datetime(2024, 1, 15).date()
    assert result.hour == 14
    assert result.minute == 30
    assert result.tzinfo is not None
    assert result.utcoffset() == timedelta(hours=5)
