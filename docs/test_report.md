# SQE Assignment 3 — Test Execution & Summary Report

## Project Details
- **Course:** Software Quality Engineering
- **Assignment:** Assignment 3 — Build Unit Test Automation Solution
- **Target Application:** [python-dateutil](https://github.com/dateutil/dateutil) (Python)
- **Repository:** [https://github.com/ahmad-haseeb129/SQE_Assignment-3](https://github.com/ahmad-haseeb129/SQE_Assignment-3)

## Team Information
| Member | Roll Number | Role / Contribution Focus |
|---|---|---|
| **M. Ibrahim Asif** | 24F-3070 | Project scaffolding, `parser` and `relativedelta` test suites, ECP/BVA test design notes, CSV tests |
| **M. Ahmad** | 24F-3040 | `rrule` test suite, edge-case test design, CSV datasets, Excel test case matrix, parallel & ordering configuration |

---

## 1. Executive Summary
A comprehensive automated unit test suite was implemented for 3 core modules of `python-dateutil` using `pytest`. The test design incorporates black-box testing techniques including **Equivalence Class Partitioning (ECP)**, **Boundary Value Analysis (BVA)**, and **Data-Driven Testing (CSV)**.

### Test Execution Summary
- **Total Test Cases Executed:** 110 passed
- **Failures / Errors:** 0
- **Warnings:** 0
- **Execution Time (Sequential):** ~0.17 seconds
- **Execution Time (Parallel with 20 workers):** ~3.2 seconds
- **Overall Status:** 100% PASSED

---

## 2. Test Architecture & Selected Modules

### Module 1: `dateutil.parser`
- **Tested Components:** `parse()`, `ParserError`, timezone handlers, flags (`dayfirst`, `yearfirst`, `fuzzy`)
- **Techniques Applied:**
  - ECP: ISO 8601 strings, US slash format, written months, abbreviated months, date-time combinations, numeric-only strings, invalid input types (empty string, non-date tokens, `None`).
  - BVA: Minimum year (`0001`), maximum year (`9999`), month boundaries (1, 12), day boundaries (1, 28/29/30/31), leap year validation (Feb 29 valid for 2024 vs invalid for 2023), time boundaries (`00:00:00` vs `23:59:59`).

### Module 2: `dateutil.relativedelta`
- **Tested Components:** `relativedelta` class, arithmetic operators (`+`, `-`, `*`), negation, identity
- **Techniques Applied:**
  - ECP: Positive/negative year/month/day offsets, combined relative deltas, absolute replacements (`month=`, `day=`), delta computation between distinct `datetime` instances, identity element.
  - BVA: Month-end overflow in leap years (Jan 31 + 1 month = Feb 29) vs non-leap years (Jan 31 + 1 month = Feb 28), leap day year increments (Feb 29 + 1 year = Feb 28), year boundary crossing (Dec 31 + 1 day = Jan 1), 100-year offsets, invalid float months (`ValueError`).

### Module 3: `dateutil.rrule`
- **Tested Components:** `rrule`, `rruleset`, recurrence frequencies (`YEARLY`, `MONTHLY`, `WEEKLY`, `DAILY`, `HOURLY`), filtering parameters (`byweekday`, `bymonthday`, `until`, `interval`, `count`)
- **Techniques Applied:**
  - ECP: Annual recurrences, multi-frequency progressions, single and compound weekday filters (`MO`, `(MO, FR)`), hourly sub-daily intervals, exclusion rules via `exdate`, date range filtering with `between()`, next/prior lookup with `after()` / `before()`.
  - BVA: Recurrence count lower bounds (`count=0`, `count=1`), interval stepping boundaries (`interval=1, 2, 3`), boundary `until == dtstart`, month-end day filter (`bymonthday=31` skipping short months), negative month-day indexing (`bymonthday=-1` capturing actual last day of each month).

---

## 3. Data-Driven Testing (Task 3)
Test datasets are decoupled from test code into external CSV files under `test_data/`:
1. `parser_test_data.csv`: Valid and error-inducing date/time strings with expected date components and error assertions.
2. `relativedelta_test_data.csv`: Start dates, relative offsets, and expected post-arithmetic date values.
3. `rrule_test_data.csv`: Recurrence frequency rules, intervals, and count constraints with expected generated counts.

All CSV datasets are consumed via the `load_csv_data` utility in `tests/conftest.py` and executed dynamically with `@pytest.mark.parametrize` in `tests/test_csv_driven.py`.

---

## 4. Test Configuration & Execution Strategy (Task 4)
- **Parallel Testing:** Configured via `pytest-xdist`. Tests can be executed in parallel using `pytest -n auto` or `pytest -n <workers>`.
- **Suite Partitioning:** Categorized using custom markers registered in `pytest.ini`:
  - Module suites: `pytest -m parser`, `pytest -m relativedelta`, `pytest -m rrule`
  - Technique suites: `pytest -m ecp`, `pytest -m bva`, `pytest -m csv_driven`
  - Quick smoke verification: `pytest -m smoke`
- **Execution Ordering:** Prioritized using `pytest-ordering` (`order(1)` for smoke, `order(2)` for equivalence partitions, `order(3)` for boundary edge cases).

---

## 5. Artifacts Checklist
- [x] Local development environment setup & verification
- [x] Project source code included (`dateutil/`)
- [x] ECP/BVA test design notes committed (`notes/`)
- [x] Automated unit test suites committed (`tests/`)
- [x] External CSV test data files (`test_data/`)
- [x] Excel test case matrix (`docs/test_cases.xlsx`)
- [x] Pytest configuration (`pytest.ini`, `requirements.txt`)
- [x] Git commit history partitioned between both group members
- [x] Setup demonstration video recording instructions in README
