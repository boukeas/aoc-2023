from sys import argv

from tools18 import area, follow, parse_file


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


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions = parse_file(file.readlines())

    _, boundary, internal = area(follow(instructions))
    print(boundary + internal)
