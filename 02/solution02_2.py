from sys import argv
from functools import reduce
from operator import mul

from tools02 import parse_game, max_dict


def power(game_dict):
    """
    Return the "power" of a game, as defined by the puzzle, i.e. the
    product of all cube cardinalities.

    For example:
    ```
    >>> max_dict(rounds)
    {'red': 6, 'blue': 2, 'green': 3}
    >>> power(max_dict(rounds))
    36
    ```
    """
    return reduce(mul, game_dict.values())


if __name__ == '__main__':
    with open(argv[1]) as file:
        result = sum(
            power(
                max_dict((rounds := parse_game(line)[1]))
            )
            for line in file
        )
        print(result)
