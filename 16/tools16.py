from collections import defaultdict
from enum import Enum


def parse_file(lines):
    result = [
        [char for char in line.strip()]
        for line in lines
    ]
    return (len(result), len(result[0])), result


def next_position(position, direction):
    return tuple(
        position_part + direction_part
        for position_part, direction_part in zip(position, direction.value)
    )


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


# capture the behaviour of the light beam as it encounters
# objects coming from different directions
behaviour = {
    Direction.East: {
        '\\': Direction.South,
        '/': Direction.North,
        '-': Direction.East,
        '|': (Direction.North, Direction.South)
    },
    Direction.West: {
        '\\': Direction.North,
        '/': Direction.South,
        '-': Direction.West,
        '|': (Direction.North, Direction.South)
    },
    Direction.North: {
        '\\': Direction.West,
        '/': Direction.East,
        '-': (Direction.West, Direction.East),
        '|': Direction.North
    },
    Direction.South: {
        '\\': Direction.East,
        '/': Direction.West,
        '-': (Direction.West, Direction.East),
        '|': Direction.South
    },
}


def zap(position, direction, mirrors, size, energised_dict):
    """
    Follow the light beam as it starts from `position`, moving towards
    `direction`. While doing so, populate the `energised_dict`, which
    maps each position to a set of directions in which the light beam
    has crossed that position.

    The final length of the `energised_dict` is the number of "energised"
    positions. However, this dict also serves to detect cycles: following
    the beam can stop whenever a position has already been crossed by
    the light beam in a certain direction.
    """
    while True:
        position = next_position(position, direction)
        if not within_bounds(position, size):
            # out of bounds: stop
            return
        if direction in energised_dict[position]:
            # position has been visited before, from the same direction: stop
            return
        # record the passing of the beam from this position, in this direction
        energised_dict[position].add(direction)
        mirror = mirrors[position[0]][position[1]]
        direction = behaviour[direction].get(mirror, direction)
        if isinstance(direction, tuple):
            # the beam has been split: make two recursive calls in order
            # to follow the beam in both directions
            zap(position, direction[0], mirrors, size, energised_dict)
            zap(position, direction[1], mirrors, size, energised_dict)
            return


def nb_energised(position, direction, mirrors, size):
    """
    Return the number of energised positions after starting the beam
    from `position` towards `direction`.

    The `zap` function is recursive and the `energised_dict` is how
    all the separate calls exchange information, but also how the function
    returns its results.
    """
    energised = defaultdict(set)
    zap(position, direction, mirrors, size, energised_dict=energised)
    return len(energised)
