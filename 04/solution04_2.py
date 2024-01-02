from collections import defaultdict
from sys import argv

from tools04 import parse_card


if __name__ == '__main__':
    with open(argv[1]) as file:
        nb_cards = 0
        # keep a tally of how many copies of each card you have
        tally = defaultdict(lambda: 1)
        for line in file:
            card_number, winning, player = parse_card(line)
            nb_cards += 1
            # intersection of winning numbers and player numbers
            nb_player_winning = len(winning & player)
            # for each winning number on the current card...
            for offset in range(nb_player_winning):
                # ... increase the tally of all remaining cards
                # by the number of copies of the current card
                tally[card_number + 1 + offset] += tally[card_number]

    # note: not sufficient to sum `tally.values()` because
    # cards with no winning numbers may not be included
    # in the `tally` dict
    result = sum(
        tally[card_number]
        for card_number in range(nb_cards)
    )
    print(result)
