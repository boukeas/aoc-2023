from sys import argv
import numpy as np

from tools22 import create_supported_dict, parse_file


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

    result = nb_bricks - len(immovable)
    print(result)
