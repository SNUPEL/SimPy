"""
Movie Ticket Purchasing Simulation

Model description:
 - This code simulates the process of moviegoers trying to purchase tickets at a theater using the SimPy library.
 - The simulation models a movie theater with a limited number of tickets for several movies.
 - Moviegoers arrive randomly and attempt to purchase tickets. If tickets are sold out, they leave the queue.
 - The simulation also tracks when movies sell out and the number of customers who leave the queue when unable to purchase tickets.

Function description:
 - moviegoer(env, movie, num_tickets, theater)
    Represents the process of a moviegoer attempting to buy tickets. The process handles cases where tickets are sold out or not enough tickets are available.
 - customer_arrivals(env, theater)
    Simulates the arrival of new moviegoers at the theater at random intervals.
 - Theater (namedtuple)
    A data structure that holds the state of the theater, including the ticket counter, available tickets, sold-out events, and customer statistics.

Execution procedure
    The simulation environment is initialized, and the theater is set up with a limited number of tickets for each movie.
    The simulation runs for 120 minutes, generating customers and processing their ticket purchase attempts.
    After the simulation, results are printed showing when each movie sold out and how many customers left the queue without buying tickets.
"""

import collections
import random

import simpy


RANDOM_SEED = 42
TICKETS = 50  # Number of tickets per movie
SIM_TIME = 120  # Simulate until


def moviegoer(env, movie, num_tickets, theater):
    """A moviegoer tries to by a number of tickets (*num_tickets*) for
    a certain *movie* in a *theater*.

    If the movie becomes sold out, she leaves the theater. If she gets
    to the counter, she tries to buy a number of tickets. If not enough
    tickets are left, she argues with the teller and leaves.

    If at most one ticket is left after the moviegoer bought her
    tickets, the *sold out* event for this movie is triggered causing
    all remaining moviegoers to leave.

    """
    with theater.counter.request() as my_turn:
        # Wait until our turn or until the movie is sold out
        result = yield my_turn | theater.sold_out[movie]

        # Check if it's our turn or if movie is sold out
        if my_turn not in result:
            theater.num_renegers[movie] += 1
            return

        # Check if enough tickets left.
        if theater.available[movie] < num_tickets:
            # Moviegoer leaves after some discussion
            yield env.timeout(0.5)
            return

        # Buy tickets
        theater.available[movie] -= num_tickets
        if theater.available[movie] < 2:
            # Trigger the "sold out" event for the movie
            theater.sold_out[movie].succeed()
            theater.when_sold_out[movie] = env.now
            theater.available[movie] = 0
        yield env.timeout(1)


def customer_arrivals(env, theater):
    """Create new *moviegoers* until the sim time reaches 120."""
    while True:
        yield env.timeout(random.expovariate(1 / 0.5))

        movie = random.choice(theater.movies)
        num_tickets = random.randint(1, 6)
        if theater.available[movie]:
            env.process(moviegoer(env, movie, num_tickets, theater))


Theater = collections.namedtuple('Theater', 'counter, movies, available, '
                                            'sold_out, when_sold_out, '
                                            'num_renegers')


# Setup and start the simulation
print('Movie renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Create movie theater
counter = simpy.Resource(env, capacity=1)
movies = ['Avatar', 'Top Gun', 'Avengers']
available = {movie: TICKETS for movie in movies}
sold_out = {movie: env.event() for movie in movies}
when_sold_out = {movie: None for movie in movies}
num_renegers = {movie: 0 for movie in movies}
theater = Theater(counter, movies, available, sold_out, when_sold_out,
                  num_renegers)

# Start process and run
env.process(customer_arrivals(env, theater))
env.run(until=SIM_TIME)

# Analysis/results
for movie in movies:
    if theater.sold_out[movie]:
        print('Movie "%s" sold out %.1f minutes after ticket counter '
              'opening.' % (movie, theater.when_sold_out[movie]))
        print('  Number of people leaving queue when film sold out: %s' %
              theater.num_renegers[movie])