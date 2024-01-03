from collections import defaultdict
from enum import Enum


def parse_file(lines):
    result = []
    for row, line in enumerate(lines):
        result.append(line.strip())
    nb_rows = len(result)
    nb_columns = len(result[0])
    start = (0, result[0].index('.'))
    end = (nb_rows-1, result[-1].index('.'))
    return (nb_rows, nb_columns), result, start, end


class Direction(Enum):
    North = (-1, 0)
    South = (1, 0)
    East = (0, 1)
    West = (0, -1)


opposite_dict = {
    Direction.North: Direction.South,
    Direction.South: Direction.North,
    Direction.East: Direction.West,
    Direction.West: Direction.East
}


slope_map = {
    '>': Direction.East,
    '<': Direction.West,
    'v': Direction.South,
    '^': Direction.North
}


def get_contents(position, matrix):
    return matrix[position[0]][position[1]]


def get_neighbour_position(position, direction):
    return tuple(
        position_part + direction_part
        for position_part, direction_part in zip(position, direction.value)
    )


def get_all_neighbour_positions(position, matrix):
    """
    Given a specific position in a matrix, return a dict mapping
    each direction of movement that doesn't lead to a '#' to the
    coordinates of the neighbour in that direction.
    """
    return {
        direction: neighbour_position
        for direction in Direction
        if get_contents(
            (neighbour_position := get_neighbour_position(position, direction)),
            matrix
        ) != '#'
    }


def find_next_branching(position, direction, matrix, neighbour_position_generator):
    """
    Given a specific position and a direction of movement in a matrix, return
    position and distance of the next branching, i.e. the next junction.

    This function starts from the provided position and moves unidirectionally
    until it encounters a position where more than one direction of motion
    is possible. The `neighbour_position_generator` callable, provided as an
    argument, is used to generate neighbours.
    """
    position = get_neighbour_position(position, direction)
    distance = 1
    while True:
        try:
            neighbours = neighbour_position_generator(position, matrix)
        except IndexError:
            # `None` is used to indicate the exit position
            return None, distance
        try:
            # from the neighbours, remove the one
            # in the direction you came from
            neighbours.pop(opposite_dict[direction])
        except KeyError:
            pass
        if len(neighbours) == 1:
            # only one neighbour remaining, so not a junction:
            # move to that neighbour and repeat
            direction, position = neighbours.popitem()
            distance += 1
        else:
            # more than one neighbour remaining: a junction
            return position, distance


def find_all_branchings(matrix, size):
    """
    Scan the matrix and generate all the branching positions
    i.e. the coordinates of all junctions.
    """
    for row in range(1, size[0]-1):
        for column in range(1, size[1]-1):
            position = (row, column)
            if get_contents(position, matrix) != '#':
                neighbour_positions = get_all_neighbour_positions(position, matrix)
                if len(neighbour_positions) > 2:
                    yield position


def find_distances(start, matrix, size, neighbour_position_generator):
    """
    Return a two-level dict that maps coordinates of neighbouring
    junctions to the distance between them.

    For example, `distances[(3, 13)][(5, 12)]` would contain the
    distance between junctions at (3, 13) and (5,12), as long as
    (5,12) is directly reachable from (3, 13).
    """
    distances = defaultdict(dict)
    next_branching_position, distance = find_next_branching(start, Direction.South, matrix, neighbour_position_generator)
    distances[start][next_branching_position] = distance
    for branching_position in find_all_branchings(matrix, size):
        for direction in neighbour_position_generator(branching_position, matrix).keys():
            next_branching_position, distance = find_next_branching(branching_position, direction, matrix, neighbour_position_generator)
            distances[branching_position][next_branching_position] = distance
    return distances


def search_distances(start, distances):
    """
    Perform a depth-first search *between junctions* and generate the
    cost (distance) of each solution, i.e. each path between junctions
    that reaches the end position (marked as `None` in the distances
    matrix).

    Each node in the depth-first search stack holds:
    - the position of the latest junction
    - a set of junctions visited previously (to check for cycles)
    - the total distance to reach this junction
    """
    # make a copy so that the original can be retained and inspected
    distances = dict(distances)
    highest = 0
    position, distance = distances[start].popitem()
    stack = [(position, set(), distance)]
    while len(stack) > 0:
        position, path, distance = stack.pop()
        if position is None:
            if distance > highest:
                highest = distance
                print(f"\r{distance=}", end='')
            yield distance
        else:
            stack.extend(
                (next_position, path.union((position,)), distance + next_distance)
                for next_position, next_distance in distances[position].items()
                if next_position not in path
            )
    print()
