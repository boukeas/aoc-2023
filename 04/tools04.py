def parse_card(card_str):
    card_number_str, numbers_str = card_str.strip().split(':')
    assert card_number_str[:5] == 'Card '
    card_number = int(card_number_str[5:])
    winning_numbers_str, player_numbers_str = numbers_str.strip().split('|')
    winning_numbers = set(
        int(number)
        for number in winning_numbers_str.strip().split()
    )
    player_numbers = set(
        int(number)
        for number in player_numbers_str.strip().split()
    )
    return card_number, winning_numbers, player_numbers
