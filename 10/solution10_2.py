from collections import defaultdict
from sys import argv

from tools10 import parse_file, follow


def count_inside(start_coordinates, pipe_map):
    # create a dict mapping a row number to the set of columns
    # intersected by the pipe trail
    intersections = defaultdict(set)
    # follow the pipe trail and record all intersections
    for (row, column), symbol, _ in follow(start_coordinates, pipe_map):
        intersections[row].add((column, symbol))
    # for each row, sort the intersections by column
    intersections = {
        row: sorted(row_intersections)
        for row, row_intersections in intersections.items()
    }

    total_inside_count = 0
    # iterate over all rows with intersections
    for row, intersection_line in intersections.items():
        # iterate over all intersections within a row
        # (we will be checking *pairs* of consecutive intersections
        # and add their distance to the "inside" count if they are
        # on the inside of the trail)
        intersection_iter = iter(intersection_line)
        # initial values
        previous_intersection = -1
        previous_symbol = None
        # this boolean keeps track of whether or not we are
        # on the inside of the trail
        inside = False
        inside_count = 0
        while True:
            try:
                intersection, symbol = next(intersection_iter)
            except StopIteration:
                break
            if symbol == '-':
                continue
            if symbol in ('L', 'F'):
                # we have encountered a new "starting" corner
                if inside:
                    inside_count += intersection - previous_intersection - 1
            if symbol in ('|'):
                if inside:
                    inside_count += intersection - previous_intersection - 1
                # flip: we are now on the other side of the trail
                inside = not inside
            if (
                (symbol == 'J' and previous_symbol == 'F') or
                (symbol == '7' and previous_symbol == 'L')
            ):
                # we have encountered a new "ending" corner
                # flip: we are on the other side of the trail
                # *depending* on the previous corner,
                # i.e. depending on whether the edge we have been
                # riding is convex or concave
                inside = not inside
            previous_intersection = intersection
            previous_symbol = symbol
        total_inside_count += inside_count
    return total_inside_count


if __name__ == '__main__':
    with open(argv[1]) as file:
        start_coordinates, pipe_map = parse_file(file.readlines())

    result = count_inside(start_coordinates, pipe_map)
    print(result)
