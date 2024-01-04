from collections import Counter, defaultdict
from itertools import tee
from sys import argv
from scipy import signal
import numpy as np


from tools14 import (
    parse_file,
    tilt_east, tilt_north, tilt_south, tilt_west,
    support_north
)


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def find_period(cycle_dict):
    """
    There will be entries in the `cycle_dict` like this:
    ```
    87: [1]
    ```
    Support value 87 only appeared at the end of the first cycle.
    However, after some iterations, the support numbers at the end of
    each cycle will settle into periodic pattern. For example:
    ```
    68: [9, 16, 23, 30, 37, 44, ...]
    # diffs: [7, 7, 7, 7, 7, 7, ...]
    ```
    Support value 68 clearly appears every 7 cycles. There are also cases
    like this:
    ```
    65: [5, 7, 12, 14, 19, 21, 26, ...]
    # diffs: [2, 5, 2, 5, 2, 5, ...]
    ```
    Support value 65 appears every 2 and then 5 cycles but the overall
    period of the pattern is still 7.

    In order to calculate the (common) period of the cycle number sequences
    appearing in the `cycle_dict`, we will perform an FFT on the diffs for
    each one of them.

    Note that this is _not_ imfallible, as the FFT may get confused by entries
    in the cycle dict that are recorded before we fall into a periodic pattern,
    so this is why we use a `Counter` to find the most common "period"
    """
    periods = Counter()
    for support, cycles in cycle_dict.items():
        # compute the differences between consecutive cycle numbers
        diffs = list(b-a for a, b in pairwise(cycles))
        # perform FFT to check for periodicity
        f, P = signal.periodogram(diffs)
        try:
            # retrieve the frequency index with the highest amplitude
            frequency_index = np.argmax(P)
        except ValueError:
            # no periodicity
            # (stems from support values appearing before we
            # settle into a periodical pattern)
            pass
        else:
            if frequency_index > 0:
                # the cycle diffs are periodical
                cycles_period = round(1/f[frequency_index])
            else:
                # the cycle diffs are constant
                cycles_period = 1
            # the *actual* period is the sum of `cycles_period` consecutive diffs
            candidate_period = sum(diffs[-cycles_period:])
            periods[candidate_period] += 1
    return periods.most_common(1)[0][0]


if __name__ == '__main__':
    with open(argv[1]) as file:
        size, data = parse_file(file.readlines())

    nb_cycles = 1000000000
    nb_cycles_short = 1000

    # perform a limited number of cycles:
    # use `cycle_dict` to record the cycle numbers at which
    # a specific support was encountered at the end of a cycle
    cycle_dict = defaultdict(list)
    for cycle in range(1, nb_cycles_short):
        tilt_north(size, data)
        tilt_west(size, data)
        tilt_south(size, data)
        tilt_east(size, data)
        support = support_north(size, data)
        cycle_dict[support].append(cycle)

    period = find_period(cycle_dict)

    # figure out the cycle number we are looking for
    # (it needs to be just below `nb_cycles_short`)
    modulo = nb_cycles % period
    target_cycle = modulo + period * ((nb_cycles_short - modulo - period) // period)

    # whichever support value appears at the end of the `target_cycle`
    # will be the support value that will also appear at the end of
    # cycle 1000000000.
    for support, cycles in cycle_dict.items():
        if target_cycle in cycles:
            result = support
            break
    print(result)
