def parse_file(line):
    return line.strip().split(',')


def hash(string):
    current = 0
    for character in string:
        ascii = ord(character)
        current += ascii
        current *= 17
        current %= 256
    return current
