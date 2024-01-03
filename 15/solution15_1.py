from sys import argv

from tools15 import hash, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions = parse_file(file.read())

    result = sum(
        hash(instruction)
        for instruction in instructions
    )
    print(result)
