from collections import defaultdict
import numpy as np
from sys import argv

from tools22 import create_supported_dict, parse_file


def collapse(brick, supports, supported_by):
    """
    Compute which bricks would collapse if `brick` was removed
    """
    original_brick = brick
    # the entire set of collapsed bricks
    collapsed = {original_brick}
    # the current wave of collapsing bricks
    layer = {original_brick}
    while True:
        # for every brick in the current wave of collapsing bricks...
        next_layer = {
            # ... collapse the bricks it supports...
            supported_brick
            for brick in layer
            for supported_brick in supports[brick]
            # ... as long as all its other supporting bricks
            # have already collapsed
            if supported_by[supported_brick].issubset(collapsed)
        }
        if len(next_layer) == 0:
            break
        layer = next_layer
        collapsed.update(layer)
    collapsed.remove(original_brick)
    return collapsed


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, bricks = parse_file(file)
    nb_bricks = len(bricks)

    # maintain a 2D array of the current "ceiling" (max z) in every position
    ceilings = np.zeros(size, dtype=np.int16)

    # sort bricks according to their minimum z-coordinate
    bricks = sorted(bricks)
    # drop all bricks, one by one, and then sort again
    bricks = sorted(brick.drop(ceilings) for brick in bricks)

    # map each brick to the set of bricks it is supported by
    supported_by = create_supported_dict(bricks)

    # if a brick is supported by a single brick, then the latter is immovable
    immovable = set()
    for supported_brick, supporting_bricks in supported_by.items():
        if len(supporting_bricks) == 1:
            immovable.add(next(iter(supporting_bricks)))

    # map each brick to the set of bricks it supports
    supports = defaultdict(set)
    for supported_brick, supporting_bricks in supported_by.items():
        for supporting_brick in supporting_bricks:
            supports[supporting_brick].add(supported_brick)

    # simulate the collapse of every immovable brick to compute the result
    result = sum(
        len(collapse(brick, supports, supported_by))
        for brick in immovable
    )
    print(result)
