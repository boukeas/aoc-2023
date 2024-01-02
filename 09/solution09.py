from sys import argv

from tools09 import extrapolate, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        sequences = parse_file(file.readlines())

    # the second command-line argument determines:
    # - forward extrapolation (1), the default
    # - backward extrapolation (0)
    try:
        position = int(argv[2])
    except IndexError:
        position = 1

    result = sum(
        extrapolate(sequence)[position]
        for sequence in sequences
    )
    print(result)
