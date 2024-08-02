"""
Fuel Station Simulation with a Container resource

Model description:
 - This simulation models a fuel station where cars arrive, refuel, and then leave. The station has a limited fuel supply, which is periodically replenished by a fuel tank process.
 - The simulation tracks cars arriving at intervals, using fuel from the station, and ensures the station is refueled when necessary.

Class and function description:
 - Fuel_station Class
    __init__(self, env, charging_duration, IAT, station): Initializes the fuel station with the environment, charging duration, inter-arrival time (IAT), and station's fuel container.
    run(self): Starts the fuel tank refilling process and manages the arrival of cars.
    car(self, car_index): Simulates each car's arrival, fuel consumption, and departure.
    fuel_tank(self): Periodically checks and refills the fuel station to ensure it has enough fuel.

Execution procedure:
    The simulation environment and fuel station container are initialized.
    A Fuel_station object is created, and the simulation runs for 15 time units, showing car arrivals, refueling actions, and station refueling operations.
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
        self.env.process(self.fuel_tank())
        for _ in range(4):
            car_index += 1
            self.env.process(self.car(car_index))
            yield self.env.timeout(self.IAT)

    def car(self, car_index):
        print('{0} arriving at'.format(car_index), self.env.now)
        yield self.station.get(40)

        print('{0} starting to charge at'.format(car_index), self.env.now)
        print('{0} fuel left at'.format(self.station.level), self.env.now)
        yield self.env.timeout(self.charging)
        print('{0} leaving the station at'.format(car_index), self.env.now)

    def fuel_tank(self):
        while True:
            fuel_need = self.station.capacity - self.station.level
            if fuel_need>0:
                self.station.put(fuel_need)
            yield self.env.timeout(4)


env = simpy.Environment()
station = simpy.Container(env, capacity=100)
charging_duration =5
IAT = 2

fuel_station = Fuel_station(env, charging_duration, IAT, station)
env.run(15)