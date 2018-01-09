"""TableauData

This module provides generic functionality for working with Tableau Data in Python 3. The
goal of this module is to provide abstracted SQL-like functionality that can be used to
group, aggregate, and otherwise manipulate tabular data to pull singular values that can
then be passed to Wordsmith.

The TableauData object expects a list of dictionaries as an initialization argument and
the object itself acts as a list and supports iteration, slicing, etc.

Example
-------
Creates a new Tableau Data object. All subsequent examples use this dataset.
>>> data = [
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
>>> tabdata = TableauData(data)
"""

class TableauData(object):
    """Data object representing tabular data sourced from Tableau

    Parameters
    ----------
    data : :class:`list` of :obj:`dict
        List of dictionaries where dictionary keys are column names and values are column 
        values.
    """

    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def by(self, column):
        """Return data objects based on unique values in a column. This is similar to SQL's
        GROUP BY clause.

        Parameters
        ----------
        by : str
            The column name, as a string, that should be used to segment the dataset.

        Yields
        ------
        :class:`TableauData`
            A TableauData object representing all rows matching a single value in the "by"
            column.

        Example
        -------
        Print the number of rows represented by each color.
        >>> for td in tabdata.by('color'):
        ...     print(len(td))
        """
        values = list(set([row[column] for row in self.data]))
        for value in self.distinct(column):
            yield TableauData([row for row in self.data if row[column] == value])
    
    def where(self, condition):
        """Return only those rows where the provided condition function is true.

        Parameters
        ----------
        condition : :function:

        Returns
        -------
        :class:`TableauData`
            A TableauData object containing all rows that satisfy the provided condition.

        Example
        -------
        Get all rows where the color is red or green
        >>> red_or_green = tabdata.where(lambda td: td['color'] in ['red', 'green'])
        """
        return TableauData([row for row in self.data if condition(row)])

    def sort(self, by, **kwargs):
        """Sort the dataset by a column or list of columns.

        Note
        ----
        The "by" parameter can be a list or single value. Any single value passed will be
        converted to a list automatically.

        Parameters
        ----------
        by : :class:`list`
            Column names to sort by. The sort will occur based on the order passed so,
            passing ['a', 'b'] will mean column "a" is sorted, then column "b".
        **kwargs
            The only kwarg supported is "reverse" which indicates that the sort order
            should be reversed (default order is ascending). Anything other than
            "reverse" will be ignored.

        Returns
        -------
        :class:`TableauData`
            A TableauData object sorted based upon the provided column(s)

        Example
        -------
        >>> sorted_by_type = tabdata.sort(['type'])
        """
        reverse = False if 'reverse' not in kwargs.keys() else kwargs['reverse']
        if type(by) != list:
            by = [by]
        return TableauData(sorted([row for row in self.data], key=lambda k: [k[column] for column in by], reverse=reverse))

    def distinct(self, column):
        """Return distinct values from a specified column.

        Parameters
        ----------
        column : str
            The name of the column containing the values.

        Returns
        -------
        :class:`list`
            A list of distinct values from the specified column.

        Example
        -------
        >>> tabdata.distinct('color')
        """
        return list(set([row[column] for row in self.data]))

    def rows(self, column = None):
        """Return an iterable with each iteration representing a single row of data.

        Parameters
        ----------
        column : str, optional
            If provided, the iterator will contain only values from the specified 
            column.

        Yields
        ------
        :class:`dict`
            A dictionary where keys represent column names and values represent column 
            values.

        Example
        -------
        Print rows from dataset to the console.
        >>> for row in tabdata.rows():
        ...     print(row)
        """
        for row in self.data:
            if column is None:
                yield row
            else:
                yield {
                    column: row[column]
                }

