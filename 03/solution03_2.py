from sys import argv
from collections import defaultdict

from tools03 import parts_from_schematic


if __name__ == '__main__':
    with open(argv[1]) as file:
        schematic = tuple(line.strip() for line in file)

    result = 0
    # create a dict that maps each gear to the set of parts
    # adjacent to that gear
    gears = defaultdict(set)
    for part_data in parts_from_schematic(schematic):
        part, part_line_number, part_position, symbol, symbol_line_number, symbol_position = part_data
        if symbol == '*':
            gears[(symbol_line_number, symbol_position)].add((part, part_line_number, part_position))

    # iterate over the gears connected to two parts
    # and sum the ratios (i.e. the product of the gear numbers)
    result = sum(
        parts_data[0][0] * parts_data[1][0]
        for _, parts_set in gears.items()
        if len((parts_data := tuple(parts_set))) == 2
    )
    print(result)
