from itertools import tee


def pairwise(iterable):
    """
    pairwise('ABCDEFG') --> AB BC CD DE EF FG

    Equivalent implementation from:
    docs.python.org/3/library/itertools.html#itertools.pairwise
    for Python < 3.10
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
