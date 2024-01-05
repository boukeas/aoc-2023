from collections import defaultdict
from dataclasses import dataclass, field
import numpy as np
from typing import Tuple


def range_overlap(range1, range2):
    """
    Return True if `range1` and `range2` overlap
    """
    return not (range1[1] < range2[0] or range2[1] < range1[0])


@dataclass(order=True)
class Brick:
    priority: int = field(init=False)
    index: int = field(compare=False)
    coordinate_ranges: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]] = field(compare=False)

    def __post_init__(self):
        self.priority = self.coordinate_ranges[2][0]

    # define this so that set of `Brick`s can be formed
    def __hash__(self):
        return self.index

    def drop(self, ceilings):
        """
        Given the current `ceilings` (maximum z coordinate in all positions),
        return a new dropped `Brick` (and update the ceilings)
        """
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = self.coordinate_ranges
        # compute the z-coordinate on which the brick will land
        # (this is the maximum ceiling in the x,y area the brick occupies)
        floor = np.max(ceilings[min_x:max_x + 1, min_y:max_y + 1])
        dropped_brick = Brick(
            index=self.index,
            coordinate_ranges=self.coordinate_ranges[:2] + ((floor + 1, floor + 1 + max_z - min_z),)
        )
        # update the ceilings x,y area that the brick occupies
        ceilings[min_x:max_x + 1, min_y:max_y + 1] = dropped_brick.coordinate_ranges[2][1]
        return dropped_brick


def parse_file(file):
    bricks = []
    max_x, max_y = 0, 0
    for index, line in enumerate(file):
        coord1_str, coord2_str = line.strip().split('~')
        brick = Brick(
            index=index,
            coordinate_ranges=tuple(
                zip(
                    (int(coord) for coord in coord1_str.split(',')),
                    (int(coord) for coord in coord2_str.split(','))
                )
            )
        )
        bricks.append(brick)
        max_x = max(max_x, brick.coordinate_ranges[0][1])
        max_y = max(max_y, brick.coordinate_ranges[1][1])
    return (max_x + 1, max_y + 1), bricks


def create_supported_dict(bricks):
    """
    Given a list of bricks that is sorted by z-coordinate, return a dict
    that maps each brick to the set of bricks it is supported by.
    """
    supported = defaultdict(set)
    for index in range(len(bricks)):
        # current brick
        brick = bricks[index]
        # iterate over the rest of the bricks
        # (or at least the ones that it could possibly support)
        for other_index in range(index + 1, len(bricks)):
            other_brick = bricks[other_index]
            # we have reached a brick that has a higher floor than
            # the current brick's ceiling: stop, as there can be no
            # other bricks that the current brick can support
            if brick.coordinate_ranges[2][1] + 1 < other_brick.coordinate_ranges[2][0]:
                break
            elif (
                range_overlap(brick.coordinate_ranges[0], other_brick.coordinate_ranges[0]) and
                range_overlap(brick.coordinate_ranges[1], other_brick.coordinate_ranges[1])
            ):
                # the current brick's x,y area overlaps with the other brick's,
                # so the latter is supported by the former
                supported[other_brick].add(brick)
    return supported
