"""
Fuel Station Simulation with a default Resource

Model description:
 - This simulation models a fuel station where cars arrive, wait for an available pump if necessary, charge, and then leave.
 - The station has limited capacity, meaning only a fixed number of cars can charge simultaneously.
 - Cars arrive at fixed intervals and spend a certain duration charging before they leave the station.

Class and function description:
 - Fuel_station Class
    __init__(self, env, charging_duration, IAT, station): Initializes the fuel station with the simulation environment, charging duration, inter-arrival time (IAT), and the station's resource capacity.
    run(self): Manages the arrival of cars at intervals specified by IAT and initiates their charging process.
    car(self, car_index): Simulates each car's arrival, waiting for an available pump, charging, and departure.

Execution procedure:
    The simulation environment is initialized along with the fuel station resource.
    A Fuel_station object is created, and the simulation runs until all cars have arrived and completed charging.
"""

import simpy

class Fuel_station():
    def __init__(self, env, charging_duration, IAT, station):
        self.env = env
        self.charging = charging_duration
        self.IAT = IAT
        self.station = station

        self.action = env.process(self.run())

    def run(self):
        car_index = 0
        for _ in range(4):
            car_index += 1
            self.env.process(self.car(car_index))
            yield self.env.timeout(self.IAT)

    def car(self, car_index):
        print('{0} arriving at'.format(car_index), self.env.now)
        with self.station.request() as req:
            yield req
            print('{0} starting to charge at'.format(car_index), self.env.now)
            yield self.env.timeout(self.charging)
            print('{0} leaving the station at'.format(car_index), self.env.now)


env = simpy.Environment()
station = simpy.Resource(env, capacity=2)
charging_duration =5
IAT = 2

fuel_station = Fuel_station(env, charging_duration, IAT, station)
env.run()