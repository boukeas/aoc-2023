from sys import argv

from tools13 import encode_rows, encode_columns, parse_file


def reflection_discrepancies(numbers, length, axis):
    """
    Given a set of `numbers` (that represent # positions) and
    the `length` of a line (the maximum possible number), return
    the pairs of values that are *not* symmetric with respect to
    the `axis` position, i.e. the discrepancies.

    A pair of numbers is symmetric with respect to the `axis` position
    if they are equidistant from the axis and they are *both* either
    in the iterable of numbers or not.
    """
    discrepancies = set()
    distance_from_axis = 0
    while True:
        left = axis - distance_from_axis - 1
        right = axis + distance_from_axis
        if left < 0 or right == length:
            return discrepancies
        reflection = not ((left in numbers) ^ (right in numbers))
        if not reflection:
            discrepancies.add((left, right))
        distance_from_axis += 1


def find_single_discrepancy_axis(lines, length):
    """
    Iterate over encoded `lines` (where the maximum value in each line may be
    `length`) and return the set of single-discrepancy axes.

    A single-discrepancy axis is an axis across which all `lines` *except one*
    are symmetrical. The non-symmetrical line contains only a single
    discrepancy with respect to the axis. In other words, fixing that single
    discrepancy would make all lines symmetrical with respect to the axis.
    """
    # this set contains the axes that have <= 1 discrepancies
    # across the lines that have been examined thus far
    candidates = set(range(1, length))
    # this dict contains the axes that have exactly 1 discrepancy
    # across the lines that have been examined thus far
    single_discrepancy_candidates = {}
    for index, line in enumerate(lines):
        for axis in set(candidates):
            discrepancies = reflection_discrepancies(line, length, axis)
            nb_discrepancies = len(discrepancies)
            if nb_discrepancies == 0:
                pass
            elif len(discrepancies) == 1 and axis not in single_discrepancy_candidates:
                left, right = discrepancies.pop()
                # also take note which indices need to be flipped
                # to make the line symmetrical
                single_discrepancy_candidates[axis] = (left, right)
            else:
                # remove axis from candidates:
                # there is either a line with >1 discrepancies
                # or more than one lines with 1 discrepancy
                candidates.remove(axis)
                try:
                    del single_discrepancy_candidates[axis]
                except KeyError:
                    pass
    return single_discrepancy_candidates


if __name__ == '__main__':
    with open(argv[1]) as file:
        data = parse_file(file.readlines())

    result = 0
    for size, rows in data:
        nb_rows, nb_columns = size
        # encode per row and check for "smudges"
        # (i.e. is there an axis of symmetry arising after a single flip?)
        encoded_rows = encode_rows(size, rows)
        row_smudge_candidates = find_single_discrepancy_axis(encoded_rows, length=nb_columns)
        try:
            result_rows, _ = row_smudge_candidates.popitem()
        except KeyError:
            result_rows = 0
        # encode per column and check for smudges
        encoded_columns = encode_columns(size, rows)
        column_smudge_candidates = find_single_discrepancy_axis(encoded_columns, length=nb_rows)
        try:
            result_columns, _ = column_smudge_candidates.popitem()
        except KeyError:
            result_columns = 0

        summary = result_rows + 100 * result_columns
        result += summary
    print(result)
