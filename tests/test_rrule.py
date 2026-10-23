"""
Unit Tests for dateutil.rrule module
SQE Assignment 3
Contributions:
- M. Ibrahim Asif (24F-3070)
- M. Ahmad (24F-3040)
"""
import pytest
from datetime import datetime, date
from dateutil.rrule import (
    rrule, rruleset,
    YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY,
    MO, TU, WE, TH, FR, SA, SU
)


# ==============================================================================
# Ibrahim's Tests (24F-3070) - Core Frequencies, Count, Interval, and Query APIs
# ==============================================================================

@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.smoke
@pytest.mark.order(1)
def test_yearly_frequency_recurrence():
    """
    Test yearly frequency produces exact annual recurrences (ECP - Valid Class).
    Author: M. Ibrahim Asif (24F-3070)
    """
    start = datetime(2024, 1, 15, 10, 0, 0)
    rule = rrule(YEARLY, count=3, dtstart=start)
    occurrences = list(rule)

    assert len(occurrences) == 3
    assert occurrences[0] == datetime(2024, 1, 15, 10, 0, 0)
    assert occurrences[1] == datetime(2025, 1, 15, 10, 0, 0)
    assert occurrences[2] == datetime(2026, 1, 15, 10, 0, 0)


@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.order(2)
@pytest.mark.parametrize("freq,count,expected_deltas", [
    (MONTHLY, 4, [(0, 1, 15), (0, 2, 15), (0, 3, 15), (0, 4, 15)]),
    (WEEKLY, 4, [(0, 1, 15), (0, 1, 22), (0, 1, 29), (0, 2, 5)]),
    (DAILY, 5, [(0, 1, 15), (0, 1, 16), (0, 1, 17), (0, 1, 18), (0, 1, 19)]),
])
def test_standard_frequencies(freq, count, expected_deltas):
    """
    Test standard frequency intervals for monthly, weekly, and daily rules (ECP).
    Author: M. Ibrahim Asif (24F-3070)
    """
    start = datetime(2024, 1, 15)
    rule = rrule(freq, count=count, dtstart=start)
    occurrences = list(rule)

    assert len(occurrences) == count
    for occ, expected in zip(occurrences, expected_deltas):
        assert occ.month == expected[1]
        assert occ.day == expected[2]


@pytest.mark.rrule
@pytest.mark.bva
@pytest.mark.order(3)
@pytest.mark.parametrize("count_val,expected_len", [
    (0, 0),
    (1, 1),
    (2, 2),
    (10, 10),
])
def test_count_boundary_values(count_val, expected_len):
    """
    Test recurrence count boundaries at min valid (0, 1) and typical values (BVA).
    Author: M. Ibrahim Asif (24F-3070)
    """
    start = datetime(2024, 5, 1)
    rule = rrule(DAILY, count=count_val, dtstart=start)
    occurrences = list(rule)
    assert len(occurrences) == expected_len


@pytest.mark.rrule
@pytest.mark.bva
@pytest.mark.order(3)
@pytest.mark.parametrize("interval_val,expected_days", [
    (1, [1, 2, 3, 4]),
    (2, [1, 3, 5, 7]),
    (3, [1, 4, 7, 10]),
])
def test_daily_interval_stepping(interval_val, expected_days):
    """
    Test day stepping according to interval boundaries (BVA).
    Author: M. Ibrahim Asif (24F-3070)
    """
    start = datetime(2024, 6, 1)
    rule = rrule(DAILY, interval=interval_val, count=4, dtstart=start)
    occurrences = list(rule)

    assert [occ.day for occ in occurrences] == expected_days


@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.order(2)
def test_between_query_method():
    """
    Test between() method returning subset within date range (ECP).
    Author: M. Ibrahim Asif (24F-3070)
    """
    start = datetime(2024, 1, 1)
    rule = rrule(DAILY, count=10, dtstart=start)

    # Search between Jan 3 and Jan 6
    sub = rule.between(datetime(2024, 1, 3), datetime(2024, 1, 6), inc=True)
    assert len(sub) == 4
    assert sub[0] == datetime(2024, 1, 3)
    assert sub[-1] == datetime(2024, 1, 6)

    # Exclusive boundary
    sub_ex = rule.between(datetime(2024, 1, 3), datetime(2024, 1, 6), inc=False)
    assert len(sub_ex) == 2
    assert sub_ex[0] == datetime(2024, 1, 4)
    assert sub_ex[-1] == datetime(2024, 1, 5)


@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.order(2)
def test_after_and_before_query_methods():
    """
    Test after() and before() lookup methods (ECP).
    Author: M. Ibrahim Asif (24F-3070)
    """
    start = datetime(2024, 1, 1)
    rule = rrule(DAILY, count=5, dtstart=start)

    nxt = rule.after(datetime(2024, 1, 2), inc=False)
    assert nxt == datetime(2024, 1, 3)

    nxt_inc = rule.after(datetime(2024, 1, 2), inc=True)
    assert nxt_inc == datetime(2024, 1, 2)

    prev = rule.before(datetime(2024, 1, 4), inc=False)
    assert prev == datetime(2024, 1, 3)


