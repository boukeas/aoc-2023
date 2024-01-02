from sys import argv
from collections import Counter
from operator import itemgetter

from tools07 import parse_file, values


def type(hand):
    """
    Return an integer corresponding to the "type" of the hand, with 1 being
    the weakest and 7 being the strongest.

    From the puzzle definition:
    > Every hand is exactly one type. From strongest to weakest, they are:
    > - Five of a kind, where all five cards have the same label: AAAAA
    > - Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    > - Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    > - Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    > - Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    > - One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    > - High card, where all cards' labels are distinct: 23456
    """
    # count occurrences of distinct cards, sorted by most occurrences
    counters = sorted(Counter(hand).items(), key=itemgetter(1), reverse=True)
    distinct = len(counters)
    highest_count = counters[0][1]
    # determine the type of hand, depending either on the count of the
    # the highest occurring card or the number of distinct cards
    if highest_count == 5:
        # five of a kind
        return 7
    elif highest_count == 4:
        # four of a kind
        return 6
    elif distinct == 2:
        # full house
        return 5
    elif highest_count == 3:
        # three of a kind
        return 4
    elif distinct == 3:
        # two pair
        return 3
    elif highest_count == 2:
        # one pair
        return 2
    else:
        # high card
        return 1


if __name__ == '__main__':
    with open(argv[1]) as file:
        hands = parse_file(file.readlines())

    # specify the values of face cards
    face_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    # the hands are sorted first by type and then by values
    hands = sorted(
        (type(hand), values(hand, face_values), bid)
        for hand, bid in hands
    )
    # the rank required for the result is obtained by enumeration
    # on the sorted list of hands
    result = sum(
        rank * bid
        for rank, (_, _, bid) in enumerate(hands, start=1)
    )
    print(result)
