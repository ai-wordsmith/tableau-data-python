# Tableau Data Python Library
This library is meant to help convert Tableau Data to a Wordsmith-ready format.
Generally, this library seeks to provide a pseudo-SQL type of interface that
enables a user to easily perform aggregating functions on a tabular dataset.

This library is designed to work in unison with the TableauHelper Javascript
library available on [GitHub](https://github.com/ai-wordsmith/tableau-js-helper).

## Requirements
This library was built and tested using Python 3.5. It requires no external
dependencies and should work with any version of Python 3 or higher.

## Installation
This library is meant for the exclusive use of Automated Insights employees and
partners. As such, it is not available via PyPI and may not be made publicly
available without the express consent of Automated Insights.

In order to install, use pip to perform an installation from GitHub:
`pip install git+ssh://github.com/ai-wordsmith/tableau-data-python.git`

## Helper Functions
Below are some helpful hints to get started using this library.

### convert_raw_tableau_data()
The TableauData object expects to receive a list of dictionaries where keys
represent column names and values represent column values. Natively, Tableau
returns data in two separate forms: one for column data and one for table data.

Using the TableauHelper JS libraries `getSummaryData()` or `getFullData()` methods, the returned structure will look something like this:

```javascript
{
    columns: [
        {
            name: "Product Type",
            dataType: "string",
            isReferenced: true,
            index: 0
            
        },
        {
            name: "Price",
            dataType: "float",
            isReferenced: true,
            index: 1
        }
    ],
    data: [
        ["Foo", "10"],
        ["Bar", "5.5"]
}

```
This library includes a helper function, `convert_raw_tableau_data()` that takes the result of a data call using the Tableau Helper JS lib and converts it to a usable format. If the above example was stored in a variable named `tableau_data`, you could convert it as follows:

```python
tableau_data_formatted = convert_raw_tableau_data(tableau_data['columns'], tableau_data['data'])
```

The resultant dataset would look like this:

```python
[
    {
        "Product Type": "Foo",
        "Price": 10.0
    },
    {
        "Product Type" "Bar",
        "Price": 5.5
    }
]
```

This list of dictionaries can be passed to instantiate the TableauData class.

## TableauData Documentation

### Methods

| Name | Return Type | Description |
|------|-------------|-------------|
| by(column: String) | Iterable<TableauData[]> | Returns an iterable where each iteration yields a TableauData object containing rows segmented by values in the passed `column` argument. This method is similar to the GROUP BY clause in SQL. |
| where(condition: Function) | TableauData | Returns a TableauData object containing rows where the passed `condition` function evaluates to `True`. |
| sort(by: List, *reverse=False*: Boolean) | Returns a TableauData object sorted by the column(s) specified in the `by` argument. Passing `reverse=True` (optional) will sort the result in descending order. |
| distinct(column) | List | Returns a list of unique values for the specified `column`. |
| rows(*column*: String) | Iterable<Dict[]> | Returns an iterable where each iteration yields a row from the TableauData dataset. |

## Examples

For the following examples, we'll assume that we are starting with the following dataset:

```python
data = [
    dict(
        type="widget",
        color="blue"
    ),
    dict(
        type="widget",
        color="red"
    ),
    dict(
        type="foo",
        color="blue"
    ),
    dict(
        type="foo",
        color="red"
    ),
    dict(
        type="bar",
        color="green"
    )
]
```

### Using `by` to count products by type

```python
for product_type in data.by('type'):
    print(len(product_type))
```

### Using `where` to find green or red products

```python
print(data.where(lambda d: d['color'] in ['red', 'green']))
```

### Sorting by product type

```python
print(data.sort(['type']))
```

### Get all colors with `distinct`

```python
print(data.distinct('color'))
```

### Get all rows from the dataset

```python
for row in data.rows():
    print(row)
```

### Chaining functions

In many cases, you'll need to chain functions in order to aggregate a tabular dataset into a singular value that can then be passed to Wordsmith. Methods that return a `TableauData` object are inherently chainable. For example, if we wanted to count product types where red is a color option we could do the following:

```python
print(len(data.where(lambda d: d['color'] == 'red').by('type')))
```

### Using List operations on a `TableauData` object

The TableauData object functions like a Python list giving you access to access to most common list functionality like slicing and iteration. Using this functionality, you could sort a list and take the first element to find the lowest value or the last element to find the highest value. Similarly, you don't need to use the `rows()` method to iterate over a `TableauData` object. 