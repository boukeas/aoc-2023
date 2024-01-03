from sys import argv

from tools19 import parse_file


def satisfies_condition(part_dict, condition):
    """
    A condition is a tuple that comprises:
    - the field that will be checked ('x', 'm', 'a' or 's')
    - the comparison operator that will be used (gt or lt)
    - the value that the field value will be compared to
    - the rule label to jump to if the condition holds
      (irrelevant here)
    """
    field, operator, value, _ = condition
    # apply the comparison operator between the field value and
    # the specified value
    return operator(part_dict[field], value)


def check_part(part_dict, rule_dict):
    '''
    Return True if `part_dict` is accepted by the rules in `rule_dict`
    or False otherwise.
    '''
    # always start at the rule labelled 'in'
    label = 'in'
    while True:
        if label == 'A':
            # accepted
            return True
        elif label == 'R':
            # rejected
            return False
        # retrieve the rule corresponding to the label
        # (a rule is a sequence of conditions, or just a label
        # leading to another rule)
        rule = rule_dict[label]
        for condition in rule:
            if isinstance(condition, tuple):
                if satisfies_condition(part_dict, condition):
                    # condition is true, current label is updated
                    # and no more conditions are scanned
                    label = condition[-1]
                    break
                else:
                    # condition is false, move to next condition
                    pass
            else:
                # no conditions remaining, just the final label
                label = condition
                break


if __name__ == '__main__':
    with open(argv[1]) as file:
        rule_dict, parts = parse_file(file.readlines())

    # sum the values of all fields for all parts
    # that are accepted by the rules
    result = sum(
        value
        for part_dict in parts
        for value in part_dict.values()
        if check_part(part_dict, rule_dict)
    )
    print(result)
