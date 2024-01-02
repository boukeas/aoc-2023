import re
from sys import argv


digits = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

# retrieve the spelled out digits into a string
# (to be included in the regular expression that matches digits)
digits_str = "|".join(digits.keys())

# regular expressions: looks for the first and last digits in a line
# (including digits that are spelled out)
first_re_str = r'^\D*?(?P<first>' + digits_str + r'|\d)\S*$'
first_re = re.compile(first_re_str)
last_re_str = r'^\S*(?P<last>' + digits_str + r'|\d)\D*$'
last_re = re.compile(last_re_str)


def extract_digit(digit_str):
    """
    Return the equivalent digit from a string
    (even when the digit is spelled out, e.g. 'eight')
    """
    try:
        return int(digit_str)
    except ValueError:
        return digits[digit_str]


def extract_value(line: str):
    """
    Return a two-digit integer comprising the first and last digits
    matched in `line`
    """
    digit_1 = first_re.match(line).group('first')
    digit_2 = last_re.match(line).group('last')
    return int(f"{extract_digit(digit_1)}{extract_digit(digit_2)}")


if __name__ == '__main__':
    with open(argv[1]) as file:
        result = sum(
            extract_value(line)
            for line in file
        )
    print(result)
