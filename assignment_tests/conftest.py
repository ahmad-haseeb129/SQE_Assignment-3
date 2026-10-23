"""Test suites, automatic tagging, and execution order for Assignment 3 (Task 4).

Features:
1. Suite markers: Tests automatically receive a suite marker ('parser', 'relativedelta', or 'rrule')
   derived from the file name, enabling suite-based execution like `pytest -m parser`.
2. Execution ordering: Tests are assigned an execution priority hook:
   smoke -> boundary -> data_driven -> everything else
   Inside each group, suites run: parser -> relativedelta -> rrule.
3. CSV Data Loader: Reusable utility to parse CSV files from assignment_tests/data/.
"""
import os
import csv
import pytest

GROUP_ORDER = ["smoke", "boundary", "data_driven"]   # then everything else
SUITE_ORDER = ["parser", "relativedelta", "rrule"]
SUITE_FILE_PREFIX = {
    "parser": "test_parser",
    "relativedelta": "test_relativedelta",
    "rrule": "test_rrule",
}


def _suite_of(item):
    for suite, prefix in SUITE_FILE_PREFIX.items():
        if item.path.name.startswith(prefix):
            return suite
    return None


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        suite = _suite_of(item)
        if suite:
            item.add_marker(getattr(pytest.mark, suite))

        group_rank = len(GROUP_ORDER)          # "everything else" runs last
        for rank, group in enumerate(GROUP_ORDER):
            if item.get_closest_marker(group):
                group_rank = rank
                break
        suite_rank = SUITE_ORDER.index(suite) if suite else len(SUITE_ORDER)

        # pytest-order runs lower numbers first: group first, then suite.
        item.add_marker(pytest.mark.order(group_rank * 10 + suite_rank + 1))


def load_csv_data(filename):
    """Load test data from a CSV file in assignment_tests/data/ directory."""
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    data = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
