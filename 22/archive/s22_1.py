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
            bricks[index] = parse_line(line)

    #for brick in bricks.values():
    #    print(brick)

    # sanity check: all bricks extend in at most one direction
    for brick in bricks.values():
        # print(brick, sum(1 for index in range(3) if brick[0][index] != brick[1][index]))
        assert sum(1 for index in range(3) if brick[0][index] != brick[1][index]) <= 1

    print("computing all supports")
    support_dict = defaultdict(set)
    for (index1, brick1), (index2, brick2) in combinations(bricks.items(), 2):
        #print(index1, brick1, index2, brick2)
        if supports(brick1, brick2) == 0:
            support_dict[index1].add(index2)
        elif supports(brick1, brick2) == 1:
            support_dict[index2].add(index1)

    #top = set(bricks.keys()).difference(support_dict.keys())
    #print(f"{len(support_dict)=} {len(top)=} {sorted(top)=}")

    print("computing true supports (remove intermediates)")
    for index in dict(support_dict):
        support = support_dict[index]
        previous_working_support = support
        #print(f">>> {index=}, {support=}")
        working_support_full = set()
        while True:
            working_support = set()
            for support_index in previous_working_support:
                #print(f"{support_index=} -> {sorted(support_dict[support_index])}")
                working_support.update(support_dict[support_index])
            working_support.difference_update(working_support_full)
            if len(working_support) == 0:
                break
            support.difference_update(working_support)
            previous_working_support = working_support
            working_support_full.update(working_support)
            #print(f"{working_support=} {support=} {len(working_support_full)=}")
            #input()

    printable_support_dict = dict(sorted(support_dict.items()))
    for index, support in printable_support_dict.items():
        print(f"{index} supports {support}")

    print("computing supported bricks for each support")
    supported_dict = defaultdict(set)
    for index, support in support_dict.items():
        for supported_index in support:
            supported_dict[supported_index].add(index)

    bottom = set(bricks.keys()).difference(supported_dict.keys())
    print(f"{len(supported_dict)=} {len(bottom)=} {sorted(bottom)=}")

    printable_supported_dict = dict(sorted(supported_dict.items()))
    for index, supported in printable_supported_dict.items():
        print(f"{index} supported by {supported}")

    print("computing immovable supports")
    immovable = set()
    for index, supported in supported_dict.items():
        if len(supported) == 1:
            immovable.add(next(iter(supported)))
    print(f"{len(bricks)=} {len(immovable)=}")

    result = len(bricks) - len(immovable)
    print(result)
