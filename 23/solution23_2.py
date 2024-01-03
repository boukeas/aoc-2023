from sys import argv


from tools23 import (
    get_all_neighbour_positions,
    parse_file,
    search_distances, find_distances
)


"""
The only difference between this and the puzzle 1 version
is that the generic `get_all_neighbour_positions` is used
as the neighbour generator, i.e. all neighbours are considered
valid and slopes are not taken into account.
"""


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data, start, end = parse_file(file.readlines())

    distances = find_distances(
        start, data, size,
        neighbour_position_generator=get_all_neighbour_positions
    )
    result = max(search_distances(start, distances))
    print(result)
