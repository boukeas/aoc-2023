from enum import Enum


def parse_file(lines):
    result = []
    for row, line in enumerate(lines):
        try:
            column = line.index('S')
        except ValueError:
            result.append(line.strip())
        else:
            start = (row, column)
            result.append(line.strip().replace('S', '.'))
    return (len(result), len(result[0])), start, result


def within_bounds(position, size):
    """
    Return True if the pair of coordinates in `position` are non-negative
    and within the bounds specified by `size`.
    """
    return all(
        position_part >= 0 and
        position_part < size_part
        for position_part, size_part in zip(position, size)
    )


class Direction(Enum):
    North = (-1, 0)
    South = (1, 0)
    East = (0, 1)
    West = (0, -1)


def get_next_position(position, direction, distance=1):
    """
    Return the coordinates that are `distance` away from the coordinates
    in `position`, in a specific `direction`.
    """
    return tuple(
        position_part + direction_part * distance
        for position_part, direction_part in zip(position, direction.value)
    )


def get_contents(position, matrix):
    return matrix[position[0]][position[1]]
