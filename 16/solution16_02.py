from sys import argv

from tools16 import Direction, nb_energised, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data = parse_file(file.readlines())

    max_east = max(
        nb_energised((init_row, -1), Direction.East, data, size)
        for init_row in range(size[0])
    )
    max_west = max(
        nb_energised((init_row, size[1]), Direction.West, data, size)
        for init_row in range(size[0])
    )
    max_south = max(
        nb_energised((-1, init_column), Direction.South, data, size)
        for init_column in range(size[1])
    )
    max_north = max(
        nb_energised((size[0], init_column), Direction.North, data, size)
        for init_column in range(size[1])
    )
    print(max(max_east, max_west, max_south, max_north))
