import sys
import os

# Ensure the parent directory (containing base.py) is in sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from base import APIBase

def test_filter_columns():
    data = [
        {"a": 1, "b": 2, "c": 3},
        {"a": 4, "b": 5, "c": 6},
    ]
    filtered = APIBase.filter_columns(data, ["a", "c"])
    assert filtered == [{"a": 1, "c": 3}, {"a": 4, "c": 6}]
    # If columns is None, returns original
    assert APIBase.filter_columns(data, None) == data

def test_filter_rows():
    data = [
        {"type": "A", "val": 1},
        {"type": "B", "val": 2},
        {"type": "A", "val": 3},
    ]
    # Single value in list
    filtered = APIBase.filter_rows(data, "type", ["A"])
    assert filtered == [
        {"type": "A", "val": 1},
        {"type": "A", "val": 3},
    ]
    # Multiple values
    filtered = APIBase.filter_rows(data, "type", ["A", "B"])
    assert filtered == data
    # None value returns original
    assert APIBase.filter_rows(data, "type", None) == data

def test_group_rows_pluralization():
    data = [
        {"category": "SENSOR", "model": "A"},
        {"category": "SENSOR", "model": "B"},
        {"category": "LOGGER", "model": "C"},
    ]
    grouped = APIBase.group_rows(data, "category")
    # SENSOR should be pluralized, LOGGER should not
    categories = [row["category"] for row in grouped]
    assert "SENSORS" in categories
    assert "LOGGER" in categories
    # Models should be joined
    for row in grouped:
        if row["category"] == "SENSORS":
            assert row["model"] == "A, B" or row["model"] == "B, A"

def test_group_rows_pluralization_y_and_s():
    data = [
        {"category": "BATTERY", "model": "A"},
        {"category": "BATTERY", "model": "B"},
        {"category": "BUS", "model": "C"},
        {"category": "BUS", "model": "D"},
    ]
    grouped = APIBase.group_rows(data, "category")
    categories = [row["category"] for row in grouped]
    assert "BATTERIES" in categories
    assert "BUSES" in categories

def test_transpose_data():
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]
    transposed = APIBase.transpose_data(data)
    # Should have two rows, one for each column
    assert any(row["column"] == "a" and row["row_0"] == 1 and row["row_1"] == 3 for row in transposed)
    assert any(row["column"] == "b" and row["row_0"] == 2 and row["row_1"] == 4 for row in transposed)

def test_rename_keys():
    data = [
        {"old": 1, "keep": 2},
        {"old": 3, "keep": 4},
    ]
    renamed = APIBase.rename_keys(data, {"old": "new"})
    assert renamed == [
        {"new": 1, "keep": 2},
        {"new": 3, "keep": 4},
    ]