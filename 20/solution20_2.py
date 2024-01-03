from collections import defaultdict
import math
from sys import argv

from tools20 import (
    Button, Conjunction, Module, Recorder,
    parse_module
)


class GatekeeperMonitor(Recorder):
    """
    Records the number of button presses required for the
    "gatekeeper" to receive a 'high' pulse from one of its
    inputs.

    The `flag` attribute is raised to True when all the
    inputs of the gatekeeper have sent a 'high' pulse
    at least once.

    The "gatekeeper" is the conjunction module controlling
    the activation of the final 'rx' module.
    """

    def __init__(self, gatekeeper, gatekeeper_inputs):
        self.flag = False
        self.gatekeeper = gatekeeper
        self.inputs = gatekeeper_inputs
        self.presses = 0
        self.nb_presses = defaultdict(list)

    def record(self, source, destination, pulse):
        if source == 'button':
            # count button presses
            self.presses += 1
        elif (
            destination == self.gatekeeper and
            source in self.inputs and
            pulse == 'high'
        ):
            # one of the inputs of the gatekeeper has sent
            # a 'high' pulse to the gatekeeper: record
            # how many button presses were required for that
            self.nb_presses[source].append(self.presses)
            # check if the flag needs to be set
            self.flag = all(
                len(self.nb_presses[label]) > 0
                for label in self.inputs
            )


if __name__ == '__main__':

    with open(argv[1]) as file:
        for line in file:
            parse_module(line)

    Conjunction.init()
    # retrieve the label of the "gatekeeper"
    # (the conjunction module that provides input to 'rx')
    for module in Module._module_dict.values():
        if 'rx' in module.destinations:
            gatekeeper = module.label
    # retrieve the gatekeeper inputs
    gatekeeper_inputs = set(Module._module_dict[gatekeeper].state.keys())
    # add a `GatekeeperMonitor` to the recorders
    Module._recorders.add(
        (monitor := GatekeeperMonitor(gatekeeper, gatekeeper_inputs))
    )

    button = Button()
    # keep pressing the button until the monitor flag is raised,
    # i.e. until all the inputs to the gatekeeper has sent a 'high'
    # pulse at least once
    while not monitor.flag:
        button.press()

    # note down how many pulses it took for each gatekeeper input
    # to send a 'high' pulse once
    periods = list(
        presses[0]
        for presses in monitor.nb_presses.values()
    )
    # each gatekeeper input will send a 'high' pulse periodically,
    # and now we know what that period is for each gatekeeper input:
    # in order for all gatekeeper inputs to send a 'high' pulse
    # *simultaneously*, these periods will need to synchronise,
    # i.e. we need their least common multiple
    print(periods)
    print(math.lcm(periods))
