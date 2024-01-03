from sys import argv


from tools20 import (
    Button, Conjunction, Module, Recorder,
    parse_module
)


class PulseCounter(Recorder):
    """
    Records the number of high and low pulses
    """

    def __init__(self):
        self.counters = {'high': 0, 'low': 0}

    def record(self, source, destination, pulse):
        self.counters[pulse] += 1

    @property
    def low(self):
        return self.counters['low']

    @property
    def high(self):
        return self.counters['high']


if __name__ == '__main__':

    with open(argv[1]) as file:
        for line in file:
            parse_module(line)

    Conjunction.init()
    # add a `PulseCounter` to the recorders
    Module._recorders.add((counter := PulseCounter()))

    button = Button()
    for _ in range(1000):
        button.press()

    print(counter.counters)
    print(counter.low * counter.high)
