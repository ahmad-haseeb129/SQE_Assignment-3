"""
Automated Unit Tests for dateutil.parser (Edge Cases, Fuzzy, Invalid Inputs)
Author: M. Ahmad (Roll No: 24F-3040)
Testing Techniques: ECP & BVA
"""
import pytest
from datetime import datetime
from dateutil.parser import parse, ParserError


def test_empty_string_raises_parser_error():
    """ECP: Empty string input raises ParserError."""
    with pytest.raises(ParserError):
        parse("")


def test_non_date_text_raises_parser_error():
    """ECP: Non-date text raises ParserError."""
    with pytest.raises(ParserError):
        parse("hello world not a date")


def test_none_input_raises_type_error():
    """ECP: None input raises TypeError."""
    with pytest.raises(TypeError):
        parse(None)


def test_numeric_only_string_parsing():
    """ECP: Unseparated numeric string YYYYMMDD parses properly."""
    res = parse("20240115")
    assert res.date() == datetime(2024, 1, 15).date()


def test_fuzzy_date_extraction():
    """ECP: Fuzzy parser extracts valid date embedded in sentences."""
    sentence = "Today is January 15, 2024 and the meeting is done"
    res = parse(sentence, fuzzy=True)
    assert res.date() == datetime(2024, 1, 15).date()


@pytest.mark.boundary
@pytest.mark.parametrize("timestr,h,m,s", [
    ("2024-01-15 00:00:00", 0, 0, 0),
    ("2024-01-15 23:59:59", 23, 59, 59),
])
def test_time_boundaries_midnight_and_day_end(timestr, h, m, s):
    """BVA: Midnight boundary (00:00:00) and day end boundary (23:59:59)."""
    res = parse(timestr)
    assert res.hour == h
    assert res.minute == m
    assert res.second == s


def test_date_with_timezone_offset():
    """ECP: Parse ISO string containing explicit UTC timezone offset."""
    res = parse("2024-01-15T14:30:00+05:00")
    assert res.year == 2024
    assert res.hour == 14
    assert res.tzinfo is not None
