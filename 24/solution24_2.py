from itertools import combinations
from sys import argv
import numpy as np

from tools24 import parse_file


def skew_symmetric(vector):
    """
    Return the skew-symmetric matrix of a 3D vector

    To be used for computing the cross-product of the vector with
    another vector:
    en.wikipedia.org/wiki/Skew-symmetric_matrix#Cross_product
    """
    return np.array(
        [
            [0, -vector[2], vector[1]],
            [vector[2], 0, -vector[0]],
            [-vector[1], vector[0], 0]
        ]
    )


if __name__ == '__main__':
    with open(argv[1]) as file:
        hailstones = tuple(parse_file(file.readlines()))

    """
    Since the rock cr + dr*t intersects with hailstone i ci + di*t:

    cr + dr*t = ci + di*t ->
    cr - ci = (di - dr)*t ->
    cr - ci is parallel to di - dr ->
    (cr - ci) x (di - dr) = 0
    (di x cr) + (ci x dr) - (cr x dr) = (ci x di)   [1]

    The same reasoning applies to the intersection of the rock with hailstone j:
    (dj x cr) + (cj x dr) - (cr x dr) = (cj x dj)   [2]

    Combining [1] and [2]:

    (di - dj) x cr + (ci - cj) x dr = (di x ci) - (dj x cj)
    [di - dj]_x @ cr + [ci - cj]_x @ dr = (di x ci) - (dj x cj)

    This is a system of 3 equations with 6 unknowns, i.e. cr and dr.
    So we need another such system (generated using a third hailstone
    ck + dk*t) to solve for cr and dr
    """

    # select 3 hailstones
    triplet_iterator = combinations(hailstones, 3)
    # note: this may need to be repeated, if the specific triplet
    # happens to yield equations that are not linearly independent
    (c1, d1), (c2, d2), (c3, d3) = next(triplet_iterator)

    b_top = np.cross(d1, c1) - np.cross(d2, c2)
    b_bottom = np.cross(d1, c1) - np.cross(d3, c3)
    b = np.concatenate((b_top, b_bottom), axis=0)

    A_top = np.concatenate((skew_symmetric(d1-d2), skew_symmetric(c1-c2)), axis=1)
    A_bottom = np.concatenate((skew_symmetric(d1-d3), skew_symmetric(c1-c3)), axis=1)
    A = np.concatenate((A_top, A_bottom), axis=0)

    solution = np.linalg.solve(A, b)
    print(round(sum(solution[:3])))
