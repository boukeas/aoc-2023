from functools import reduce
from sys import argv
from operator import lt, mul

from tools19 import parse_file


"""
The `part_dict` represents a specific part, with bound values
for each field:
```
{'x': 3378, 'm': 2275, 'a': 534, 's': 2317}
```
The `domain_dict` is a generalisation of the `part_dict` that
stores a domain of values for each field:
```
{'x': (1, 1523), 'm': (3158, 3482), 'a': (1, 2499), 's': (3473, 4001)}
```
Note that the upper value of a domain is *not* included in the domain.
"""


def replace(domains, the_field, the_domain):
    """
    Replace the domain for a given field with updated values

    ```
    >>> domains
    {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}
    >>> replace(domains, 'm', (1, 2001))
    {'x': (1, 4001), 'm': (1, 2001), 'a': (1, 4001), 's': (1, 4001)}
    ```
    """
    return {
        a_field: the_domain if a_field == the_field else a_domain
        for a_field, a_domain in domains.items()
    }


def combinations(domain_dict):
    """
    Return the number of value combinations that correspond to a specific
    `domain_dict`. This is essentially the product of domain widths.
    ```
    >>> domain_dict = {'x': (1, 11), 'm': (6, 21), 'a': (1, 2), 's': (1, 2)}
    >>> combinations(domain_dict)
    150
    ```
    """
    return reduce(
        mul,
        (
            domain[1] - domain[0]
            for domain in domain_dict.values()
        ),
        1
    )


def compute(domains, conditions, rule_dict):
    """
    Return how many ways there are to satisfy the given conditions,
    given the current domains for the four fields ('x', 'm', 'a' and 's')
    and the rules in the `rule_dict`.

    A condition is a tuple that comprises:
    - the field that will be checked ('x', 'm', 'a' or 's')
    - the comparison operator that will be used (gt or lt)
    - the value that the field value will be compared to
    - the rule label to jump to if the condition holds
    """
    if len(conditions) == 1:
        # there is only one condition remaining:
        # it can only be a label (i.e. not a full condition)
        label = conditions[0]
        if label == 'A':
            # accept: the number of ways to satisfy this trivial
            # condition is the product of the domain widths
            return combinations(domains)
        elif label == 'R':
            # reject: there is no way to satisfy this trivial condition
            return 0
        else:
            # the label dictates a jump to a different rule:
            # the domains remain unchanged and the conditions
            # are replaced by the conditions of the new rule
            return compute(domains, rule_dict[label], rule_dict)

    # unpack the first of the conditions
    field, operator, value, jump_label = conditions[0]
    # unpack the domain of the field to which the condition applies
    domain_min, domain_max = domains[field]
    # perform the comparisons and modify the domains accordingly
    if operator is lt:
        if value < domain_min:
            # the domain cannot satisfy the condition:
            # continue recursively with the same domain and
            # the remaining conditions in the current rule
            return compute(domains, conditions[1:], rule_dict)
        else:
            # part of the domain satisfies the condition:
            # split the computation (and the domain) into the
            # values that satisfy the condition and those that don't
            return (
                # the lower part of the domain satisfies the condition:
                # continue recursively with the lower part of the domain
                # and the conditions in the rule labelled 'jump_label'
                compute(
                    domains=replace(domains, field, (domain_min, value)),
                    conditions=[jump_label],
                    rule_dict=rule_dict
                ) +
                # the upper part of the domain doesn't satisfy the condition:
                # continue recursively with the upper part of the domain and
                # the remaining conditions in the current rule
                compute(
                    domains=replace(domains, field, (value, domain_max)),
                    conditions=conditions[1:],
                    rule_dict=rule_dict
                )
            )
    else:
        if value > domain_max:
            # the domain cannot satisfy the condition:
            # continue recursively with the same domain and
            # the remaining conditions in the current rule
            return compute(domains, conditions[1:], rule_dict)
        else:
            # part of the domain satisfies the condition:
            # split the computation (and the domain) into the
            # values that satisfy the condition and those that don't
            return (
                # the upper part of the domain satisfies the condition:
                # continue recursively with the upper part of the domain
                # and the conditions in the rule labelled 'jump_label'
                compute(
                    domains=replace(domains, field, (value + 1, domain_max)),
                    conditions=[jump_label],
                    rule_dict=rule_dict
                ) +
                # the lower part of the domain doesn't satisfy the condition:
                # continue recursively with the lower part of the domain and
                # the remaining conditions in the current rule
                compute(
                    domains=replace(domains, field, (domain_min, value + 1)),
                    conditions=conditions[1:],
                    rule_dict=rule_dict
                )
            )


if __name__ == '__main__':
    with open(argv[1]) as file:
        rule_dict, _ = parse_file(file.readlines())

    # start with a domain of 1 to 4000 for each of the
    # four fields ('x', 'm', 'a' and 's') and the initial
    # 'in' rule
    result = compute(
domains={
    field: (1, 4001)
    for field in 'xmas'
},
        conditions=rule_dict['in'],
        rule_dict=rule_dict
    )
    print(result)
