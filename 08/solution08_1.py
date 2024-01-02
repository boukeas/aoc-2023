from sys import argv
import re

from tools08 import parse_file


node_re = r'([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)'


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions, nodes = parse_file(file.readlines(), re.compile(node_re))

    current_node = 'AAA'
    steps = 0
    while current_node != 'ZZZ':
        for direction in instructions:
            current_node = nodes[current_node][direction]
            steps += 1
    print(steps)
