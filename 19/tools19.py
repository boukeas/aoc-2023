from operator import lt, gt
import re


rule_re = re.compile(r'^(?P<label>[a-z]+){(?P<contents>.*)}')
condition_re = re.compile(r'((?P<field>[xmas])(?P<condition>[<>])(?P<value>[0-9]+):)?(?P<label>[AR]|[a-z]+)')

condition_map = {
    '<': lt,
    '>': gt
}


def parse_rule(line):
    label, contents = rule_re.match(line).groups()
    conditions = []
    for content in contents.split(','):
        match = condition_re.match(content)
        if match.group('field') is None:
            conditions.append(match.group('label'))
        else:
            conditions.append(
                (
                    match.group('field'),
                    condition_map[match.group('condition')],
                    int(match.group('value')),
                    match.group('label')
                )
            )
    return label, conditions


def parse_part(line):
    part_dict = {}
    fields = line[1:-1].split(',')
    for field in fields:
        name, value = field.split('=')
        part_dict[name] = int(value)
    return part_dict


def parse_file(lines):
    line_iter = (line.strip() for line in lines)
    rule_dict = {}
    for line in line_iter:
        line = line.strip()
        if len(line) == 0:
            break
        label, rule = parse_rule(line)
        rule_dict[label] = rule
    return rule_dict, [parse_part(line.strip()) for line in line_iter]
