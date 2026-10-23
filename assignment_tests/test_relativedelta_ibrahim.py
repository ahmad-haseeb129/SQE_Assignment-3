"""
Automated Unit Tests for dateutil.relativedelta
Author: M. Ibrahim Asif (Roll No: 24F-3070)
Testing Techniques: ECP & BVA
"""
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


@pytest.mark.smoke
def test_identity_offset():
    """ECP: Empty relativedelta acts as identity returning same date."""
    base = date(2024, 6, 15)
    assert base + relativedelta() == base


@pytest.mark.parametrize("delta,expected", [
    (relativedelta(years=+1), date(2025, 1, 15)),
    (relativedelta(years=-1), date(2023, 1, 15)),
    (relativedelta(months=+3), date(2024, 4, 15)),
    (relativedelta(months=-3), date(2023, 10, 15)),
])
def test_basic_offsets(delta, expected):
    """ECP: Relative year and month addition and subtraction."""
    base = date(2024, 1, 15)
    assert base + delta == expected


def test_combined_offsets():
    """ECP: Adding compound offsets with years, months, and days."""
    base = date(2024, 1, 15)
    delta = relativedelta(years=1, months=2, days=5)
    assert base + delta == date(2025, 3, 20)


def test_multiplication_scaling():
    """ECP: Multiplying relativedelta scales internal components."""
    delta = relativedelta(months=2, days=3)
    res = delta * 3
    assert res == relativedelta(months=6, days=9)


@pytest.mark.boundary
@pytest.mark.parametrize("base,delta,expected", [
    (date(2024, 1, 31), relativedelta(months=1), date(2024, 2, 29)),
    (date(2023, 1, 31), relativedelta(months=1), date(2023, 2, 28)),
    (date(2024, 3, 31), relativedelta(months=-1), date(2024, 2, 29)),
    (date(2024, 5, 31), relativedelta(months=1), date(2024, 6, 30)),
])
def test_month_end_overflow_boundaries(base, delta, expected):
    """BVA: Month-end overflow correctly clamps to month range for leap and non-leap years."""
    assert base + delta == expected


@pytest.mark.boundary
def test_leap_year_boundary_offset():
    """BVA: Adding 1 year to Feb 29 clamps to Feb 28 in non-leap year."""
    leap_date = date(2024, 2, 29)
    assert leap_date + relativedelta(years=1) == date(2025, 2, 28)
    assert leap_date + relativedelta(years=-1) == date(2023, 2, 28)
