from collections import defaultdict
from enum import Enum


def parse_file(lines):
    result = [
        [int(char) for char in line.strip()]
        for line in lines
    ]
    return (len(result), len(result[0])), result


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


# map the direction of motion to the direction you need to turn
turn_direction = {
    Direction.East: (Direction.South, Direction.North),
    Direction.West: (Direction.South, Direction.North),
    Direction.South: (Direction.East, Direction.West),
    Direction.North: (Direction.East, Direction.West)
}


def get_next_position(position, direction, distance=1):
    """
    Return the coordinates that are `distance` away from the coordinates
    in `position`, in a specific `direction`.
    """
    return tuple(
        position_part + direction_part * distance
        for position_part, direction_part in zip(position, direction.value)
    )


def search(matrix, size, next_positions_generator):
    """
    Assuming the start of the search is at (0, 0) and the target is at the
    bottom right of `matrix` (which is of a given `size`), perform a
    breadth-first branch-and-bound search to generate the (descending) cost
    of paths from the start to the end, without any circles.

    The rules of motion are captured by the `next_positions_generator`,
    a function that accepts the current position and direction in the
    matrix and generates valid tuples of the form:
    ```
    (next_position, next_direction, move_cost, distance)
    ```

    It is very important to note that the "moves" implemented by the
    `next_positions_generator` function are walk-and-turn moves,
    i.e. the `next_position` will be `distance` steps away from
    the original position in a certain direction and `next_direction`
    will represent a 90 degree turn away from that direction.
    """
    target = (size[0] - 1, size[1] - 1)
    # map (position, direction) nodes at a specific level to the
    # minimum cost of reaching that node
    nodes_per_level = defaultdict(dict)
    nodes_per_level[0] = {
        ((0, 0), Direction.South): 0,
        ((0, 0), Direction.East): 0
    }
    current_level = 0
    # the upper bound: traverse the entire matrix at a cost of 9 per step
    bound = size[0] * size[1] * 9
    while len(nodes_per_level) > 0:
        # monitor progress
        print(f"\r{current_level=} {len(nodes_per_level[current_level])}", end="")
        # iterate over all the nodes in this level
        for (position, direction), cost in nodes_per_level[current_level].items():
            if cost >= bound:
                # prune if cost exceeds upper bound
                continue
            if position == target:
                # reached the target:
                # yield the path cost and update bound
                print(f"\nsolution {cost=}")
                yield cost
                bound = cost
                continue
            # expand current node to generate its neighbours
            for next_position, next_direction, move_cost, distance in next_positions_generator(position, direction, matrix, size):
                next_level = current_level + distance
                next_cost = cost + move_cost
                if next_cost >= bound:
                    # prune if cost exceeds upper bound
                    continue
                next_node = (next_position, next_direction)
                # update the stored cost
                try:
                    existing_cost = nodes_per_level[next_level][next_node]
                except KeyError:
                    nodes_per_level[next_level][next_node] = next_cost
                else:
                    if existing_cost > next_cost:
                        nodes_per_level[next_level][next_node] = next_cost
        del nodes_per_level[current_level]
        current_level += 1
