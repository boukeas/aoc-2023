from sys import argv

from tools05 import parse_file


if __name__ == '__main__':
    with open(argv[1]) as file:
        seeds, maps = parse_file(file.readlines())

    result = None
    # for each seed...
    for seed in seeds:
        # ... go over all the maps in the sequence
        for map in maps:
            # ... and translate the seed through each map
            seed = map.translate(seed)
        # keep track of the minimum destination location for the seeds
        if result is None or seed < result:
            result = seed
    print(result)
