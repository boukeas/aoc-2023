from sys import argv

from tools03 import parts_from_schematic


if __name__ == '__main__':
    with open(argv[1]) as file:
        schematic = tuple(line.strip() for line in file)

    result = sum(
        (part := part_data[0])
        for part_data in parts_from_schematic(schematic)
    )
    print(result)
