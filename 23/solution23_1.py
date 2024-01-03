from sys import argv

from tools23 import (
    Direction,
    get_contents, get_neighbour_position,
    opposite_dict,
    parse_file,
    slope_map,
    search_distances, find_distances
)


def get_neighbour_positions(position, matrix):
    """
    Given a specific position in a matrix, return a dict mapping
    each *valid* direction of movement to the coordinates of the
    neighbour in that direction.

    In this case, a direction of movement is valid if:
    - it doesn't lead to a '#'
    - it doesn't lead to a slope that can't be climbed
      (a slope opposite to the direction of movement)
    """
    neighbour_positions = {}
    for direction in Direction:
        neighbour_position = get_neighbour_position(position, direction)
        neighbour_contents = get_contents(neighbour_position, matrix)
        if (
            neighbour_contents != '#' and
            slope_map.get(neighbour_contents) != opposite_dict[direction]
        ):
            neighbour_positions[direction] = neighbour_position
    return neighbour_positions


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data, start, end = parse_file(file.readlines())

    distances = find_distances(
        start, data, size,
        neighbour_position_generator=get_neighbour_positions
    )
    result = max(search_distances(start, distances))
    print(result)
