# ECP/BVA Test Design Notes — M. Ibrahim Asif (24F-3070)

**Project:** python-dateutil (version 3.0.0)  
**Modules Tested:** `dateutil.parser` (Standard Formats & Dates) & `dateutil.relativedelta` (Relative Arithmetic)  
**Author:** M. Ibrahim Asif (24F-3070)  
**Techniques Applied:** Equivalence Class Partitioning (ECP) & Boundary Value Analysis (BVA)  

---

## 1. `dateutil.parser.parse()` — Standard Formats

### Equivalence Class Partitioning (ECP)

| Partition ID | Input Class / Format | Condition | Expected Result | Status |
|---|---|---|---|---|
| EC_P_01 | ISO 8601 string (`YYYY-MM-DD`) | Valid standard date format | Correct `datetime` instance with midnight time | Tested & Verified |
| EC_P_02 | US format (`MM/DD/YYYY`) | Valid slash separated date | Correct `datetime` with month interpreted first | Tested & Verified |
| EC_P_03 | Written month names (`January 15, 2024`) | Full month name spelling | Parsed to month number (1) | Tested & Verified |
| EC_P_04 | Abbreviated month (`Jan 15, 2024`) | 3-letter month abbreviation | Parsed to month number (1) | Tested & Verified |
| EC_P_05 | Date with timestamp (`YYYY-MM-DD HH:MM:SS`) | Timestamp appended | Date and time fields preserved accurately | Tested & Verified |
| EC_P_06 | Ambiguous date (`01/02/2024`) with `dayfirst=True` | Flag `dayfirst=True` | Day=1, Month=2 | Tested & Verified |
| EC_P_07 | Ambiguous date (`01/02/2024`) with `dayfirst=False` | Flag `dayfirst=False` | Month=1, Day=2 | Tested & Verified |

### Boundary Value Analysis (BVA)

| Boundary ID | Target Boundary | Test Input | Expected Result | Status |
|---|---|---|---|---|
| BV_P_01 | Minimum supported year | `0001-01-01` | `datetime(1, 1, 1)` | Tested & Verified |
| BV_P_02 | Maximum supported year | `9999-12-31` | `datetime(9999, 12, 31)` | Tested & Verified |
| BV_P_03 | Start of month boundary | `2024-01-01` | `day=1` | Tested & Verified |
| BV_P_04 | End of 31-day month | `2024-01-31` | `day=31` | Tested & Verified |
| BV_P_05 | End of 30-day month | `2024-04-30` | `day=30` | Tested & Verified |
| BV_P_06 | Leap day boundary (leap year) | `2024-02-29` | `year=2024, month=2, day=29` | Tested & Verified |
| BV_P_07 | Feb boundary (non-leap year) | `2023-02-28` | `year=2023, month=2, day=28` | Tested & Verified |

---

## 2. `dateutil.relativedelta.relativedelta` — Date Arithmetic

### Equivalence Class Partitioning (ECP)

| Partition ID | Input Class | Test Vector | Expected Output | Status |
|---|---|---|---|---|
| EC_RD_01 | Identity element (zero offset) | `base + relativedelta()` | Unmodified `base` date | Tested & Verified |
| EC_RD_02 | Positive year offset | `date(2024,1,15) + relativedelta(years=1)` | `date(2025, 1, 15)` | Tested & Verified |
| EC_RD_03 | Negative year offset | `date(2024,1,15) + relativedelta(years=-1)` | `date(2023, 1, 15)` | Tested & Verified |
| EC_RD_04 | Positive month offset | `date(2024,1,15) + relativedelta(months=3)` | `date(2024, 4, 15)` | Tested & Verified |
| EC_RD_05 | Compound relative delta | `base + relativedelta(years=1, months=2, days=5)` | `date(2025, 3, 20)` | Tested & Verified |
| EC_RD_06 | Scalar multiplication | `relativedelta(months=2, days=3) * 3` | `relativedelta(months=6, days=9)` | Tested & Verified |

### Boundary Value Analysis (BVA)

| Boundary ID | Target Boundary | Input Vector | Expected Output | Status |
|---|---|---|---|---|
| BV_RD_01 | Month-end roll into Leap Feb | `date(2024,1,31) + relativedelta(months=1)` | `date(2024, 2, 29)` (clamped to 29) | Tested & Verified |
| BV_RD_02 | Month-end roll into Non-Leap Feb | `date(2023,1,31) + relativedelta(months=1)` | `date(2023, 2, 28)` (clamped to 28) | Tested & Verified |
| BV_RD_03 | Negative month roll into Leap Feb | `date(2024,3,31) + relativedelta(months=-1)` | `date(2024, 2, 29)` (clamped to 29) | Tested & Verified |
| BV_RD_04 | Month-end roll into 30-day month | `date(2024,5,31) + relativedelta(months=1)` | `date(2024, 6, 30)` (clamped to 30) | Tested & Verified |
| BV_RD_05 | Feb 29 plus 1 year (leap to non-leap) | `date(2024,2,29) + relativedelta(years=1)` | `date(2025, 2, 28)` | Tested & Verified |
| BV_RD_06 | Feb 29 minus 1 year (leap to non-leap) | `date(2024,2,29) + relativedelta(years=-1)` | `date(2023, 2, 28)` | Tested & Verified |
