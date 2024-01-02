from itertools import islice
from sys import argv

from tools05 import parse_file, Range


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


if __name__ == '__main__':
    with open(argv[1]) as file:
        seed_data, maps = parse_file(file.readlines())

    # interpret the seed data as ranges rather than individual numbers
    # (sorting is necessary for the translation that follows)
    ranges = sorted(Range(start, start+length) for start, length in batched(seed_data, n=2))
    # for each map...
    for map in maps:
        # ... translate the ranges through the map
        ranges = sorted(map.translate_ranges(ranges))

    # the minimum location is the start of the lowest range
    print(ranges[0].start)
