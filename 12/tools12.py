from functools import lru_cache
import re


@lru_cache(maxsize=None)
def nb_arrangements(conditions, groups):
    if not groups:
        # no more groups remaining to assign
        if any(symbol == '#' for symbol in conditions):
            return 0
        else:
            return 1
    # find next batch of assignable symbols in the `conditions` string
    match = re.search(r'[#?]+', conditions)
    if not match:
        return 0
    # check if you need to explore the assignment branch, i.e if you can
    # assign the group to the batch of assignable symbols
    # - is the batch long enough to fit the group?
    # - can the symbol right *after* the assignment be a '.'?
    match_length = match.end() - match.start()
    group = groups[0]
    if (
        match_length >= group and (
            match.start() + group == len(conditions) or
            conditions[match.start() + group] != '#'
        )
    ):
        # recursive call for the remaining groups
        assignment_arrangements = nb_arrangements(
            conditions[match.start() + group + 1:],
            groups[1:]
        )
    else:
        assignment_arrangements = 0
    # check if you need to explore the non-assignment branch, i.e if you can
    # just assign a dot to the beginning of the current batch and move along
    # with the remaining conditions and groups
    # - is the first symbol of the batch a '?'?
    if conditions[match.start()] == '?':
        non_assignment_arrangements = nb_arrangements(
            conditions[match.start() + 1:],
            groups
        )
    else:
        non_assignment_arrangements = 0

    return assignment_arrangements + non_assignment_arrangements


def parse_file(lines, factor=1):
    for line in lines:
        conditions, groups = line.strip().split()
        groups = tuple(int(group) for group in groups.split(','))
        yield "?".join(conditions for _ in range(factor)), groups * factor
