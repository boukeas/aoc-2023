from itertools import tee


def parse_file(lines):
    return [
        tuple(int(number) for number in line.strip().split())
        for line in lines
    ]


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def differences(sequence):
    """
    Given a `sequence` of numbers, return a tuple containing
    the differences between the pairs of numbers in the sequence.

    Example:
    >>> differences((10, 13, 16, 21, 30, 45))
    (3, 3, 5, 9, 15)
    """
    return tuple(
        current - previous
        for previous, current in pairwise(sequence)
    )


def all_differences(sequence):
    """
    Given a `sequence` of numbers, generate all tuples of higher-order
    differences, until all differences are 0.

    Example:
    >>> for diffs in all_differences((10, 13, 16, 21, 30, 45)):
    ...   print(diffs)
    (10, 13, 16, 21, 30, 45)
    (3, 3, 5, 9, 15)
    (0, 2, 4, 6)
    (2, 2, 2)
    (0, 0)
    """
    last_differences = sequence
    yield last_differences
    while not all(
        difference == 0
        for difference in last_differences
    ):
        last_differences = differences(last_differences)
        yield last_differences


def all_differences_range(sequence):
    """
    Given a `sequence` of numbers, calculate all tuples of higher-order
    differences, until all differences are 0 but generate only pairs
    containing the lowest and higher differences for each order
    (because these are the only ones necessary for extrapolating forward
    or in reverse).

    Example:
    >>> for diffs in all_differences_range((10, 13, 16, 21, 30, 45)):
    ...   print(diffs)
    ...
    (10, 45)
    (3, 15)
    (0, 6)
    (2, 2)
    (0, 0)
    """
    for last_differences in all_differences(sequence):
        yield last_differences[0], last_differences[-1]


def extrapolate(sequence):
    """
    Given a `sequence` of numbers, return a pair of values corresponding
    to the extrapolated preceeding and succeeding sequence values,
    based on the higher-order differences of the sequence.
    """
    ranges = tuple(all_differences_range(sequence))
    extrapolated_values = ranges[-2]
    # traverse the higher-order differences in reverse...
    for range in reversed(ranges[:-2]):
        # ... and update the pair of extrapolated values
        # on the reverse and forward end of the range
        extrapolated_values = (
            range[0] - extrapolated_values[0],
            extrapolated_values[1] + range[1]
        )
    return extrapolated_values
