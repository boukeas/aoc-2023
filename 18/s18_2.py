from itertools import tee
from sys import argv
import re


line_str = r'(?P<direction>[LRUD]) (?P<length>[0-9]+) \(#(?P<colour>[0-9a-f]{6})\)'
line_re = re.compile(line_str)


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_file(lines):
    '''
    for line in lines:
        print(line.strip())
        yield tuple(line_re.match(line.strip()).groups())
    '''
    return tuple(
        tuple(line_re.match(line.strip()).groups())
        for line in lines
    )


instruction_map = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}


def colour_to_instruction(colour):
    distance_str = colour[:5]
    direction_str = colour[5]
    return (
        instruction_map[direction_str],
        int(distance_str, base=16)
    )


def follow(instructions, start=(0, 0)):
    direction_map = {
        'L': (0, -1),
        'R': (0, 1),
        'U': (-1, 0),
        'D': (1, 0)
    }
    coordinate = start
    for _, _, colour in instructions:
        yield coordinate
        direction_str, length = colour_to_instruction(colour)
        direction = direction_map[direction_str]
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
    # https://en.wikipedia.org/wiki/Shoelace_formula
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
    for instruction in instructions:
        print(instruction)
    '''
    '''
    for instruction, coordinates in zip(instructions, follow(instructions)):
        print(instruction, coordinates)
    '''

    boundary = nb_boundary_points(follow(instructions))
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    internal = area(follow(instructions)) - boundary / 2 + 1
    print(int(boundary + internal))