# ==============================================================================
# Ahmad's Tests (24F-3040) - Sub-daily, Weekdays, Until, Monthday, Rruleset
# ==============================================================================

@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.order(2)
def test_hourly_frequency():
    """
    Test sub-daily HOURLY recurrence generation (ECP).
    Author: M. Ahmad (24F-3040)
    """
    start = datetime(2024, 1, 1, 8, 0, 0)
    rule = rrule(HOURLY, count=4, interval=2, dtstart=start)
    occurrences = list(rule)

    assert len(occurrences) == 4
    assert occurrences[0] == datetime(2024, 1, 1, 8, 0, 0)
    assert occurrences[1] == datetime(2024, 1, 1, 10, 0, 0)
    assert occurrences[2] == datetime(2024, 1, 1, 12, 0, 0)
    assert occurrences[3] == datetime(2024, 1, 1, 14, 0, 0)


@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.order(2)
@pytest.mark.parametrize("weekdays,expected_days", [
    (MO, [1, 8, 15]),
    ((MO, FR), [1, 5, 8, 12, 15]),
])
def test_byweekday_filtering(weekdays, expected_days):
    """
    Test filtering by single and multiple weekdays (ECP).
    Author: M. Ahmad (24F-3040)
    """
    # 2024-01-01 is a Monday
    start = datetime(2024, 1, 1)
    rule = rrule(DAILY, count=len(expected_days), byweekday=weekdays, dtstart=start)
    occurrences = list(rule)

    assert [occ.day for occ in occurrences] == expected_days


@pytest.mark.rrule
@pytest.mark.bva
@pytest.mark.order(3)
def test_until_boundary_equals_dtstart():
    """
    Test boundary condition where until equals dtstart (BVA).
    Should produce exactly one occurrence.
    Author: M. Ahmad (24F-3040)
    """
    start = datetime(2024, 3, 10, 12, 0, 0)
    rule = rrule(DAILY, dtstart=start, until=start)
    occurrences = list(rule)

    assert len(occurrences) == 1
    assert occurrences[0] == start


@pytest.mark.rrule
@pytest.mark.bva
@pytest.mark.order(3)
def test_until_boundary_range():
    """
    Test until boundary terminating recurrence on an exact limit date (BVA).
    Author: M. Ahmad (24F-3040)
    """
    start = datetime(2024, 1, 1)
    until_dt = datetime(2024, 1, 5)
    rule = rrule(DAILY, dtstart=start, until=until_dt)
    occurrences = list(rule)

    assert len(occurrences) == 5
    assert occurrences[-1] == until_dt


@pytest.mark.rrule
@pytest.mark.bva
@pytest.mark.order(3)
def test_bymonthday_month_end_filtering():
    """
    Test bymonthday=31 skips February, April, June etc. (BVA).
    Author: M. Ahmad (24F-3040)
    """
    start = datetime(2024, 1, 1)
    rule = rrule(MONTHLY, count=4, bymonthday=31, dtstart=start)
    occurrences = list(rule)

    # 31-day months: Jan, Mar, May, Jul
    assert [occ.month for occ in occurrences] == [1, 3, 5, 7]
    assert all(occ.day == 31 for occ in occurrences)


@pytest.mark.rrule
@pytest.mark.bva
@pytest.mark.order(3)
def test_negative_bymonthday_last_day():
    """
    Test negative bymonthday=-1 selects the actual last day of each month (BVA).
    Handles 31-day, 29-day (leap), and 30-day months correctly.
    Author: M. Ahmad (24F-3040)
    """
    start = datetime(2024, 1, 1)
    rule = rrule(MONTHLY, count=4, bymonthday=-1, dtstart=start)
    occurrences = list(rule)

    assert occurrences[0] == datetime(2024, 1, 31)
    assert occurrences[1] == datetime(2024, 2, 29)  # 2024 is leap year
    assert occurrences[2] == datetime(2024, 3, 31)
    assert occurrences[3] == datetime(2024, 4, 30)


@pytest.mark.rrule
@pytest.mark.ecp
@pytest.mark.order(2)
def test_rruleset_with_exdate():
    """
    Test rruleset combining a rule with an excluded date exdate (ECP).
    Author: M. Ahmad (24F-3040)
    """
    start = datetime(2024, 1, 1)
    rset = rruleset()
    rset.rrule(rrule(DAILY, count=5, dtstart=start))
    rset.exdate(datetime(2024, 1, 3))

    occurrences = list(rset)
    assert len(occurrences) == 4
    assert datetime(2024, 1, 3) not in occurrences
    assert [occ.day for occ in occurrences] == [1, 2, 4, 5]
