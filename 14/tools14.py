"""
Obviously it's not the most elegant of approaches to have four different
functions for the four tilt directions but that's not really the point of
the puzzle, is it?
"""


def tilt_north(size, map):
    nb_rows, nb_columns = size
    for column in range(nb_columns):
        last = -1
        for row in range(nb_rows):
            if map[row][column] == 'O':
                last += 1
                if row > last:
                    map[last][column] = 'O'
                    map[row][column] = '.'
            elif map[row][column] == '#':
                last = row


def tilt_south(size, map):
    nb_rows, nb_columns = size
    for column in range(nb_columns):
        last = nb_rows
        for row in reversed(range(nb_rows)):
            if map[row][column] == 'O':
                last -= 1
                if row < last:
                    map[last][column] = 'O'
                    map[row][column] = '.'
            elif map[row][column] == '#':
                last = row


def tilt_west(size, map):
    nb_rows, nb_columns = size
    for row in range(nb_rows):
        last_column = -1
        for column in range(nb_columns):
            if map[row][column] == 'O':
                last_column += 1
                if column > last_column:
                    map[row][last_column] = 'O'
                    map[row][column] = '.'
            elif map[row][column] == '#':
                last_column = column


def tilt_east(size, map):
    nb_rows, nb_columns = size
    for row in range(nb_rows):
        last_column = nb_columns
        for column in reversed(range(nb_columns)):
            if map[row][column] == 'O':
                last_column -= 1
                if column < last_column:
                    map[row][last_column] = 'O'
                    map[row][column] = '.'
            elif map[row][column] == '#':
                last_column = column


def support_north(size, map):
    nb_rows, nb_columns = size
    load = 0
    row_load = nb_rows
    for row in map:
        for symbol in row:
            if symbol == 'O':
                load += row_load
        row_load -= 1
    return load


def parse_file(lines):
    result = [
        [char for char in line.strip()]
        for line in lines
    ]
    return (len(result), len(result[0])), result
