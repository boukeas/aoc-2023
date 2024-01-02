from math import lcm  # > Python 3.9
from itertools import cycle
from sys import argv
import re

from tools08 import parse_file


"""
# Observation

Each start node in the data reaches a specific unique end node
and then iterates over the same pattern, i.e. it reaches the
same end node again and again every `period` steps.

start   end
node    node    period
DFA     MRZ     18157
BLA     KMZ     14363
TGA     JVZ     19783
AAA     ZZZ     15989
PQA     TVZ     19241
CQA     RCZ     12737

So, instead of following all instructions simultaneously for all
start nodes, we follow the instructions separately for each node,
note down the period and then simply find the largest common factor
for all periods, i.e. the number of steps where all periods will
coincide: 13830919117339

The result indicates that a naive approach, i.e. actually following
the instructions simultaneously, is intractable
"""

# e.g. 22C = (22Z, 22Z)
node_re = r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)'


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions, nodes = parse_file(file.readlines(), re.compile(node_re))

    # gather all start nodes (they end in 'A')
    start_nodes = tuple(
        node
        for node in nodes
        if node.endswith('A')
    )
    periods = []
    # for each start node...
    for node in start_nodes:
        steps = 0
        start_node = node
        # go over the directions (repeatedly)...
        for direction in cycle(instructions):
            node = nodes[node][direction]
            steps += 1
            # ... until you find an end node (they end in 'Z')
            if node.endswith('Z'):
                periods.append(steps)
                break
    result = lcm(*periods)
    print(result)
