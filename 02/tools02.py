def parse_game(line):
    """
    Parse an input `line` representing a multi-round game and
    return the id of the game and a list of dicts, each representing
    the results of a game round.

    For example:
    ```
    >>> parse_game('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green')
    (1, [{'blue': 3, 'red': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'green': 2}])
    ```
    """
    game_str, rounds_str = line.split(':')
    rounds = []
    for round_str in rounds_str.strip().split(';'):
        rounds_dict = {}
        for balls in round_str.strip().split(','):
            number, colour = balls.strip().split(' ')
            rounds_dict[colour] = int(number)
        rounds.append(rounds_dict)
    return int(game_str[5:]), rounds


def max_dict(dicts):
    """
    Process an iterable of dicts and return a dict mapping each key encountered
    across these dicts to the maximum value for that key.

    For example:
    ```
    >>> rounds
    [{'blue': 3, 'red': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'green': 2}]
    >>> max_dict(rounds)
    {'blue': 6, 'red': 4, 'green': 2}
    ```
    """
    result_dict = {}
    for d in dicts:
        for key, value in d.items():
            result_dict[key] = max(result_dict.get(key, 0), value)
    return result_dict
