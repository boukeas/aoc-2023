from collections import defaultdict, deque
from sys import argv

from tools21 import Direction, get_contents, get_next_position, parse_file, within_bounds


def generate_neighbour_positions(position, matrix, size):
    """
    Given a specific position in a matrix, generate the coordinates
    of the positions that are directly accessible from it.
    """
    for direction in Direction:
        next_position = get_next_position(position, direction)
        if (
            within_bounds(next_position, size) and
            get_contents(next_position, matrix) != '#'
        ):
            yield next_position


def search(start, matrix, size, radius):
    layer_nodes = {start}
    for layer in range(radius):
        new_layer_nodes = set()
        while len(layer_nodes) > 0:
            position = layer_nodes.pop()
            extensions = set(generate_neighbour_positions(position, matrix, size))
            new_layer_nodes.update(extensions)
        layer_nodes = new_layer_nodes
    return len(layer_nodes)


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, start, data = parse_file(file.readlines())

    try:
        radius = int(argv[2])
    except IndexError:
        radius = 6

    result = search(start, data, size, radius=radius)
    print(result)
