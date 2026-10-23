"""
Automated Unit Tests for dateutil.parser (Standard Formats & Boundaries)
Author: M. Ibrahim Asif (Roll No: 24F-3070)
Testing Techniques: ECP (Equivalence Class Partitioning) & BVA (Boundary Value Analysis)
"""
import pytest
from datetime import datetime
from dateutil.parser import parse


@pytest.mark.smoke
@pytest.mark.parametrize("timestr,expected", [
    ("2024-01-15", datetime(2024, 1, 15)),
    ("2024-06-30", datetime(2024, 6, 30)),
    ("2024-12-25", datetime(2024, 12, 25)),
    ("2020-02-29", datetime(2020, 2, 29)),
])
def test_parse_iso8601_format(timestr, expected):
    """ECP: Test parsing standard ISO 8601 YYYY-MM-DD dates."""
    res = parse(timestr)
    assert res.date() == expected.date()


@pytest.mark.parametrize("timestr,expected", [
    ("01/15/2024", datetime(2024, 1, 15)),
    ("12/31/2024", datetime(2024, 12, 31)),
    ("06/15/2023", datetime(2023, 6, 15)),
])
def test_parse_us_date_format(timestr, expected):
    """ECP: Test parsing standard US MM/DD/YYYY slash formatted dates."""
    res = parse(timestr)
    assert res.date() == expected.date()


@pytest.mark.parametrize("timestr,expected", [
    ("January 15, 2024", datetime(2024, 1, 15)),
    ("March 1, 2020", datetime(2020, 3, 1)),
    ("December 25, 2023", datetime(2023, 12, 25)),
])
def test_parse_written_month_names(timestr, expected):
    """ECP: Test parsing written month names."""
    res = parse(timestr)
    assert res.date() == expected.date()


@pytest.mark.parametrize("timestr,expected", [
    ("Jan 15, 2024", datetime(2024, 1, 15)),
    ("Dec 25, 2023", datetime(2023, 12, 25)),
    ("Mar 1, 2020", datetime(2020, 3, 1)),
])
def test_parse_abbreviated_month_names(timestr, expected):
    """ECP: Test parsing abbreviated month names."""
    res = parse(timestr)
    assert res.date() == expected.date()


@pytest.mark.parametrize("timestr,expected_date,h,m,s", [
    ("2024-01-15 14:30:00", datetime(2024, 1, 15), 14, 30, 0),
    ("2024-06-15 23:59:59", datetime(2024, 6, 15), 23, 59, 59),
    ("2024-03-01 08:15:45", datetime(2024, 3, 1), 8, 15, 45),
])
def test_parse_dates_with_time(timestr, expected_date, h, m, s):
    """ECP: Test parsing combined date and time strings."""
    res = parse(timestr)
    assert res.date() == expected_date.date()
    assert res.hour == h
    assert res.minute == m
    assert res.second == s


@pytest.mark.parametrize("timestr,dayfirst,expected_month,expected_day", [
    ("01/02/2024", True, 2, 1),
    ("01/02/2024", False, 1, 2),
    ("13/02/2024", True, 2, 13),
])
def test_parse_dayfirst_flag(timestr, dayfirst, expected_month, expected_day):
    """ECP: Test ambiguous date parsing with dayfirst parameter."""
    res = parse(timestr, dayfirst=dayfirst)
    assert res.month == expected_month
    assert res.day == expected_day


@pytest.mark.boundary
@pytest.mark.parametrize("timestr,expected_year", [
    ("0001-01-01", 1),
    ("9999-12-31", 9999),
])
def test_parse_year_boundaries(timestr, expected_year):
    """BVA: Test datetime min and max boundary years."""
    res = parse(timestr)
    assert res.year == expected_year


@pytest.mark.boundary
@pytest.mark.parametrize("timestr,expected_day", [
    ("2024-01-01", 1),
    ("2024-01-31", 31),
    ("2024-04-30", 30),
    ("2024-02-29", 29),
    ("2023-02-28", 28),
])
def test_parse_day_boundaries(timestr, expected_day):
    """BVA: Test calendar day limits including leap day boundary."""
    res = parse(timestr)
    assert res.day == expected_day
