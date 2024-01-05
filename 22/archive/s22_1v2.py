from collections import defaultdict
from itertools import combinations
from sys import argv


def parse_line(line):
    coord1, coord2 = line.strip().split('~')
    coord1 = tuple(int(coord) for coord in coord1.split(','))
    coord2 = tuple(int(coord) for coord in coord2.split(','))
    return coord1, coord2


def overlap(min1, max1, min2, max2):
    return not (max1 < min2 or max2 < min1)


def supports(brick1, brick2):
    if (
        overlap(brick1[0][0], brick1[1][0], brick2[0][0], brick2[1][0]) and
        overlap(brick1[0][1], brick1[1][1], brick2[0][1], brick2[1][1])
    ):
        try:
            assert not overlap(brick1[0][2], brick1[1][2], brick2[0][2], brick2[1][2])
        except AssertionError:
            print(brick1, brick2)
            exit()
        if brick1[1][2] < brick2[0][2]:
            return 0
        else:
            return 1


if __name__ == '__main__':
    bricks = {}
    with open(argv[1]) as file:
        for index, line in enumerate(file):
            brick = parse_line(line)
            z_min = brick[0][2]
            z_max = brick[1][2]
            if z_min == z_max:
                bricks[index] = brick
            else:
                for counter, z in enumerate(range(z_min, z_max + 1)):
                    bricks[(index, counter)] = ((brick[0][0], brick[0][1], z), (brick[1][0], brick[1][1], z))
    nb_bricks = index + 1

    #for brick in bricks.values():
    #    print(brick)

    # sanity check: all bricks extend in at most one direction
    for brick in bricks.values():
        # print(brick, sum(1 for index in range(3) if brick[0][index] != brick[1][index]))
        assert sum(1 for index in range(3) if brick[0][index] != brick[1][index]) <= 1

    print("computing all supported (naive)")
    overlap_dict = defaultdict(set)
    for (index1, brick1), (index2, brick2) in combinations(bricks.items(), 2):
        #print(index1, brick1, index2, brick2)
        if supports(brick1, brick2) == 0:
            overlap_dict[index2].add(index1)
        elif supports(brick1, brick2) == 1:
            overlap_dict[index1].add(index2)

    '''
    printable_supported_dict = dict(sorted(overlap_dict.items()))
    for index, supported in printable_supported_dict.items():
        print(f"{index} supported by {supported}")
    '''

    print("refining supported")
    supported_dict = {}
    remaining = set(overlap_dict)
    bottom = set(bricks).difference(overlap_dict)
    print(f"{len(remaining)=} {len(bottom)=} {bottom=}")
    while len(remaining) > 0:
        new_bottom = set()
        for index in remaining:
            supported_dict[index] = overlap_dict[index].intersection(bottom)
            overlap_dict[index].difference_update(bottom)
            if len(overlap_dict[index]) == 0:
                new_bottom.add(index)
        bottom = new_bottom
        remaining.difference_update(bottom)
        print(f"{len(remaining)=} {len(bottom)=} {bottom=}")

    print("computing immovable supports")
    immovable = set()
    for index, supported in supported_dict.items():
        if len(supported) == 1:
            unique_support = next(iter(supported))
            if isinstance(unique_support, tuple):
                unique_support = unique_support[0]
            if isinstance(index, tuple):
                index = index[0]
                if index == unique_support:
                    continue
            immovable.add(unique_support)

    print(f"{nb_bricks=} {len(immovable)=}")
    result = nb_bricks - len(immovable)
    print(result)
