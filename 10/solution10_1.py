from sys import argv
import math

from tools10 import parse_file, follow


if __name__ == '__main__':
    with open(argv[1]) as file:
        start_coordinates, pipe_map = parse_file(file.readlines())

    trail = follow(start_coordinates, pipe_map)
    trail_length = len(tuple(trail))
    result = math.ceil(trail_length / 2)
    print(result)
