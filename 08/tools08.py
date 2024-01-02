def parse_file(lines, line_re):
    # first line: instructions
    # (translate 'L' and 'R' into 0 and 1, to aid tuple access)
    line_iterator = iter(lines)
    direction_dict = {'L': 0, 'R': 1}
    instructions = [
        direction_dict[instruction]
        for instruction in next(line_iterator).strip()
    ]
    # blank line
    next(line_iterator)
    # map each node to a pair of neighbouring left and right nodes
    nodes = {}
    for line in line_iterator:
        node, left, right = line_re.match(line).groups()
        nodes[node] = (left, right)
    return instructions, nodes
