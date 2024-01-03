from sys import argv

from tools13 import encode_rows, encode_columns, parse_file


def is_reflection(numbers, length, axis):
    """
    Given a set of `numbers` (that represent # positions) and
    the `length` of a line (the maximum possible number), return
    True if the numbers are symmetrical around the `axis` position
    and False otherwise.

    A pair of numbers is symmetric with respect to the `axis` position
    if they are equidistant from the axis and they are *both* either
    in the iterable of numbers or not.

    For example: the `numbers` for a line such as "#.##..##." are
    [0, 2, 3, 6, 7]. There is no reflection (no symmetry) around axis
    position 4, but there is around axis position 5.
    ```
    >>> is_reflection([0, 2, 3, 6, 7], 9, 4)
    False
    >>> is_reflection([0, 2, 3, 6, 7], 9, 5)
    True
    ```
    """
    left = axis - 1
    right = axis
    while left >= 0 and right < length:
        reflection = not ((left in numbers) ^ (right in numbers))
        if not reflection:
            return False
        left -= 1
        right += 1
    return True


def find_axis(lines, length):
    """
    Find and return a *common* axis of symmetry among the `lines`
    """
    # initialise candidate axes
    candidates = set(range(1, length))
    for line in lines:
        # iterate over a copy of the candidate set...
        for axis in set(candidates):
            # ... and remove the candidates that aren't axes of symmetry
            # for the current line
            if not is_reflection(line, length, axis):
                candidates.remove(axis)
                if len(candidates) == 0:
                    break
    try:
        return candidates.pop()
    except KeyError:
        return 0


if __name__ == '__main__':
    with open(argv[1]) as file:
        data = parse_file(file.readlines())

    result = 0
    for size, rows in data:
        nb_rows, nb_columns = size
        encoded_rows = encode_rows(size, rows)
        result_rows = find_axis(encoded_rows, length=nb_columns)
        encoded_columns = encode_columns(size, rows)
        result_columns = find_axis(encoded_columns, length=nb_rows)
        summary = result_rows + 100 * result_columns
        result += summary
    print(result)
