from sys import argv

from tools02 import parse_game, max_dict


def is_possible(result_dict, limit_dict):
    """
    Return True of the result of a game or round (respresented by a dict,
    such as the ones returned by `max_dict` or `parse_round`) is possible,
    according to the `limit_dict`, or False otherwise.

    For example:
    ```
    >>> max_dict(rounds)
    {'blue': 6, 'red': 4, 'green': 2}
    >>> is_possible(max_dict(rounds), limit_dict={'red': 12, 'green': 13, 'blue': 14})
    True
    >>> is_possible(max_dict(rounds), limit_dict={'red': 12, 'green': 13, 'blue': 4})
    False
    ```
    """
    return all(
        result_dict[colour] <= limit_dict[colour]
        for colour in result_dict
    )


if __name__ == '__main__':
    # what the bag contains (determines which games are possible)
    limit_dict = {'red': 12, 'green': 13, 'blue': 14}
    with open(argv[1]) as file:
        result = 0
        for line in file:
            id, rounds = parse_game(line)
            if is_possible(max_dict(rounds), limit_dict):
                result += id
        print(result)
