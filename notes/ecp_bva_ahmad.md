# ECP/BVA Test Design Notes — M. Ahmad (24F-3040)

**Project:** python-dateutil (version 3.0.0)  
**Modules Tested:** `dateutil.parser` (Edge/Fuzzy Cases) & `dateutil.rrule` (Recurrence Rules)  
**Author:** M. Ahmad (24F-3040)  
**Techniques Applied:** Equivalence Class Partitioning (ECP) & Boundary Value Analysis (BVA)  

---

## 1. `dateutil.parser.parse()` — Edge, Fuzzy & Boundaries

### Equivalence Class Partitioning (ECP)

| Partition ID | Input Condition | Test Case / Vector | Expected Result | Status |
|---|---|---|---|---|
| EC_PE_01 | Empty string input | `parse("")` | Raises `ParserError` | Tested & Verified |
| EC_PE_02 | Non-date conversational text | `parse("hello world not a date")` | Raises `ParserError` | Tested & Verified |
| EC_PE_03 | None object input | `parse(None)` | Raises `TypeError` | Tested & Verified |
| EC_PE_04 | Continuous numeric string | `parse("20240115")` | Parsed to `datetime(2024, 1, 15)` | Tested & Verified |
| EC_PE_05 | Conversational sentence | `parse(..., fuzzy=True)` | Extracted embedded date `datetime(2024, 1, 15)` | Tested & Verified |
| EC_PE_06 | Explicit timezone offset | `parse("2024-01-15T14:30:00+05:00")` | Preserved tzinfo with +5hr offset | Tested & Verified |

### Boundary Value Analysis (BVA)

| Boundary ID | Target Boundary | Input Vector | Expected Output | Status |
|---|---|---|---|---|
| BV_PE_01 | Midnight start boundary | `2024-01-15 00:00:00` | `hour=0, minute=0, second=0` | Tested & Verified |
| BV_PE_02 | End-of-day boundary | `2024-01-15 23:59:59` | `hour=23, minute=59, second=59` | Tested & Verified |
| BV_PE_03 | Invalid non-leap Feb 29 | `2023-02-29` | Raises `ParserError` | Tested & Verified |
| BV_PE_04 | Day above maximum (32) | `32/01/2024` | Raises `ParserError` | Tested & Verified |

---

## 2. `dateutil.rrule.rrule` — Recurrence Rules & Sets

### Equivalence Class Partitioning (ECP)

| Partition ID | Input Class | Test Configuration | Expected Output | Status |
|---|---|---|---|---|
| EC_RR_01 | YEARLY recurrence | `rrule(YEARLY, count=3, dtstart=...)` | 3 exact annual dates | Tested & Verified |
| EC_RR_02 | MONTHLY recurrence | `rrule(MONTHLY, count=3, dtstart=...)` | 3 monthly occurrences on day 15 | Tested & Verified |
| EC_RR_03 | WEEKLY recurrence | `rrule(WEEKLY, count=3, dtstart=...)` | 3 weekly occurrences (7-day delta) | Tested & Verified |
| EC_RR_04 | Sub-daily HOURLY | `rrule(HOURLY, interval=2, count=3)` | 3 intervals separated by 2 hours | Tested & Verified |
| EC_RR_05 | Single weekday filter | `rrule(DAILY, byweekday=MO, count=3)` | Only Mondays returned | Tested & Verified |
| EC_RR_06 | Multiple weekday filter | `rrule(DAILY, byweekday=(MO,FR), count=5)` | Only Mondays & Fridays | Tested & Verified |
| EC_RR_07 | rruleset exclusion | `rset.rrule(...)` + `rset.exdate(...)` | Excluded date omitted from output | Tested & Verified |

### Boundary Value Analysis (BVA)

| Boundary ID | Target Boundary | Input Configuration | Expected Output | Status |
|---|---|---|---|---|
| BV_RR_01 | Recurrence count lower min | `count=0` | Exactly 0 occurrences | Tested & Verified |
| BV_RR_02 | Recurrence count boundary | `count=1` | Exactly 1 occurrence (dtstart) | Tested & Verified |
| BV_RR_03 | Limit `until` equals `dtstart` | `until = dtstart` | Exactly 1 occurrence | Tested & Verified |
| BV_RR_04 | Month-end 31-day filter | `MONTHLY, bymonthday=31` | Skips Feb, Apr, Jun, Sep, Nov | Tested & Verified |
| BV_RR_05 | Dynamic last day indexing | `MONTHLY, bymonthday=-1` | Yields Jan 31, Feb 29, Mar 31, Apr 30 | Tested & Verified |
