from itertools import tee
from sys import argv
import re


line_str = r'(?P<direction>[LRUD]) (?P<length>[0-9]+) \(#(?P<colour>[0-9a-f]{6})\)'
line_re = re.compile(line_str)


def follow(instructions, start=(0, 0)):
    direction_map = {
        'L': (0, -1),
        'R': (0, 1),
        'U': (-1, 0),
        'D': (1, 0)
    }
    coordinate = start
    for direction_str, length_str, colour in instructions:
        yield coordinate
        direction = direction_map[direction_str]
        length = int(length_str)
        coordinate = (
            coordinate[0] + direction[0] * length,
            coordinate[1] + direction[1] * length
        )
    yield coordinate


'''
def area(coordinates):
    coordinates_iter = iter(coordinates)
    x1, y1 = next(coordinates_iter)
    acc = 0
    for (x, y), (x_next, y_next) in pairwise(coordinates_iter):
        acc += x * y_next - x_next * y
    return abs(acc) / 2
'''


def nb_boundary_points(coordinates):
    coordinates_iter = iter(coordinates)
    x1, y1 = next(coordinates_iter)
    x_prev, y_prev = x1, y1
    counter = 0
    while True:
        try:
            x, y = next(coordinates_iter)
        except StopIteration:
            break
        increment = abs(x - x_prev) + abs(y - y_prev)
        counter += increment
        x_prev, y_prev = x, y
    return counter


def area(coordinates):
    coordinates_iter = iter(coordinates)
    x1, y1 = next(coordinates_iter)
    x_prev, y_prev = x1, y1
    acc = 0
    while True:
        try:
            x, y = next(coordinates_iter)
        except StopIteration:
            break
        increment = x_prev * y - x * y_prev
        acc += increment
        x_prev, y_prev = x, y
    return abs(acc) / 2


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions = parse_file(file.readlines())

    '''
    for instruction, coordinates in zip(instructions, follow(instructions)):
        print(instruction, coordinates)
    '''

    boundary = nb_boundary_points(follow(instructions))
    internal = area(follow(instructions)) - boundary / 2 + 1
    print(boundary + internal)
