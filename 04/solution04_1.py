from sys import argv

from tools04 import parse_card


if __name__ == '__main__':
    with open(argv[1]) as file:
        result = 0
        for line in file:
            _, winning, player = parse_card(line)
            # intersection of winning numbers and player numbers
            nb_player_winning = len(winning & player)
            if nb_player_winning > 0:
                result += 2 ** (nb_player_winning-1)
        print(result)
