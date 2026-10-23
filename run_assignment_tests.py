"""Run the assignment tests by suite or group, in order or in parallel (Task 4).

Usage (from the repository root, with the virtual environment active):

    python run_assignment_tests.py <name>

Names:
    all           every test in assignment_tests/, in the configured order
    order         only list the tests in the order they will run (nothing is executed)
    smoke         the smoke group
    boundary      the boundary group
    data          the data-driven group (tests that read an external CSV file)
    parser        the dateutil.parser suite
    relativedelta the dateutil.relativedelta suite
    rrule         the dateutil.rrule suite
    groups        smoke, then boundary, then data-driven, as three separate runs
    parallel      every test, spread over all CPU cores (pytest-xdist)

Anything after the name is passed on to pytest, for example:
    python run_assignment_tests.py parser -k iso8601
"""
import sys
import pytest

COMMANDS = {
    "all": [],
    "order": ["--collect-only", "-q"],
    "smoke": ["-m", "smoke"],
    "boundary": ["-m", "boundary"],
    "data": ["-m", "data_driven"],
    "parser": ["-m", "parser"],
    "relativedelta": ["-m", "relativedelta"],
    "rrule": ["-m", "rrule"],
    "parallel": ["-n", "auto"],
}
GROUP_SEQUENCE = ["smoke", "boundary", "data"]


def run(extra):
    return pytest.main(["assignment_tests", "-v", *extra])


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    name, extra = argv[0], argv[1:]
    if name == "groups":
        status = 0
        for group in GROUP_SEQUENCE:
            print("\n===== group: %s =====" % group)
            status = max(status, run(COMMANDS[group] + extra))
        return status
    if name not in COMMANDS:
        print("Unknown name %r. Run with --help to see the options." % name)
        return 2
    return run(COMMANDS[name] + extra)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
