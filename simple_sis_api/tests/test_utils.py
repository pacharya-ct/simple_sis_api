import sys
import os

# Ensure the parent directory (containing base.py) is in sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import utils

def test_filter_columns():
    data = [
        {"a": 1, "b": 2, "c": 3},
        {"a": 4, "b": 5, "c": 6},
    ]
    filtered = utils.filter_columns(data, ["a", "c"])
    assert filtered == [{"a": 1, "c": 3}, {"a": 4, "c": 6}]
    # If columns is None, returns original
    assert utils.filter_columns(data, None) == data

def test_filter_rows():
    data = [
        {"type": "A", "val": 1},
        {"type": "B", "val": 2},
        {"type": "A", "val": 3},
    ]
    # Single value in list
    filtered = utils.filter_rows(data, "type", ["A"])
    assert filtered == [
        {"type": "A", "val": 1},
        {"type": "A", "val": 3},
    ]
    # Multiple values
    filtered = utils.filter_rows(data, "type", ["A", "B"])
    assert filtered == data
    # None value returns original
    assert utils.filter_rows(data, "type", None) == data

def test_pluralize_noun():
    assert utils.pluralize_noun("sensor") == "sensors"
    assert utils.pluralize_noun("battery") == "batteries"
    assert utils.pluralize_noun("Logger") == "Loggers"
    assert utils.pluralize_noun("CITY") == "CITIES"
    assert utils.pluralize_noun("sensors") == "sensors"  # already plural

def test_group_rows_pluralization():
    data = [
        {"category": "SENSOR", "model": "A"},
        {"category": "SENSOR", "model": "B"},
        {"category": "LOGGER", "model": "C"},
    ]
    grouped = utils.group_rows(data, "category")
    # SENSOR should be pluralized, LOGGER should not
    categories = [row["category"] for row in grouped]
    assert "SENSORS" in categories
    assert "LOGGER" in categories
    # Models should be joined
    for row in grouped:
        if row["category"] == "SENSORS":
            assert row["model"] == "A, B" or row["model"] == "B, A"

def test_group_rows_pluralization_y():
    data = [
        {"category": "BATTERY", "model": "A"},
        {"category": "BATTERY", "model": "B"}
    ]
    grouped = utils.group_rows(data, "category")
    categories = [row["category"] for row in grouped]
    assert "BATTERIES" in categories

def test_group_rows_more_than_two_columns():
    data = [
        {"category": "SENSOR", "model": "A", "extra": 1},
        {"category": "SENSOR", "model": "B", "extra": 2},
    ]
    with pytest.raises(ValueError):
        utils.group_rows(data, "category")

def test_aggregate_column_single_value():
    data = [
        {"type": "A"},
        {"type": "A"}
    ]
    result = utils.aggregate_column(data, "type")
    assert result == [{"type": "A"}]

def test_aggregate_column_multiple_values():
    data = [
        {"type": "A"},
        {"type": "B"}
    ]
    result = utils.aggregate_column(data, "type")
    # Should pluralize column name
    assert result == [{"types": "A, B"}]

def test_aggregate_column_empty():
    data = []
    result = utils.aggregate_column(data, "type")
    assert result == []

def test_transpose_data():
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]
    transposed = utils.transpose_data(data)
    # Should have two rows, one for each column
    assert any(row["column"] == "a" and row["row_0"] == 1 and row["row_1"] == 3 for row in transposed)
    assert any(row["column"] == "b" and row["row_0"] == 2 and row["row_1"] == 4 for row in transposed)

def test_rename_columns():
    data = [
        {"old": 1, "keep": 2},
        {"old": 3, "keep": 4},
    ]
    renamed = utils.rename_columns(data, {"old": "new"})
    assert renamed == [
        {"new": 1, "keep": 2},
        {"new": 3, "keep": 4},
    ]