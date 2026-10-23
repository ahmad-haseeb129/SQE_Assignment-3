"""
Unit Tests for dateutil.relativedelta module
SQE Assignment 3
- M. Ibrahim Asif (24F-3070)
- M. Ahmad (24F-3040)

This module contains comprehensive pytest unit tests for the
dateutil.relativedelta class, covering basic offsets, month-end overflow,
leap year handling, arithmetic operations, absolute parameters,
datetime deltas, and year-boundary crossing scenarios.

Test design techniques used:
- Equivalence Class Partitioning (ECP)
- Boundary Value Analysis (BVA)
"""

import pytest
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# Ibrahim's Tests (24F-3070) — basic offsets, overflow, leap year, arithmetic
# ---------------------------------------------------------------------------


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
@pytest.mark.parametrize(
    "base, delta, expected",
    [
        pytest.param(
            date(2024, 1, 15),
            relativedelta(years=1),
            date(2025, 1, 15),
            id="positive_year_offset",
        ),
        pytest.param(
            date(2024, 6, 15),
            relativedelta(years=-1),
            date(2023, 6, 15),
            id="negative_year_offset",
        ),
        pytest.param(
            date(2024, 1, 15),
            relativedelta(months=3),
            date(2024, 4, 15),
            id="positive_month_offset",
        ),
        pytest.param(
            date(2024, 6, 15),
            relativedelta(months=-3),
            date(2024, 3, 15),
            id="negative_month_offset",
        ),
    ],
)
def test_basic_year_and_month_offsets(base, delta, expected):
    """ECP: Verify that adding positive/negative year and month offsets
    to a date produces the correct result across distinct equivalence
    classes (positive years, negative years, positive months, negative
    months)."""
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
def test_combined_offsets():
    """ECP: Verify that combining year, month, and day offsets in a single
    relativedelta applies all components correctly."""
    base = date(2024, 1, 15)
    delta = relativedelta(years=1, months=2, days=5)
    expected = date(2025, 3, 20)
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.bva
@pytest.mark.order(3)
@pytest.mark.parametrize(
    "base, delta, expected",
    [
        pytest.param(
            date(2024, 1, 31),
            relativedelta(months=1),
            date(2024, 2, 29),
            id="month_end_overflow_leap_year",
        ),
        pytest.param(
            date(2023, 1, 31),
            relativedelta(months=1),
            date(2023, 2, 28),
            id="month_end_overflow_non_leap_year",
        ),
    ],
)
def test_month_end_overflow(base, delta, expected):
    """BVA: When adding months causes the day to exceed the target month's
    last day, the result should clamp to the last valid day of that month.
    Tests both leap-year (Feb 29) and non-leap-year (Feb 28) boundaries."""
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.bva
@pytest.mark.order(3)
def test_leap_year_boundary():
    """BVA: Adding one year to Feb 29 of a leap year should clamp to
    Feb 28 of the following non-leap year."""
    base = date(2024, 2, 29)
    delta = relativedelta(years=1)
    expected = date(2025, 2, 28)
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.smoke
@pytest.mark.order(1)
def test_identity_offset():
    """Smoke / ECP: An empty relativedelta should act as the identity —
    adding it to any date returns the same date unchanged."""
    base = date(2024, 6, 15)
    assert base + relativedelta() == base


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
def test_multiplication():
    """ECP: Multiplying a relativedelta by an integer should scale every
    component proportionally."""
    delta = relativedelta(months=2, days=3)
    result = delta * 3
    expected = relativedelta(months=6, days=9)
    assert result == expected


# ---------------------------------------------------------------------------
# Ahmad's Tests (24F-3040) — zero/large offsets, absolute params, deltas,
#                              year boundaries, negation, error handling
# ---------------------------------------------------------------------------


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
def test_zero_offset():
    """ECP: A relativedelta with no arguments should leave the date
    completely unchanged (zero-offset equivalence class)."""
    base = date(2024, 3, 15)
    assert base + relativedelta() == base


@pytest.mark.relativedelta
@pytest.mark.bva
@pytest.mark.order(3)
def test_large_year_offset():
    """BVA: A very large year offset (100 years) should be handled
    correctly without overflow or error."""
    base = date(2024, 1, 1)
    delta = relativedelta(years=100)
    expected = date(2124, 1, 1)
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
@pytest.mark.parametrize(
    "base, delta, expected",
    [
        pytest.param(
            date(2024, 6, 15),
            relativedelta(month=1),
            date(2024, 1, 15),
            id="absolute_month",
        ),
        pytest.param(
            date(2024, 6, 15),
            relativedelta(day=1),
            date(2024, 6, 1),
            id="absolute_day",
        ),
    ],
)
def test_absolute_parameters(base, delta, expected):
    """ECP: Singular keyword arguments (month=, day=) set the component
    to an absolute value rather than adding a relative offset."""
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
@pytest.mark.parametrize(
    "dt1, dt2, exp_years, exp_months, exp_days",
    [
        pytest.param(
            date(2025, 3, 15),
            date(2024, 1, 10),
            1, 2, 5,
            id="delta_between_two_dates",
        ),
        pytest.param(
            date(2024, 1, 1),
            date(2024, 1, 1),
            0, 0, 0,
            id="delta_same_dates",
        ),
    ],
)
def test_delta_between_dates(dt1, dt2, exp_years, exp_months, exp_days):
    """ECP: Computing the relativedelta between two dates should yield
    the correct year, month, and day components. Also verifies the zero-
    difference case."""
    rd = relativedelta(dt1, dt2)
    assert rd.years == exp_years
    assert rd.months == exp_months
    assert rd.days == exp_days


@pytest.mark.relativedelta
@pytest.mark.bva
@pytest.mark.order(3)
def test_year_boundary_crossing():
    """BVA: Adding one day to December 31 should cross the year boundary
    and produce January 1 of the next year."""
    base = date(2024, 12, 31)
    delta = relativedelta(days=1)
    expected = date(2025, 1, 1)
    assert base + delta == expected


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
def test_negation():
    """ECP: Negating a relativedelta should invert the sign of every
    component."""
    delta = relativedelta(years=1, months=2)
    neg = -delta
    assert neg == relativedelta(years=-1, months=-2)


@pytest.mark.relativedelta
@pytest.mark.ecp
@pytest.mark.order(2)
def test_non_integer_months_raises_value_error():
    """ECP: Passing a non-integer value for months (or years) must raise
    a ValueError because fractional months are ambiguous."""
    with pytest.raises(ValueError):
        relativedelta(months=1.5)
