from collections import defaultdict
from itertools import combinations
from sys import argv


from tools22 import overlaps, parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        bricks = parse_file(file)
    nb_bricks = len(bricks)

    under = defaultdict(set)
    for (index1, brick1), (index2, brick2) in combinations(bricks.items(), 2):
        if overlaps(brick1, brick2) == 0:
            under[index2].add(index1)
        elif overlaps(brick1, brick2) == 1:
            under[index1].add(index2)

    layered_supported_dict = {}
    remaining = set(under)
    bottom = set(bricks).difference(under)
    while len(remaining) > 0:
        new_bottom = set()
        for index in remaining:
            layered_supported_dict[index] = under[index].intersection(bottom)
            under[index].difference_update(bottom)
            if len(under[index]) == 0:
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

    result = nb_bricks - len(immovable)
    print(result)
