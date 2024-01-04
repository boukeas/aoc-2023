from sys import argv

from tools18 import Direction, area, follow, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions_raw = parse_file(file.readlines())

    direction_map = {
        'L': Direction.Left,
        'R': Direction.Right,
        'U': Direction.Up,
        'D': Direction.Down
    }
    # convert raw instructions to tuples of the form:
    # (direction: Direction, length: int)
    instructions = (
        (direction_map[direction_str], int(length_str))
        for direction_str, length_str, _ in instructions_raw
    )

    coordinates = follow(instructions)
    print(area(coordinates))
