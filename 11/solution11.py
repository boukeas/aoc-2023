from itertools import combinations
from sys import argv

from tools11 import distance, parse_file


if __name__ == '__main__':
    try:
        factor = int(argv[2])
    except IndexError:
        factor = 2

    with open(argv[1]) as file:
        coordinates = parse_file(file.readlines(), factor=factor)

    result = sum(
        distance(coordinate1, coordinate2)
        for coordinate1, coordinate2 in combinations(coordinates, 2)
    )
    print(result)
