import random


class InfectionController:

    def __init__(self, num_individuals):
        self.current_healthy = num_individuals
        self.current_infected = 0
        self.current_dead = 0
        self.current_removed = 0
        self.individuals = None

    def set_individuals(self, individuals):
        self.individuals = individuals

    def start_infection(self, num=1):
        if self.individuals is not None:
            inds = random.choices(self.individuals, k=num)
            return inds
        else:
            return None