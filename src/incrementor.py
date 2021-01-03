import numpy as np
from src import Universe, Population

class Incrementor:
    def __init__(self, inf_bound, increment, sup_bound, step_duration):
        self.inf_bound = inf_bound
        self.increment = increment
        self.sup_bound = sup_bound
        self.step_duration = step_duration
        self.count = 0
        self.stepper = inf_bound
    
    def next(self, universe):
        """
        Preapre the simulation next step.
        """
        self.count += 1
        if self.count == self.step_duration:
            self.count = 0
            self.stepper += self.increment
            if self.stepper >= self.sup_bound - self.increment:
                self.increment = -self.increment
            if self.stepper >= self.inf_bound:
                universe.boids.roo = self.stepper
