from sys import argv

from tools17 import get_next_position, turn_direction, parse_file, within_bounds, search


def generate_next_positions(position, direction, matrix, size):
    """
    Generate the valid successor positions from the current `position`
    and `direction`.

    The "moves" implemented by this function are walk-and-turn moves,
    i.e. the next positions will be 1, 2 or 3 steps away from the original
    `position` towards `direction` and the next direction will represent
    a 90 degree turn away from that direction.
    """
    for next_direction in turn_direction[direction]:
        cost = 0
        # only allow moves in distances 1, 2 and 3
        for distance in range(1, 4):
            next_position = get_next_position(position, next_direction, distance)
            if within_bounds(next_position, size):
                # accumulate cost
                cost += matrix[next_position[0]][next_position[1]]
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
