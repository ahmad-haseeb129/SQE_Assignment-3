# ECP/BVA Analysis — `dateutil.rrule`

## Module Overview
`rrule` generates recurrence rules (RFC 2445) — repeating date/time sequences like "every Monday", "monthly on the 15th", etc.

---

## Equivalence Class Partitioning (ECP)

### Input: Frequency (`freq`)

| Class ID | Equivalence Class | Valid/Invalid | Example                                |
|----------|-------------------|---------------|----------------------------------------|
| EC1      | YEARLY            | Valid         | `rrule(YEARLY, dtstart=dt)`            |
| EC2      | MONTHLY           | Valid         | `rrule(MONTHLY, dtstart=dt)`           |
| EC3      | WEEKLY            | Valid         | `rrule(WEEKLY, dtstart=dt)`            |
| EC4      | DAILY             | Valid         | `rrule(DAILY, dtstart=dt)`             |
| EC5      | HOURLY            | Valid         | `rrule(HOURLY, dtstart=dt)`            |
| EC6      | MINUTELY          | Valid         | `rrule(MINUTELY, dtstart=dt)`          |
| EC7      | SECONDLY          | Valid         | `rrule(SECONDLY, dtstart=dt)`          |
| EC8      | Invalid freq value| Invalid       | `rrule(99, dtstart=dt)`                |

### Input: `count` Parameter (Limit Results)

| Class ID | Equivalence Class    | Valid/Invalid | Example                        |
|----------|----------------------|---------------|--------------------------------|
| CT1      | count=1 (single)     | Valid         | Produces exactly 1 occurrence  |
| CT2      | count=5 (small)      | Valid         | Produces exactly 5 occurrences |
| CT3      | count=0              | Valid/Edge    | Produces 0 occurrences         |
| CT4      | count=None (no limit)| Valid         | Infinite (needs `until`)       |

### Input: `interval` Parameter

| Class ID | Equivalence Class    | Valid/Invalid | Example                         |
|----------|----------------------|---------------|---------------------------------|
| IV1      | interval=1 (default) | Valid         | Every day/month/etc.            |
| IV2      | interval=2           | Valid         | Every other day/month/etc.      |
| IV3      | interval=0           | Invalid/Edge  | No progression                  |
| IV4      | Large interval       | Valid         | `interval=100`                  |

### Input: `byweekday` Parameter

| Class ID | Equivalence Class      | Valid/Invalid | Example                      |
|----------|------------------------|---------------|------------------------------|
| WD1      | Single weekday         | Valid         | `byweekday=MO`               |
| WD2      | Multiple weekdays      | Valid         | `byweekday=(MO, WE, FR)`     |
| WD3      | Nth weekday of month   | Valid         | `byweekday=MO(+1)` (1st Mon) |
| WD4      | Last weekday of month  | Valid         | `byweekday=FR(-1)` (last Fri)|

### Input: `until` Parameter

| Class ID | Equivalence Class      | Valid/Invalid | Example                                 |
|----------|------------------------|---------------|-----------------------------------------|
| UN1      | until > dtstart        | Valid         | Normal range                            |
| UN2      | until == dtstart       | Valid/Edge    | Only dtstart included                   |
| UN3      | until < dtstart        | Valid/Edge    | Empty result                            |

### Input: `dtstart` Parameter

| Class ID | Equivalence Class      | Valid/Invalid | Example                    |
|----------|------------------------|---------------|----------------------------|
| DS1      | Specific datetime      | Valid         | `datetime(2024, 1, 1)`     |
| DS2      | None (uses now)        | Valid         | Default behavior           |

---

## Boundary Value Analysis (BVA)

### Count Boundaries

| Boundary   | Value  | Expected                       |
|------------|--------|--------------------------------|
| Min        | 0      | 0 occurrences                  |
| Min + 1    | 1      | Exactly 1 occurrence           |
| Typical    | 10     | Exactly 10 occurrences         |
| Large      | 1000   | Exactly 1000 occurrences       |

### Interval Boundaries

| Boundary   | Value  | Expected                       |
|------------|--------|--------------------------------|
| Min valid  | 1      | Normal frequency               |
| Step       | 2      | Every other period             |
| Large      | 365    | Once per year (daily + 365)    |

### Date Boundaries (Start/End)

| Scenario                     | Expected                                   |
|------------------------------|-------------------------------------------|
| dtstart = Jan 1, until = Jan 1  | 1 occurrence (only Jan 1)              |
| dtstart = Dec 31, YEARLY       | Crosses year boundary correctly          |
| dtstart = Feb 29 (leap), YEARLY | Handles non-leap years correctly        |

### `bymonthday` Boundaries

| Scenario                     | Expected                                   |
|------------------------------|-------------------------------------------|
| bymonthday=31, MONTHLY      | Skips months with < 31 days               |
| bymonthday=29, MONTHLY      | Skips Feb in non-leap years               |
| bymonthday=1, MONTHLY       | Every 1st of month                        |

---

## Test Strategy Summary

**Ibrahim (24F-3070)** will test:
- EC1–EC4: Frequency types (YEARLY, MONTHLY, WEEKLY, DAILY)
- CT1–CT4: Count parameter testing
- BVA for count and interval boundaries
- `between()` method behavior

**Ahmad (24F-3040)** will test:
- EC5–EC8: Higher frequencies and invalid inputs
- WD1–WD4: Weekday filtering
- UN1–UN3: `until` parameter edge cases
- `bymonthday` boundary behavior
- `rruleset` (combining multiple rules)
