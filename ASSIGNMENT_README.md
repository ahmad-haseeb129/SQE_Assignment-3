# Assignment 3: Unit Test Automation (python-dateutil)

Project: [python-dateutil](https://github.com/dateutil/dateutil) (version 3.0.0)  
Course: Software Quality Engineering (CS-4001)  

## Team Members
| Name               | Roll No   |
|--------------------|-----------|
| M. Ibrahim Asif    | 24F-3070  |
| M. Ahmad           | 24F-3040  |

---

## Setup

```bash
git clone https://github.com/ahmad-haseeb129/SQE_Assignment-3.git
cd SQE_Assignment-3
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
pip install -e ./dateutil
pytest assignment_tests
```

Expected result: 89 passed in ~0.20s (100% pass rate).

- Setup evidence (terminal output): `assignment_docs/setup_output_ibrahim.txt` and `assignment_docs/setup_output_ahmad.txt`
- Setup video details: `assignment_docs/setup_video_link.txt`
- Excel Test Cases: `assignment_docs/test_cases_ibrahim.xlsx` and `assignment_docs/test_cases_ahmad.xlsx`

---

## Repository Layout

| Path | Contents |
|---|---|
| `notes/` | ECP/BVA test design notes, one file per member (`ecp_bva_ibrahim.md`, `ecp_bva_ahmad.md`) |
| `assignment_tests/` | Automated unit tests, `conftest.py` (suites and order hook) and `data/` (external CSV test data) |
| `assignment_docs/` | Setup output logs, setup video link, and Excel test case sheets |
| `pytest.ini` | Registers test suite markers (`parser`, `relativedelta`, `rrule`, `smoke`, `boundary`, `data_driven`) |
| `run_assignment_tests.py` | Helper CLI to run a suite or group, view order, or run in parallel |
| `ASSIGNMENT_README.md` | Assignment documentation |

---

## Running the Assignment Tests

Run these from the repository root with the virtual environment active:

| What | Pytest Command | Helper Script Command |
|---|---|---|
| Everything, in configured order | `pytest assignment_tests -v` | `python run_assignment_tests.py all` |
| One group (Smoke) | `pytest assignment_tests -m smoke` | `python run_assignment_tests.py smoke` |
| One group (Boundary / BVA) | `pytest assignment_tests -m boundary` | `python run_assignment_tests.py boundary` |
| One group (Data-driven / CSV) | `pytest assignment_tests -m data_driven` | `python run_assignment_tests.py data` |
| Suite 1 (`dateutil.parser`) | `pytest assignment_tests -m parser` | `python run_assignment_tests.py parser` |
| Suite 2 (`dateutil.relativedelta`)| `pytest assignment_tests -m relativedelta` | `python run_assignment_tests.py relativedelta` |
| Suite 3 (`dateutil.rrule`) | `pytest assignment_tests -m rrule` | `python run_assignment_tests.py rrule` |
| Sequential Groups run | — | `python run_assignment_tests.py groups` |
| In parallel (all CPU cores) | `pytest assignment_tests -n auto` | `python run_assignment_tests.py parallel` |
| Show execution order only | `pytest assignment_tests --collect-only -q` | `python run_assignment_tests.py order` |

---

## Test Architecture & Execution Order (Task 4)

### Groups and Suites
- **Groups (markers):** `smoke`, `boundary`, `data_driven`.
- **Suites (automatically tagged via file prefix):** `parser`, `relativedelta`, `rrule`.
- Markers are registered in `pytest.ini`; suites and ordering are dynamically assigned in `assignment_tests/conftest.py`.

### Execution Order
Tests execute in the following prioritized sequence:
1. **`smoke` group:** Fast initial sanity checks (`test_parse_iso8601_format`, `test_identity_offset`, `test_yearly_recurrence_rule`).
2. **`boundary` group:** Boundary Value Analysis test cases for day/month/year limits, overflow rolls, and count limits.
3. **`data_driven` group:** Tests loaded from external CSV files.
4. **All remaining tests:** General equivalence classes and special edge cases.

Inside each group, suites execute in order: `parser` -> `relativedelta` -> `rrule`.

### Parameterization & Data-Driven Tests (Task 3)
- `@pytest.mark.parametrize` is used extensively across `test_parser_ibrahim.py`, `test_relativedelta_ibrahim.py`, and `test_rrule_ahmad.py`.
- External CSV test data files live in `assignment_tests/data/`:
  - `parser_cases_ibrahim.csv`: 8 valid parsing vectors.
  - `relativedelta_cases_ibrahim.csv`: 8 date arithmetic vectors.
  - `parser_cases_ahmad.csv`: 5 error/malformed input vectors.
  - `rrule_cases_ahmad.csv`: 8 recurrence rule vectors.
- Adding a row to any CSV file immediately creates a new automated test case without changing code.

---

## Who Did What (Rubric Allocation Audit)

| Item | M. Ibrahim Asif (24F-3070) | M. Ahmad (24F-3040) |
|---|---|---|
| **Task 1: Setup & Instructions** | Initial project scaffolding, virtual environment, and dependency configuration | Setup evidence logs, `run_assignment_tests.py` CLI runner |
| **Task 1: Setup Video** | Walkthrough execution demonstration script | Demonstration recording coordination |
| **Task 2: Classes / Modules Covered** | `dateutil.parser` (standard formats, timestamps, dayfirst/yearfirst), `dateutil.relativedelta` (offsets, overflow, leap year, scaling) | `dateutil.parser` (edge cases, invalid inputs, None, fuzzy, timezone), `dateutil.rrule` (frequencies, weekdays, until, bymonthday, rruleset) |
| **Task 2: ECP/BVA Notes** | `notes/ecp_bva_ibrahim.md` | `notes/ecp_bva_ahmad.md` |
| **Task 2: Automated Tests** | `test_parser_ibrahim.py`, `test_relativedelta_ibrahim.py` | `test_parser_edge_ahmad.py`, `test_rrule_ahmad.py` |
| **Task 3: CSV Data Files** | `data/parser_cases_ibrahim.csv`, `data/relativedelta_cases_ibrahim.csv` | `data/parser_cases_ahmad.csv`, `data/rrule_cases_ahmad.csv` |
| **Task 3: Data-Driven Tests** | `test_parser_csv_ibrahim.py`, `test_relativedelta_csv_ibrahim.py` | `test_parser_csv_ahmad.py`, `test_rrule_csv_ahmad.py` |
| **Task 3: Excel Test Cases** | `assignment_docs/test_cases_ibrahim.xlsx` | `assignment_docs/test_cases_ahmad.xlsx`, `test_cases.xlsx` |
| **Task 4: Suites, Order & Config** | Marker definitions in `pytest.ini` and execution hook in `conftest.py` | `run_assignment_tests.py` CLI helper and parallel runner verification |
| **Summary / Excel Reports** | Test matrix design and initial ECP/BVA mapping | Final compilation: `assignment_docs/test_cases.xlsx` and setup logs |
