from abc import abstractmethod
from collections import deque


class Recorder:
    """
    Classes derived from `Recorder` record pulse events
    (in order to monitor the process).

    Make sure you add any recorders to `Module._recorders`
    """

    @abstractmethod
    def record(self, source, destination, pulse):
        raise NotImplementedError


class Module:

    # class-wide index of modules, mapping labels to module objects
    _module_dict = {}
    # class-wide queue of sent but yet-to-be-processed pulses:
    # stores (sender label, pulse) pairs
    _pulses = deque()
    # a set of recorder objects: they get notified of all pulses sent
    _recorders = set()

    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations
        # register module in the class-wide index
        self._module_dict[label] = self

    @abstractmethod
    def receive(self, source, pulse):
        # specifies what is to be done when a pulse is received
        raise NotImplementedError

    def send(self, pulse):
        # print(f"{self.label}: {pulse} -> {', '.join(self.destinations)}")
        # add pulse to class-wide queue,
        # to be processed when `activate` is called
        self._pulses.append((self.label, pulse))

    @classmethod
    def activate(cls):
        # process all pulses in the queue, i.e. call `receive`
        # on all destination modules
        while len(cls._pulses) > 0:
            source, pulse = cls._pulses.popleft()
            for destination in cls._module_dict[source].destinations:
                # record the event for all registered recorders
                for recorder in cls._recorders:
                    recorder.record(source, destination, pulse)
                try:
                    cls._module_dict[destination].receive(source, pulse)
                except KeyError:
                    pass


class FlipFlop(Module):
    """
    Flip-flop modules are either on or off; they are initially off.

    If a flip-flop module receives a high pulse, it is ignored and nothing
    happens. However, if a flip-flop module receives a low pulse, it flips
    between on and off. If it was off, it turns on and sends a high pulse.
    If it was on, it turns off and sends a low pulse
    """

    def __init__(self, label, destinations):
        super().__init__(label, destinations)
        self.state = 'off'

    def receive(self, source, pulse):
        if pulse == 'low':
            if self.state == 'off':
                self.state = 'on'
                self.send('high')
            else:
                self.state = 'off'
                self.send('low')


class Conjunction(Module):
    """
    Conjunction modules remember the type of the most recent pulse
    received from each of their connected input modules; they initially
    default to remembering a low pulse for each input.

    When a pulse is received, the conjunction module first updates its
    memory for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    """

    def __init__(self, label, destinations):
        super().__init__(label, destinations)
        self.state = {}

    @classmethod
    def init(cls):
        for source_module in Module._module_dict.values():
            for destination in source_module.destinations:
                try:
                    destination_module = Module._module_dict[destination]
                except KeyError:
                    pass
                else:
                    if isinstance(destination_module, cls):
                        destination_module.state[source_module.label] = 'low'

    def receive(self, source, pulse):
        self.state[source] = pulse
        if all(pulse == 'high' for pulse in self.state.values()):
            self.send('low')
        else:
            self.send('high')


class Broadcaster(Module):
    """
    There is a single broadcast module (named broadcaster).

    When it receives a pulse, it sends the same pulse to all of its
    destination modules.
    """

    def receive(self, source, pulse):
        self.send(pulse)


class Button(Module):
    """
    There is a module with a single button on it called, aptly,
    the button module.

    When you push the button, a single low pulse is sent directly
    to the broadcaster module.
    """

    def __init__(self):
        super().__init__('button', ['broadcaster'])

    def press(self):
        self.send('low')
        self.activate()


module_type_map = {
    'broadcaster': Broadcaster,
    '%': FlipFlop,
    '&': Conjunction
}


def parse_module(line):
    module_str, destinations_str = line.split(' -> ')
    if module_str == 'broadcaster':
        type = module_str
        module = module_str
    else:
        type = module_str[0]
        module = module_str[1:]
    destinations = tuple(
        destination.strip()
        for destination in destinations_str.split(', ')
    )
    # create module
    # (automatically registers in Module._module_dict)
    module_type_map[type](module, destinations)
