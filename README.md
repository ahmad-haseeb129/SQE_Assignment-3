# SQE Assignment 3 — Unit Test Automation for `dateutil`

## Team Members
| Name               | Roll No   | GitHub                                              |
|--------------------|-----------|------------------------------------------------------|
| M. Ibrahim Asif    | 24F-3070  | [asifibrahim256](https://github.com/asifibrahim256)  |
| M. Ahmad           | 24F-3040  | [ahmad-haseeb129](https://github.com/ahmad-haseeb129)|

## Project Under Test
- **Project:** [python-dateutil](https://github.com/dateutil/dateutil)
- **Language:** Python
- **Description:** Powerful extensions to the standard `datetime` module — parsing, relative deltas, recurrence rules, and timezone handling.

## Modules Selected for Testing
| # | Module                  | Description                                  |
|---|-------------------------|----------------------------------------------|
| 1 | `dateutil.parser`       | Parsing human-readable date/time strings     |
| 2 | `dateutil.relativedelta`| Date arithmetic with relative deltas         |
| 3 | `dateutil.rrule`        | Recurrence rule generation (RFC 2445)        |

## Task Distribution
| Member | Responsibilities / Test Scope |
|---|---|
| **M. Ibrahim Asif (24F-3070)** | • Project environment setup, dependency configuration, and initial repo scaffolding.<br>• ECP & BVA analysis for `dateutil.parser` (standard date formats, boundary dates, dayfirst/yearfirst) and test implementation.<br>• ECP & BVA analysis for `dateutil.relativedelta` (basic offsets, month-end overflow, leap year handling, arithmetic scaling) and test implementation.<br>• Core recurrence tests for `dateutil.rrule` (YEARLY, MONTHLY, WEEKLY, DAILY frequencies, count boundaries, interval progression, between/after lookups).<br>• CSV-driven test implementation for parser and relativedelta. |
| **M. Ahmad (24F-3040)** | • ECP & BVA analysis for `dateutil.parser` edge cases (empty strings, non-date text, None inputs, fuzzy parsing, time boundaries, timezone offsets).<br>• ECP & BVA analysis for `dateutil.relativedelta` (zero offset, large offset, absolute date parameters, inter-date deltas, year boundaries, negative offsets, type validation).<br>• Advanced recurrence tests for `dateutil.rrule` (HOURLY frequency, weekday filtering, until boundaries, monthday filtering, negative indexing, rruleset exclusions).<br>• CSV test datasets creation and CSV-driven test validation for error handling and recurrence rules.<br>• Excel test case documentation (`docs/test_cases.xlsx`) and execution reporting. |

## Setup Demonstration Video
- **Demonstration Video Link:** [Video / Recording link placeholder - upload to repository or Google Drive]
- The video demonstrates cloning the repository, virtual environment creation, dependencies installation, and test execution (`pytest`).

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/ahmad-haseeb129/SQE_Assignment-3.git
cd SQE_Assignment-3

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install dateutil in development mode
pip install -e ./dateutil
```

### Verify Installation
```bash
python -c "import dateutil; print(dateutil.__version__)"
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests by Module (Suite)
```bash
# Parser tests only
pytest -m parser

# Relativedelta tests only
pytest -m relativedelta

# Rrule tests only
pytest -m rrule
```

### Run Tests by Category
```bash
# ECP tests
pytest -m ecp

# BVA tests
pytest -m bva

# CSV-driven tests
pytest -m csv_driven
```

### Run Tests in Parallel
```bash
# Use all available CPU cores
pytest -n auto

# Use specific number of workers
pytest -n 4
```

### Run Specific Test Groups in Order
```bash
# Smoke tests first, then full suite
pytest -m "smoke" && pytest -m "not smoke"
```

## Project Structure
```
SQE_Assignment-3/
├── dateutil/               # Cloned dateutil source (project under test)
├── tests/
│   ├── conftest.py         # Shared fixtures and CSV data loader
│   ├── test_csv_driven.py  # Data-driven test runner from CSV files
│   ├── test_parser.py      # Unit tests for dateutil.parser
│   ├── test_relativedelta.py # Unit tests for dateutil.relativedelta
│   └── test_rrule.py       # Unit tests for dateutil.rrule
├── test_data/
│   ├── parser_test_data.csv       # CSV test data for parser
│   ├── relativedelta_test_data.csv # CSV test data for relativedelta
│   └── rrule_test_data.csv        # CSV test data for rrule
├── notes/
│   ├── ecp_bva_parser.md          # ECP/BVA analysis for parser
│   ├── ecp_bva_relativedelta.md   # ECP/BVA analysis for relativedelta
│   └── ecp_bva_rrule.md           # ECP/BVA analysis for rrule
├── docs/
│   └── test_cases.xlsx            # Excel sheet with all test cases
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .gitignore
```

## Test Design Techniques Used
- **ECP (Equivalence Class Partitioning):** Inputs divided into valid/invalid classes
- **BVA (Boundary Value Analysis):** Testing at boundary values
- **Data-Driven Testing:** Test data loaded from CSV files
- **Parameterization:** `pytest.mark.parametrize` for multiple inputs
- **Parallel Execution:** `pytest-xdist` for concurrent test runs
- **Test Ordering:** `pytest-ordering` for controlled execution sequence
