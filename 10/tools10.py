from enum import Enum


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


def opposite(direction):
    return opposite_dict[direction]


# for each pipe symbol, record the directions where it has openings
pipe_dict = {
    '|': {Direction.North, Direction.South},
    '-': {Direction.East, Direction.West},
    'L': {Direction.North, Direction.East},
    'J': {Direction.North, Direction.West},
    '7': {Direction.South, Direction.West},
    'F': {Direction.South, Direction.East},
}


def neighbour_coordinates(coordinates, direction):
    """
    Given a pair of (row, column) `coordinates`, return the coordinates
    of the neighbouring point in a specific `direction`
    """
    return (
        coordinates[0] + direction.value[0],
        coordinates[1] + direction.value[1]
    )


def start(start_coordinates, pipe_map):
    """
    Given the start coordindates in the pipe map, return the
    actual start symbol (i.e. under 'S') and the two directions
    that can be followed starting from 'S'
    """
    # create a dict that maps a direction to the symbols (pipe shapes)
    # that have openings in that direction
    pipe_symbols_from_direction = {
        direction: {
            symbol
            for symbol, directions in pipe_dict.items()
            if direction in directions
        }
        for direction in Direction
    }
    start_directions = set()
    # for every direction...
    for direction in Direction:
        neighbour_row, neighbour_column = neighbour_coordinates(start_coordinates, direction)
        if neighbour_row < 0 or neighbour_column < 0:
            continue
        try:
            # ... retrieve the neighbouring pipe symbol...
            neighbour = pipe_map[neighbour_row][neighbour_column]
        except IndexError:
            pass
        else:
            if neighbour == '.':
                continue
            # ... and check if the neighbour has an opening
            # towards the current position
            if neighbour in pipe_symbols_from_direction[opposite(direction)]:
                start_directions.add(direction)
    # knowing the two directions that the starting pipe has to link
    # calculate what the starting pipe symbol needs to be
    for symbol, direction_set in pipe_dict.items():
        if direction_set == start_directions:
            start_symbol = symbol
            break
    return start_symbol, start_directions


def follow(start_coordinates, pipe_map):
    """
    Starting from the start coordinates of the pipe map, generate a trail
    of (coordinates, pipe symbol, direction) tuples, following the pipe
    trail until returning to the start coordinates
    """
    start_symbol, directions = start(start_coordinates, pipe_map)
    direction = directions.pop()
    yield start_coordinates, start_symbol, direction
    coordinates = neighbour_coordinates(start_coordinates, direction)
    while coordinates != start_coordinates:
        symbol = pipe_map[coordinates[0]][coordinates[1]]
        # the pipe symbol has openings in two directions
        # remove the direction facing the current symbol (difference/opposite)
        # and retrieve the remaining direction (next/iter)
        direction = next(iter(pipe_dict[symbol].difference({opposite(direction)})))
        yield coordinates, symbol, direction
        coordinates = neighbour_coordinates(coordinates, direction)


def parse_file(lines):
    """
    Parse the lines in the input file and return the `(row, column)`
    coordinates of the starting point and the map of pipes, i.e. a list
    of strings, with each string representing a row in the pipe map
    """
    pipe_map = []
    line_iterator = enumerate(lines)
    for row, line in line_iterator:
        pipe_map.append(line.strip())
        try:
            # try to find the start position in each line
            column = line.index('S')
        except ValueError:
            pass
        else:
            break
    # after the start position has been found, just iterate
    # over the rest of the lines
    pipe_map.extend((line.strip() for _, line in line_iterator))
    return (row, column), pipe_map
