from itertools import combinations
from sys import argv
import numpy as np

from tools24 import parse_file


def coordinate(c1, d1, t):
    return c1 + d1 * t


def solve(line_1, line_2):
    """
    Given two lines c1 + d1*t and c2 + d2*t (where c1, d1, c2 and d2 are
    3D vectors) return the times t1 and t2 at which these lines intersect
    at the same x, y coordinates, along with the coordinates themselves.

    The (unknown) t1 and t2 are computed by solving a 2x2 system of linear
    equations:

    c1 + d1*t1 = c2 + d2*t2 ->
    d1x*t1 - d2x*t2 = c2x - c1x
    d1y*t1 - d2y*t2 = c2y - c1y
    """
    (c1x, c1y, _), (d1x, d1y, _) = line_1
    (c2x, c2y, _), (d2x, d2y, _) = line_2
    A = np.array([[d1x, -d2x], [d1y, -d2y]])
    b = np.array([c2x - c1x, c2y - c1y])
    t = np.linalg.solve(A, b)
    t1, t2 = t
    return t1, t2, coordinate(c1x, d1x, t1), coordinate(c1y, d1y, t1)


if __name__ == '__main__':
    with open(argv[1]) as file:
        hailstones = parse_file(file.readlines())

    nb_crossing = 0
    test_area = (int(argv[2]), int(argv[3]))
    # iterate over all pairs of hailstones
    for hailstone1, hailstone2 in combinations(hailstones, 2):
        try:
            # compute times and x, y coordinates of intersection
            t1, t2, x, y = solve(hailstone1, hailstone2)
        except np.linalg.LinAlgError:
            # no intersection: parallel lines
            pass
        else:
            if (
                t1 >= 0 and t2 >= 0 and
                test_area[0] <= x <= test_area[1] and
                test_area[0] <= y <= test_area[1]
            ):
                # intersection not in the past and
                # within the test area
                nb_crossing += 1
    print(nb_crossing)
