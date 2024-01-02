from collections import defaultdict


def distance(coordinate1, coordinate2):
    return (
        abs(coordinate1[0] - coordinate2[0]) +
        abs(coordinate1[1] - coordinate2[1])
    )


def expand(axis_dict, factor=2):
    """
    Given an `axis_dict`, which is essentially a representation of a sparse
    sparse 2D matrix (keys are coordinates on one axis and values are the
    sets of coordinates on the other axis), return a new axis dict where
    the gaps between the key coordinates have been expanded by `factor`
    """
    axis_dict = sorted(axis_dict.items())
    axis_dict_iterator = iter(axis_dict)
    result_dict = {}
    # maintain a running count of how much further away each
    # coordinate should be offset
    offset = 0
    previous_index = -1
    while True:
        try:
            index, positions = next(axis_dict_iterator)
        except StopIteration:
            break
        # compute the gap between consecutive coordinates
        gap = index - previous_index - 1
        # increase the offset, if necessary
        if gap > 0:
            offset += gap * factor - 1
        result_dict[index + offset] = positions
        previous_index = index
    return result_dict


def parse_file(lines, factor=2):
    # map every row to the set of columns where '#'s appear
    row_dict = defaultdict(set)
    for row, line in enumerate(lines):
        start = 0
        while True:
            try:
                column = line.index('#', start)
            except ValueError:
                break
            row_dict[row].add(column)
            start = column + 1
    # expand the empty columns
    row_dict = expand(row_dict, factor=factor)
    # map every column to the set of rows where '#'s appear
    # (using the `row_dict` mapping)
    column_dict = defaultdict(set)
    for row, columns in row_dict.items():
        for column in columns:
            column_dict[column].add(row)
    # expand the empty rows
    column_dict = expand(column_dict, factor=factor)
    # yield all row, column pairs where '#'s appear
    for column, rows in column_dict.items():
        for row in rows:
            yield (row, column)
