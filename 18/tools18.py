from enum import Enum
from itertools import tee
import re


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


line_re = re.compile(r'(?P<direction>[LRUD]) (?P<length>[0-9]+) \(#(?P<colour>[0-9a-f]{6})\)')


def parse_file(lines):
    return tuple(
        tuple(line_re.match(line.strip()).groups())
        for line in lines
    )


class Direction(Enum):
    Up = (-1, 0)
    Down = (1, 0)
    Right = (0, 1)
    Left = (0, -1)


def follow(instructions, start=(0, 0)):
    """
    Generate the set of coordinates visited by starting at `start`
    and following the `instructions`, which are tuples of the form:
    ```
    (direction: Direction, length: int)
    ```
    """
    coordinate = start
    for direction, length in instructions:
        yield coordinate
        offset_row, offset_column = direction.value
        coordinate = (
            coordinate[0] + offset_row * length,
            coordinate[1] + offset_column * length
        )
    yield coordinate


def area(coordinates):
    """
    Compute the area contained within the `coordinates`

    This is the number of points on the "boundary" (i.e. the shape formed
    by the coordinates) plus the number of internal points contained
    within the boundary
    """
    coordinates_iter = iter(coordinates)
    # first point
    x1, y1 = next(coordinates_iter)
    x_prev, y_prev = x1, y1
    nb_boundary_points = 0
    area_acc = 0
    # iterate over the rest of the points...
    while True:
        try:
            x, y = next(coordinates_iter)
        except StopIteration:
            break
        # accumulate the number of boundary points
        nb_boundary_points += abs(x - x_prev) + abs(y - y_prev)
        # while simultaneously computing the area
        # using the shoelace formula:
        # https://en.wikipedia.org/wiki/Shoelace_formula
        area_acc += x_prev * y - x * y_prev
        x_prev, y_prev = x, y

    # compute the number of internal points
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    nb_internal_points = int(abs(area_acc) / 2 - nb_boundary_points / 2 + 1)

    return nb_boundary_points + nb_internal_points
