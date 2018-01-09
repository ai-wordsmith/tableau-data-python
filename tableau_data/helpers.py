"""Tableau Data Helpers

This module containers various helper functions that aim to make it easier for a
user to work with the TableauData library.
"""

from datetime import datetime

def convert_raw_tableau_data(tableau_columns, tableau_data):
    """Take raw column and table data returned from the Tableau Javascript API
    and convert to a list of dictionaries where keys represent the column name
    and values represent the column values.

    By default, this function will use the "value" property returned by the
    Tableau Javascript API. For columns where you would prefer to use the 
    "formattedValue" property, pass them as a list to the use_formatted_value
    parameter.

    Parameters
    ----------
    tableau_columns : :class:`dict`
        A dictionary object representing the column data provided by the Tableau
        Javascript API's getColumns() function.
    tableau_data : :class:`dict`
        A dictionary object representing the table data provided by the Tableau
        Javascript API's getData() function.

    Returns
    -------
    :class:`list`
        A list of dictionaries where each dictionary has keys representing the
        column name and values representing the column values.
    """
    converted = []
    for row in tableau_data:
        converted_row = {}
        for idx, val in enumerate(row):
            col = tableau_columns[idx]
            field_name = col['name']
            data_type = col['dataType']
            converted_row[field_name] = _converter(val, data_type)
        converted.append(converted_row)
    return converted

def _converter(value, data_type):
    """Private function that dictates how data elements are parsed based on the
    data type provided in the Tableau Javascript API's getColumns() method.
    """
    # Tableau returns "%null" (as a string) for any NULL vals
    if value == '%null%':
        return None
    # Default date formatting from the Tableau JS API is YYYY-MM-DD
    if data_type == 'date':
        return datetime.strptime(value, '%Y-%m-%d')
    elif data_type == 'datetime':
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    elif data_type == 'float':
        return float(value)
    elif data_type == 'integer':
        return int(value)
    elif data_type == 'boolean':
        return True if 'value' == 'true' else False
    # Default is to return a string
    return value