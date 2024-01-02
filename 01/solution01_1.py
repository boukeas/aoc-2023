import re
from sys import argv


# regular expressions: looks for the first and last digits in a line
first_re_str = r'^\D*(?P<first>\d)\S*$'
first_re = re.compile(first_re_str)
last_re_str = r'^\S*(?P<last>\d)\D*$'
last_re = re.compile(last_re_str)


def extract_value(line: str):
    """
    Return a two-digit integer comprising the first and last digits
    matched in `line`
    """
    digit_1 = first_re.match(line).group('first')
    digit_2 = last_re.match(line).group('last')
    return int(f"{digit_1}{digit_2}")


if __name__ == '__main__':
    with open(argv[1]) as file:
        result = sum(
            extract_value(line)
            for line in file
        )
    print(result)
