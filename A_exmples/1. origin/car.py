"""
Car Simulation with SimPy

Model description:
 - This code simulates the behavior of a car alternating between driving and parking using the SimPy library.
 - The car drives for a specified duration, then parks for another specified duration, continuously cycling through these states.
 - The simulation prints the current state (driving or parking) and the simulation time at which each state begins.

Class and function description:
 - Car Class
    __init__(self, env, parking_duration, trip_duration): Initializes the car with specified parking and driving durations.
    run(self): Defines the main loop where the car alternates between driving and parking.

Execution procedure
    Initializes the simulation environment with env = simpy.Environment().
    A Car object is created with specific durations, and the simulation runs for 15 time units using env.run(until=15).
"""

import simpy

class Car():
    def __init__(self, env, parking_duration, trip_duration):
        self.env = env
        self.parking = parking_duration
        self.driving = trip_duration
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Start driving at', self.env.now)
            yield self.env.timeout(self.driving)

            print('Start parking at', self.env.now)
            yield self.env.timeout(self.parking)


env = simpy.Environment()
parking_duration = 5
trip_duration = 2

car = Car(env, parking_duration, trip_duration)
env.run(until=15)