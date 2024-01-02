import re


def candidate_part_ranges(line):
    """
    Return all (possible) part matches in `line`
    """
    for match in re.finditer(r'\d+', line):
        start, end = match.span()
        matched = line[start:end]
        yield (
            matched,
            (start, end-1)
        )


def candidate_symbol_ranges(line):
    """
    Return symbol matches in `line`
    """
    for match in re.finditer(r'[^.\d]', line):
        start, end = match.span()
        matched = line[start:end]
        yield matched, (start-1, end)


def ranges_overlap(range1, range2):
    """
    Return whether or not two ranges (x11, x12) and (x21, x22) overlap
    """
    x11, x12 = range1
    x21, x22 = range2
    return x21 <= x12 and x11 <= x22


def parts_from_ranges(part_ranges, symbol_ranges):
    """
    Return overlaps between `part_ranges` and `symbol_ranges`
    """
    for part, part_range in part_ranges:
        for symbol, symbol_range in symbol_ranges:
            if ranges_overlap(part_range, symbol_range):
                yield int(part), part_range, symbol, symbol_range[0]+1
                break


def parts_from_schematic(schematic):
    """
    Return all part data from the schematic in tuples of the form:
    `(part, part_line_number, part_position, symbol, symbol_line_number, symbol_position)`

    Note: this may contain duplicate *parts* if a part is adjacent to multiple
    symbols but disambiguation will be possible by the symbol information.
    """
    nb_lines = len(schematic)
    # first line
    line_number = 0
    line = schematic[line_number]
    # find all candidate parts and symbols in the line
    part_ranges = list(candidate_part_ranges(line))
    symbol_ranges = list(candidate_symbol_ranges(line))
    # combine candidate parts and symbols to retrieve parts
    line_parts = {
        (part, line_number, part_range[0], symbol, line_number, symbol_position)
        for part, part_range, symbol, symbol_position in parts_from_ranges(part_ranges, symbol_ranges)
    }
    yield from line_parts
    # rest of the lines
    for line_number in range(1, nb_lines):
        previous_line_part_ranges = part_ranges
        previous_line_symbol_ranges = symbol_ranges
        line = schematic[line_number]
        # find all candidate parts and symbols in the line
        part_ranges = list(candidate_part_ranges(line))
        symbol_ranges = list(candidate_symbol_ranges(line))
        # combine to retrieve parts:
        # - candidate parts and symbols from this line
        # - candidate parts from the previous line with symbols from this line
        # - candidate parts from this line with symbols from the previous line
        line_parts = {
            (part, line_number, part_range[0], symbol, line_number, symbol_position)
            for part, part_range, symbol, symbol_position in parts_from_ranges(part_ranges, symbol_ranges)
        } | {
            (part, line_number-1, part_range[0], symbol, line_number, symbol_position)
            for part, part_range, symbol, symbol_position in parts_from_ranges(previous_line_part_ranges, symbol_ranges)
        } | {
            (part, line_number, part_range[0], symbol, line_number-1, symbol_position)
            for part, part_range, symbol, symbol_position in parts_from_ranges(part_ranges, previous_line_symbol_ranges)
        }
        yield from line_parts
