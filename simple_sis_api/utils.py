'''
utils.py
Author: Prabha Acharya
Create date: 20240402
Version: 0.1
'''
import datetime as dt

def parsedate(val):
    if not val:
        return val
    return dt.datetime.fromisoformat(val)

FUTURE_OFF_DATE = dt.datetime(3000, 1, 1, tzinfo=dt.UTC)

# define the non string attribute types 
# key is attribute name and the value is the function used to cast it to the expected datatype
ATTR_DATATYPE_MAPPING = dict(latitude=float,
    longitude=float, 
    elevation=float,
    xcoord=float,
    ycoord=float,
    zcoord=float,
    ondate=parsedate,
    offdate=parsedate,
)

def filter_columns(data, columns):
    """
    Given a list of dictionaries (data), return a new list of dictionaries
    containing only the specified columns.
    If columns is empty or None, return the original data.
    """
    if not columns:
        return data

    filtered_data = []
    for entry in data:
        filtered_entry = {k: v for k, v in entry.items() if k in columns}
        filtered_data.append(filtered_entry)

    return filtered_data

def filter_rows(data, column, values):
    """
    Given a list of dictionaries (data), return a new list of dictionaries
    where the value of a specified column matches any of the given values.
    If value is None, return the original data.
    """
    if not values:
        return data

    filtered_data = [entry for entry in data if entry.get(column) in values]
    return filtered_data

def group_rows(data, column):  
    """
    Given a list of dictionaries (data), return a new list of dictionaries
    where rows with the same value in the specified column are grouped together.
    The values of other columns are joined with commas.
    Only works if there are exactly two columns in the data.

    Example usage:
    To group by 'category' column:
    data = [{"category": "SENSOR", "model": "A"},
            {"category": "SENSOR", "model": "B"},
            {"category": "LOGGER", "model": "C"}]
    grouped = group_rows(data, "category")
    Result:
    [{"category": "SENSOR", "model": "A, B"},
        {"category": "LOGGER", "model": "C"}]
    """
    if not data or len(data[0].keys()) != 2:
        raise ValueError("Data must contain exactly two columns to group rows.")

    # Create a dictionary of the form {column_value: {column: column_value, other_column: joined_values}}
    grouped_data = {}
    for entry in data:
        if entry[column] not in grouped_data:
            grouped_data[entry[column]] = entry.copy()
        else:
            for k, v in entry.items():
                if k != column:
                    if v not in grouped_data[entry[column]][k].split(','):
                        grouped_data[entry[column]][k] += f", {v}"
    
    # Reformat the grouped data back into a list of dictionaries
    grouped_data = list(grouped_data.values())
    return grouped_data

def aggregate_column(data, column, sep=", "):
    """
    Given a list of dictionaries (data), aggregate the distinct values of a specified column
    into a single string, separated by the given separator.
    Returns a list with a single dictionary containing the aggregated value.
    If data is empty, returns an empty list.
    If more than one unique value is aggregated, the column name is pluralized using the inflect library via the pluralize_noun function.
    """
    if not data:
        return []

    # Collect distinct values, preserving order
    distinct_values = list(dict.fromkeys(str(entry[column]) for entry in data if column in entry))
    aggregated_str = sep.join(distinct_values)

    return [{column: aggregated_str}]

def transpose_data(data):
    """
    Given a list of dictionaries (data), return a new list of dictionaries
    where rows are converted to columns and columns to rows.
    """
    if not data:
        return []

    # Get the column names from the first row
    columns = data[0].keys()
    transposed = []

    # Create a new dictionary for each column
    for col in columns:
        new_row = {"column": col}
        new_row.update({f"row_{i}": row[col] for i, row in enumerate(data)})
        transposed.append(new_row)

    return transposed

def rename_columns(data, column_map):
    """
    Given a list of dictionaries (data), rename columns based on the provided column_map.
    column_map is a dictionary where keys are old names and values are new names.
    """
    renamed_data = []
    for entry in data:
        renamed_entry = {column_map.get(k, k): v for k, v in entry.items()}
        renamed_data.append(renamed_entry)

    return renamed_data