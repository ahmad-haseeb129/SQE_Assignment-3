"""
Automated Unit Tests for dateutil.rrule (Recurrence Rules & Sets)
Author: M. Ahmad (Roll No: 24F-3040)
Testing Techniques: ECP & BVA
"""
import pytest
from datetime import datetime
from dateutil.rrule import (
    rrule, rruleset,
    YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY,
    MO, FR
)


@pytest.mark.smoke
def test_yearly_recurrence_rule():
    """ECP: Verify annual recurrence generation over 3 years."""
    start = datetime(2024, 1, 15, 10, 0, 0)
    rule = rrule(YEARLY, count=3, dtstart=start)
    occurrences = list(rule)

    assert len(occurrences) == 3
    assert occurrences[0] == datetime(2024, 1, 15, 10, 0, 0)
    assert occurrences[1] == datetime(2025, 1, 15, 10, 0, 0)
    assert occurrences[2] == datetime(2026, 1, 15, 10, 0, 0)


@pytest.mark.parametrize("freq,count,expected_days", [
    (MONTHLY, 3, [15, 15, 15]),
    (WEEKLY, 3, [15, 22, 29]),
    (DAILY, 4, [15, 16, 17, 18]),
])
def test_standard_recurrence_frequencies(freq, count, expected_days):
    """ECP: Monthly, weekly, and daily recurrence frequencies."""
    start = datetime(2024, 1, 15)
    rule = rrule(freq, count=count, dtstart=start)
    occurrences = list(rule)

    assert len(occurrences) == count
    assert [occ.day for occ in occurrences] == expected_days


def test_hourly_frequency_stepping():
    """ECP: Sub-daily hourly recurrence rule."""
    start = datetime(2024, 1, 1, 8, 0, 0)
    rule = rrule(HOURLY, interval=2, count=3, dtstart=start)
    occurrences = list(rule)

    assert len(occurrences) == 3
    assert occurrences[0] == datetime(2024, 1, 1, 8, 0, 0)
    assert occurrences[1] == datetime(2024, 1, 1, 10, 0, 0)
    assert occurrences[2] == datetime(2024, 1, 1, 12, 0, 0)


@pytest.mark.parametrize("weekdays,expected_days", [
    (MO, [1, 8, 15]),
    ((MO, FR), [1, 5, 8, 12, 15]),
])
def test_byweekday_filtering(weekdays, expected_days):
    """ECP: Single and compound weekday filters."""
    start = datetime(2024, 1, 1)  # Monday
    rule = rrule(DAILY, count=len(expected_days), byweekday=weekdays, dtstart=start)
    occurrences = list(rule)

    assert [occ.day for occ in occurrences] == expected_days


@pytest.mark.boundary
@pytest.mark.parametrize("count_val,expected_len", [
    (0, 0),
    (1, 1),
    (5, 5),
])
def test_count_boundary_limits(count_val, expected_len):
    """BVA: Count parameter lower boundaries (0, 1) and small count."""
    start = datetime(2024, 5, 1)
    rule = rrule(DAILY, count=count_val, dtstart=start)
    assert len(list(rule)) == expected_len


@pytest.mark.boundary
def test_until_boundary_equals_dtstart():
    """BVA: Boundary condition where until equals dtstart."""
    start = datetime(2024, 3, 10, 12, 0, 0)
    rule = rrule(DAILY, dtstart=start, until=start)
    occurrences = list(rule)

    assert len(occurrences) == 1
    assert occurrences[0] == start


@pytest.mark.boundary
def test_bymonthday_month_end_filtering():
    """BVA: bymonthday=31 skips short months without 31 days."""
    start = datetime(2024, 1, 1)
    rule = rrule(MONTHLY, count=4, bymonthday=31, dtstart=start)
    occurrences = list(rule)

    assert [occ.month for occ in occurrences] == [1, 3, 5, 7]
    assert all(occ.day == 31 for occ in occurrences)


@pytest.mark.boundary
def test_negative_bymonthday_last_day():
    """BVA: bymonthday=-1 resolves to dynamic last day of each month."""
    start = datetime(2024, 1, 1)
    rule = rrule(MONTHLY, count=4, bymonthday=-1, dtstart=start)
    occurrences = list(rule)

    assert occurrences[0] == datetime(2024, 1, 31)
    assert occurrences[1] == datetime(2024, 2, 29)
    assert occurrences[2] == datetime(2024, 3, 31)
    assert occurrences[3] == datetime(2024, 4, 30)


def test_rruleset_with_exdate_exclusion():
    """ECP: rruleset combining inclusion recurrence rule with excluded date."""
    start = datetime(2024, 1, 1)
    rset = rruleset()
    rset.rrule(rrule(DAILY, count=5, dtstart=start))
    rset.exdate(datetime(2024, 1, 3))

    occurrences = list(rset)
    assert len(occurrences) == 4
    assert datetime(2024, 1, 3) not in occurrences
    assert [occ.day for occ in occurrences] == [1, 2, 4, 5]
