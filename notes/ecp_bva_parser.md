# ECP/BVA Analysis — `dateutil.parser`

## Module Overview
The `dateutil.parser.parse()` function parses human-readable date/time strings into `datetime` objects.

---

## Equivalence Class Partitioning (ECP)

### Input: Date String Format

| Class ID | Equivalence Class           | Valid/Invalid | Example                    |
|----------|-----------------------------|---------------|----------------------------|
| EC1      | ISO 8601 format             | Valid         | `"2024-01-15"`             |
| EC2      | US format (MM/DD/YYYY)      | Valid         | `"01/15/2024"`             |
| EC3      | Written month name          | Valid         | `"January 15, 2024"`       |
| EC4      | Abbreviated month           | Valid         | `"Jan 15, 2024"`           |
| EC5      | Date with time              | Valid         | `"2024-01-15 14:30:00"`    |
| EC6      | Date with timezone           | Valid         | `"2024-01-15T14:30:00+05:00"` |
| EC7      | Relative/ambiguous string    | Valid         | `"15/01/2024"` with dayfirst=True |
| EC8      | Empty string                | Invalid       | `""`                       |
| EC9      | Random non-date text        | Invalid       | `"hello world"`            |
| EC10     | None input                  | Invalid       | `None`                     |
| EC11     | Numeric-only string         | Valid         | `"20240115"`               |

### Input: `dayfirst` Parameter

| Class ID | Equivalence Class | Valid/Invalid | Example            |
|----------|-------------------|---------------|--------------------|
| DF1      | dayfirst=False    | Valid         | `"01/02/2024"` → Jan 2 |
| DF2      | dayfirst=True     | Valid         | `"01/02/2024"` → Feb 1 |

### Input: `yearfirst` Parameter

| Class ID | Equivalence Class  | Valid/Invalid | Example              |
|----------|--------------------|---------------|----------------------|
| YF1      | yearfirst=False    | Valid         | `"01/02/03"` → 2003  |
| YF2      | yearfirst=True     | Valid         | `"01/02/03"` → Jan   |

### Input: `fuzzy` Parameter

| Class ID | Equivalence Class      | Valid/Invalid | Example                          |
|----------|------------------------|---------------|----------------------------------|
| FZ1      | fuzzy=False, clean     | Valid         | `"2024-01-15"`                   |
| FZ2      | fuzzy=True, noisy      | Valid         | `"The date is Jan 15, 2024 ok"`  |
| FZ3      | fuzzy=False, noisy     | Invalid       | `"The date is Jan 15, 2024 ok"`  |

---

## Boundary Value Analysis (BVA)

### Date Component Boundaries

| Boundary           | Min         | Just Below   | Just Above  | Max          |
|--------------------|-------------|--------------|-------------|--------------|
| Year               | `0001`      | N/A          | `0001`      | `9999`       |
| Month              | `01`        | `00` (invalid)| `01`       | `12`         |
| Day (31-day month) | `01`        | `00` (invalid)| `01`       | `31`         |
| Day (30-day month) | `01`        | `32` (invalid)| `01`       | `30`         |
| Day (Feb, non-leap)| `01`        | `29` (invalid)| `01`       | `28`         |
| Day (Feb, leap yr) | `01`        | `30` (invalid)| `01`       | `29`         |

### Time Component Boundaries

| Boundary   | Min    | Max      | Beyond Max  |
|------------|--------|----------|-------------|
| Hour       | `00`   | `23`     | `24` (edge) |
| Minute     | `00`   | `59`     | `60` (invalid) |
| Second     | `00`   | `59`     | `60` (leap second edge) |

### Special Dates to Test
- `"0001-01-01"` — minimum datetime
- `"9999-12-31"` — maximum datetime
- `"2024-02-29"` — leap year Feb 29
- `"2023-02-29"` — non-leap year Feb 29 (invalid)
- `"2024-12-31"` — year-end boundary
- `"2024-01-01"` — year-start boundary

---

## Test Strategy Summary

**Ibrahim (24F-3070)** will test:
- EC1–EC6: Standard date format parsing
- BVA for date boundaries (min/max year, month, day)
- `dayfirst` / `yearfirst` parameter behavior

**Ahmad (24F-3040)** will test:
- EC7–EC11: Edge cases and invalid inputs
- BVA for time boundaries (hour, minute, second)
- `fuzzy` parameter behavior
- Error handling for malformed inputs
