from functools import reduce
from operator import mul
from sys import argv

from tools06 import winning_combinations_simple as winning_combinations


def parse_file(lines):
    line_iterator = iter(lines)
    line = next(line_iterator)
    header = 'Time: '
    times = [int(number) for number in line[len(header):].split()]
    line = next(line_iterator)
    header = 'Distance: '
    distances = [int(number) for number in line[len(header):].split()]
    return zip(times, distances)


def product(iterable):
    return reduce(mul, iterable)


if __name__ == '__main__':
    with open(argv[1]) as file:
        races = parse_file(file.readlines())
    result = product(
        winning_combinations(*race)
        for race in races
    )
    print(result)
