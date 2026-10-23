# ECP/BVA Analysis — `dateutil.relativedelta`

## Module Overview
`relativedelta` provides advanced date arithmetic — adding/subtracting years, months, days, etc., with intelligent overflow handling (e.g., Jan 31 + 1 month = Feb 28).

---

## Equivalence Class Partitioning (ECP)

### Input: Relative Offset Parameters

| Class ID | Equivalence Class           | Valid/Invalid | Example                              |
|----------|-----------------------------|---------------|--------------------------------------|
| EC1      | Positive year offset        | Valid         | `relativedelta(years=+1)`            |
| EC2      | Negative year offset        | Valid         | `relativedelta(years=-1)`            |
| EC3      | Positive month offset       | Valid         | `relativedelta(months=+3)`           |
| EC4      | Negative month offset       | Valid         | `relativedelta(months=-3)`           |
| EC5      | Positive day offset         | Valid         | `relativedelta(days=+10)`            |
| EC6      | Negative day offset         | Valid         | `relativedelta(days=-10)`            |
| EC7      | Combined offsets             | Valid         | `relativedelta(years=1, months=2)`   |
| EC8      | Zero offset (identity)      | Valid         | `relativedelta()`                    |
| EC9      | Large offset                 | Valid         | `relativedelta(years=100)`           |
| EC10     | Absolute value (month=3)     | Valid         | `relativedelta(month=3)` (singular)  |

### Input: Absolute vs Relative Parameters

| Class ID | Equivalence Class            | Description                              |
|----------|------------------------------|------------------------------------------|
| ABS1     | `month=X` (singular)          | Sets month to X absolutely               |
| ABS2     | `months=X` (plural)           | Adds X months relatively                 |
| ABS3     | `day=X` (singular)            | Sets day to X absolutely                 |
| ABS4     | `days=X` (plural)             | Adds X days relatively                   |

### Input: Two datetime Objects (Delta Calculation)

| Class ID | Equivalence Class             | Example                                 |
|----------|-------------------------------|-----------------------------------------|
| DD1      | dt2 > dt1 (positive delta)    | `relativedelta(dt2, dt1)` where dt2 > dt1 |
| DD2      | dt2 < dt1 (negative delta)    | `relativedelta(dt2, dt1)` where dt2 < dt1 |
| DD3      | dt2 == dt1 (zero delta)       | `relativedelta(dt1, dt1)`               |
| DD4      | Cross-year boundary            | Dec 31 → Jan 1                          |
| DD5      | Cross-leap-year                | Feb 28 2023 → Feb 29 2024              |

---

## Boundary Value Analysis (BVA)

### Month-End Overflow Boundaries

| Scenario                       | Input                    | Expected Result         |
|--------------------------------|--------------------------|-------------------------|
| Jan 31 + 1 month               | `date(2024,1,31) + relativedelta(months=1)` | Feb 29 (leap) |
| Jan 31 + 1 month (non-leap)    | `date(2023,1,31) + relativedelta(months=1)` | Feb 28         |
| Mar 31 - 1 month               | `date(2024,3,31) + relativedelta(months=-1)` | Feb 29 (leap) |
| May 31 + 1 month               | `date(2024,5,31) + relativedelta(months=1)` | Jun 30         |

### Leap Year Boundaries

| Scenario                       | Input                    | Expected Result         |
|--------------------------------|--------------------------|-------------------------|
| Feb 29 + 1 year                | `date(2024,2,29) + relativedelta(years=1)` | Feb 28, 2025   |
| Feb 29 - 1 year                | `date(2024,2,29) + relativedelta(years=-1)` | Feb 28, 2023  |
| Feb 28 + 1 day (leap year)     | `date(2024,2,28) + relativedelta(days=1)` | Feb 29, 2024   |
| Feb 28 + 1 day (non-leap)      | `date(2023,2,28) + relativedelta(days=1)` | Mar 1, 2023    |

### Year Boundaries

| Scenario                | Input                            | Expected Result         |
|-------------------------|----------------------------------|-------------------------|
| Dec 31 + 1 day          | `date(2024,12,31) + relativedelta(days=1)` | Jan 1, 2025 |
| Jan 1 - 1 day           | `date(2024,1,1) + relativedelta(days=-1)` | Dec 31, 2023 |
| Dec 31 + 1 month        | `date(2024,12,31) + relativedelta(months=1)` | Jan 31, 2025 |

### Arithmetic Properties

| Property          | Test                                                |
|-------------------|-----------------------------------------------------|
| Identity          | `dt + relativedelta() == dt`                        |
| Negation          | `dt + rd + (-rd)` should ≈ dt (not always exact)    |
| Addition          | `rd1 + rd2` should combine offsets correctly         |
| Multiplication    | `rd * 2` should double offsets                       |

---

## Test Strategy Summary

**Ibrahim (24F-3070)** will test:
- EC1–EC7: Basic offset operations (positive, negative, combined)
- BVA for month-end overflow and leap year boundaries
- Arithmetic properties (identity, addition, multiplication)

**Ahmad (24F-3040)** will test:
- EC8–EC10: Zero offset, large offset, absolute values
- ABS1–ABS4: Absolute vs relative parameter distinction
- DD1–DD5: Delta between two datetimes
- Year boundary transitions
