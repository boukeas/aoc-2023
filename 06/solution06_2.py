from sys import argv

from tools06 import winning_combinations


def parse_file(lines):
    line_iterator = iter(lines)
    line = next(line_iterator)
    header = 'Time: '
    time = int("".join(number for number in line[len(header):].split()))
    line = next(line_iterator)
    header = 'Distance: '
    distance = int("".join(number for number in line[len(header):].split()))
    return time, distance


if __name__ == '__main__':
    with open(argv[1]) as file:
        race = parse_file(file.readlines())
    print(winning_combinations(*race))
