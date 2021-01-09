class Incrementor:
    def __init__(self, inf_bound, increment, sup_bound, step_duration):
        self.inf_bound = inf_bound
        self.increment = increment
        self.sup_bound = sup_bound
        self.step_duration = step_duration
        self.count = 0
        self.stepper = inf_bound

    @property
    def is_rising(self):
        return self.increment > 0

    @property
    def will_change(self):
        return self.count+1 == self.step_duration

    def next(self, universe):
        """
        Prepare the simulation's next step.
        """
        self.count += 1
        if self.count == self.step_duration:
            self.count = 0
            self.stepper += self.increment
            if self.stepper >= self.sup_bound - self.increment:
                self.increment = -self.increment
            if self.stepper >= self.inf_bound:
                universe.pop.roo = self.stepper
