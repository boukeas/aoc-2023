def parse_file(lines):
    nb_rows = 0
    batched_lines = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            nb_columns = len(batched_lines[0])
            yield (nb_rows, nb_columns), batched_lines
            nb_rows = 0
            batched_lines = []
        else:
            batched_lines.append(line)
            nb_rows += 1
    nb_columns = len(batched_lines[0])
    yield (nb_rows, nb_columns), batched_lines


def encode_positions(line):
    """
    Generate the indices in the `line` where a '#' character appears
    """
    yield from (
        index
        for index, symbol in enumerate(line)
        if symbol == '#'
    )


def encode_rows(size, rows):
    """
    Given an iterable of rows, return a corresponding iterable that,
    for each row, contains the set of columns where a `#` character appears.
    """
    return [
        set(encode_positions(row))
        for row in rows
    ]


def encode_columns(size, rows):
    """
    Given an iterable of rows, return a iterable that, for each *column*,
    contains the set of rows where a `#` character appears. This is
    essentially a transposed version of `encode_rows`.
    """
    nb_rows, nb_columns = size
    columns = [
        "".join(
            rows[row][column]
            for row in range(nb_rows)
        )
        for column in range(nb_columns)
    ]
    return [
        set(encode_positions(column))
        for column in columns
    ]
