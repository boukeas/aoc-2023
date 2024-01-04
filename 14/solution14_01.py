from sys import argv

from tools14 import parse_file, tilt_north, support_north


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data = parse_file(file.readlines())

    tilt_north(size, data)

    result = support_north(size, data)
    print(result)
