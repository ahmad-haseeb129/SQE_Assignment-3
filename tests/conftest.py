# conftest.py — shared fixtures and CSV loading utility
import csv
import pytest
import os

def load_csv_data(filename):
    """Load test data from a CSV file in the test_data directory."""
    filepath = os.path.join(os.path.dirname(__file__), '..', 'test_data', filename)
    data = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
