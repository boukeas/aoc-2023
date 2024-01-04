from sys import argv

from tools16 import Direction, nb_energised, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data = parse_file(file.readlines())

    result = nb_energised((0, -1), Direction.East, data, size)
    print(result)
