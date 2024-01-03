import numpy as np


def parse_file(lines):
    for line in lines:
        coordinates, speeds = line.strip().split('@')
        coordinates = tuple(
            int(coordinate)
            for coordinate in coordinates.strip().split(', ')
        )
        speeds = tuple(
            int(speed)
            for speed in speeds.strip().split(', ')
        )
        yield np.array(coordinates), np.array(speeds)
