def parse_file(lines):
    for line in lines:
        hand, bid = line.split()
        yield hand, int(bid)


def value(card, face_values):
    try:
        return face_values[card]
    except KeyError:
        return int(card)


def values(hand, face_values):
    return tuple(value(card, face_values) for card in hand)
