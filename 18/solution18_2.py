from sys import argv

from tools18 import Direction, area, follow, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions_raw = parse_file(file.readlines())

    direction_map = {
        '2': Direction.Left,
        '0': Direction.Right,
        '3': Direction.Up,
        '1': Direction.Down
    }
    # convert raw instructions to tuples of the form:
    # (direction: Direction, length: int)
    instructions = (
        (direction_map[colour_str[5]], int(colour_str[:5], base=16))
        for _, _, colour_str in instructions_raw
    )

    coordinates = follow(instructions)
    print(area(coordinates))
