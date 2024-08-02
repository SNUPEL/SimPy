"""
Bank Customer Reneging Simulation

Model description:
 - This code simulates a bank scenario where customers arrive, wait for service, and either get served or leave (renege) due to impatience.
 - Customers are generated at random intervals and request service from a bank counter with limited capacity.
 - If a customer waits longer than their patience allows, they leave without being served; otherwise, they are served and then leave.
 - The simulation runs for a specified duration, capturing customer behavior under different conditions.

Class and function description:
 - source(env, number, interval, counter)
    Generates customers at random intervals and starts their service process.

 - customer(env, name, counter, time_in_bank)
    Simulates a customer arriving, waiting for service, getting served, or reneging if they wait too long.

Main Simulation Execution
     Initializes the simulation environment, sets up the bank counter resource, generates customers, and runs the simulation for 200 time units.
"""

import random

import simpy


RANDOM_SEED = 30
NEW_CUSTOMERS = 500  # Total number of customers
INTERVAL_CUSTOMERS = 3.0  # Generate new customers roughly every x min
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run(200)
