from sys import argv

from tools17 import get_next_position, turn_direction, parse_file, within_bounds, search


def generate_next_positions(position, direction, matrix, size):
    """
    Generate the valid successor positions from the current `position`
    and `direction`.

    The "moves" implemented by this function are walk-and-turn moves,
    i.e. the next positions will be 4 to 11 steps away from the original
    `position` towards `direction` and the next direction will represent
    a 90 degree turn away from that direction.
    """
    for next_direction in turn_direction[direction]:
        cost = 0
        # generate all positions in distances 1 to 10
        # (because we need to accumulate the cost in these first 4 steps)
        for distance in range(1, 11):
            next_position = get_next_position(position, next_direction, distance)
            if within_bounds(next_position, size):
                # accumulate cost
                cost += matrix[next_position[0]][next_position[1]]
                # only yield positions that are at least 4 steps away
                if distance >= 4:
                    yield next_position, next_direction, cost, distance
            else:
                break


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data = parse_file(file.readlines())

    result = min(
        solution_cost
        for solution_cost in search(data, size, generate_next_positions)
    )
    print(result)
