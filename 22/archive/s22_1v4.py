from collections import defaultdict
from itertools import combinations
from sys import argv


def parse_line(line):
    coord1, coord2 = line.strip().split('~')
    coord1 = tuple(int(coord) for coord in coord1.split(','))
    coord2 = tuple(int(coord) for coord in coord2.split(','))
    return coord1, coord2


def range_overlap(min1, max1, min2, max2):
    return not (max1 < min2 or max2 < min1)


def overlap(brick1, brick2):
    """
    Return None is there is no overlap between `brick1` and `brick2`.
    Otherwise:
    - return 0 if `brick1` is under `brick2` and
    - return 1 if `brick2` is under `brick1`
    """
    if (
        range_overlap(brick1[0][0], brick1[1][0], brick2[0][0], brick2[1][0]) and
        range_overlap(brick1[0][1], brick1[1][1], brick2[0][1], brick2[1][1])
    ):
        try:
            assert not range_overlap(brick1[0][2], brick1[1][2], brick2[0][2], brick2[1][2])
        except AssertionError:
            print(brick1, brick2)
            exit()
        if brick1[1][2] < brick2[0][2]:
            return 0
        else:
            return 1


def drop_brick(brick, floor):
    return (
        (brick[0][0], brick[0][1], floor + 1),
        (brick[1][0], brick[1][1], floor + 1 + brick[1][2] - brick[0][2]),
    )


def ceiling(bricks):
    return max(z_max for _, (_, _, z_max) in bricks)


if __name__ == '__main__':
    bricks = {}
    with open(argv[1]) as file:
        for index, line in enumerate(file):
            bricks[index] = parse_line(line)

    #for brick in bricks.values():
    #    print(brick)

    '''
    # sanity check: all bricks extend in at most one direction
    for brick in bricks.values():
        # print(brick, sum(1 for index in range(3) if brick[0][index] != brick[1][index]))
        assert sum(1 for index in range(3) if brick[0][index] != brick[1][index]) <= 1
    '''

    print("computing unders")
    under = defaultdict(set)
    for (index1, brick1), (index2, brick2) in combinations(bricks.items(), 2):
        overlap_result = overlap(brick1, brick2)
        if overlap_result == 0:
            under[index2].add(index1)
        elif overlap_result == 1:
            under[index1].add(index2)

    remaining = set(under)
    bottom = set(bricks).difference(under)
    print(sorted(bottom))

    '''
    print("refining supported")
    supported_dict = {}
    remaining = set(overlap_dict)
    bottom = set(bricks).difference(overlap_dict)
    for index in bottom:
        bricks[index] = drop_brick(bricks[index], floor=0)
    print(f"{len(remaining)=} {len(bottom)=} {bottom=}")
    while len(remaining) > 0:
        new_bottom = set()
        for index in remaining:
            supported_dict[index] = overlap_dict[index].intersection(bottom)
            overlap_dict[index].difference_update(bottom)
            if len(overlap_dict[index]) == 0:
                new_bottom.add(index)
        bottom = new_bottom
        for index in bottom:
            support_indices = set(supported_dict[index])
            floor = ceiling(bricks[support_index] for support_index in support_indices)
            bricks[index] = drop_brick(bricks[index], floor=floor)
            #not_really_supporting = {
            #    support_index
            #    for support_index in support_indices
            #    if bricks[support_index][1][2] < floor
            #}
            #if not_really_supporting:
            #    print(f"removing {not_really_supporting} from support of brick {index}")
            #    supported_dict[index].difference_update(not_really_supporting)
        remaining.difference_update(bottom)
        print(f"{len(remaining)=} {len(bottom)=} {bottom=}")

    print("computing immovable supports")
    immovable = set()
    for index, supported in supported_dict.items():
        if len(supported) == 1:
            immovable.add(next(iter(supported)))

    print(f"{len(bricks)=} {len(immovable)=}")
    result = len(bricks) - len(immovable)
    print(result)
    '''