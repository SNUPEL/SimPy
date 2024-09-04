"""
Event Latency Simulation

Model description:
 - This code simulates the propagation delay of messages through a cable using the SimPy library.
 - A sender process generates messages at regular intervals and sends them through a cable with a specified delay.
 - A receiver process consumes these messages after they pass through the cable, accounting for the delay.

Function description:
 - Cable Class
    __init__(self, env, delay): Initializes the cable with a specified propagation delay.
    latency(self, value): Simulates the delay before the message is transmitted through the cable.
    put(self, value): Puts a message into the cable with a delay.
    get(self): Retrieves a message from the cable after the delay.
 - sender(env, cable): Simulates a process that generates and sends messages at regular intervals.
 - receiver(env, cable): Simulates a process that receives messages after they have passed through the cable.

When Useful:
    This example shows how to separate the time delay of events between processes from the processes themselves.
    When modeling physical things such as cables, RF propagation, etc.
    it would be better encapsulation to keep this propagation mechanism outside of the sending and receiving processes.
"""

import simpy


SIM_DURATION = 100


class Cable(object):
    """This class represents the propagation through a cable."""
    def __init__(self, env, delay):
        self.env = env
        self.delay = delay
        self.store = simpy.Store(env)

    def latency(self, value):
        yield self.env.timeout(self.delay)
        self.store.put(value)

    def put(self, value):
        self.env.process(self.latency(value))

    def get(self):
        return self.store.get()


def sender(env, cable):
    """A process which randomly generates messages."""
    while True:
        # wait for next transmission
        yield env.timeout(5)
        cable.put('Sender sent this at %d' % env.now)


def receiver(env, cable):
    """A process which consumes messages."""
    while True:
        # Get event for message pipe
        msg = yield cable.get()
        print('Received this at %d while %s' % (env.now, msg))


# Setup and start the simulation
print('Event Latency')
env = simpy.Environment()

cable = Cable(env, 10)
env.process(sender(env, cable))
env.process(receiver(env, cable))

env.run(until=SIM_DURATION)