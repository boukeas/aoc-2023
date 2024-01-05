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


def collapse(index, support_dict, supported_dict):
    original_index = index
    collapsed = {original_index}
    layer = {original_index}
    while True:
        next_layer = set()
        for index in layer:
            next_layer.update(
                supported_index
                for supported_index in support_dict[index]
                if supported_dict[supported_index].issubset(collapsed)
            )
        if len(next_layer) == 0:
            break
        layer = next_layer
        collapsed.update(layer)
    collapsed.remove(original_index)
    return collapsed


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

    overlap_dict = defaultdict(set)
    for (index1, brick1), (index2, brick2) in combinations(bricks.items(), 2):
        if supports(brick1, brick2) == 0:
            overlap_dict[index2].add(index1)
        elif supports(brick1, brick2) == 1:
            overlap_dict[index1].add(index2)

    layered_supported_dict = {}
    remaining = set(overlap_dict)
    bottom = set(bricks).difference(overlap_dict)
    while len(remaining) > 0:
        new_bottom = set()
        for index in remaining:
            layered_supported_dict[index] = overlap_dict[index].intersection(bottom)
            overlap_dict[index].difference_update(bottom)
            if len(overlap_dict[index]) == 0:
                new_bottom.add(index)
        bottom = new_bottom
        remaining.difference_update(bottom)

    supported_dict = {}
    for index, supported in layered_supported_dict.items():
        if isinstance(index, tuple):
            index, _ = index
        if len(supported) == 1:
            unique_support = next(iter(supported))
            if isinstance(unique_support, tuple):
                unique_support = unique_support[0]
            if index == unique_support:
                continue
            else:
                supported_dict[index] = {unique_support}
        else:
            supported = {
                support_index[0] if isinstance(support_index, tuple) else support_index
                for support_index in supported
            }
            supported_dict[index] = supported

    immovable = set()
    for index, supported in supported_dict.items():
        if len(supported) == 1:
            immovable.add(next(iter(supported)))

    support_dict = defaultdict(set)
    for index, supported in supported_dict.items():
        for support_index in supported:
            support_dict[support_index].add(index)

    total_collapsed = 0
    for index in immovable:
        nb_collapsed = len(collapse(index, support_dict, supported_dict))
        print(index, nb_collapsed)
        total_collapsed += nb_collapsed
    print(total_collapsed)
