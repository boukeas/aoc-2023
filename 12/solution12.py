from sys import argv

from tools12 import nb_arrangements, parse_file


if __name__ == '__main__':
    try:
        factor = int(argv[2])
    except IndexError:
        factor = 1

    with open(argv[1]) as file:
        data = parse_file(file.readlines(), factor=factor)

    result = sum(
        nb_arrangements(conditions, groups)
        for conditions, groups in data
    )
    print(result)
