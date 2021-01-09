# -*- coding: utf-8 -*-
class Incrementor:
    def __init__(self, inf_bound, increment, sup_bound, step_duration):
        """Build a new Incrementor.

        Args:
            inf_bound (int or float): The inf bound (included).
            increment (int or float):  The step increment.
            sup_bound (int or float): The sup bound (excluded).
            step_duration (int): The number of call to next() to change the value.
        """
        self.inf_bound = inf_bound
        self.increment = increment
        self.sup_bound = sup_bound
        self.step_duration = step_duration
        self.count = 0
        self.stepper = inf_bound

    @property
    def is_rising(self):
        """Whether the value will rise or not at the next change.

        Returns:
            bool: Whether the value will rise or not at the next change.

        """
        return self.increment > 0

    @property
    def will_change(self):
        """Whether the value will change or not at the next call to next().

        Returns:
            bool: Whether the value will change or not at the next call to next().

        """
        return self.count + 1 == self.step_duration

    def next(self):
        """Prepare the next step of the simulation.

        Returns:
            The current value.
        """
        value = self.stepper
        self.count += 1

        if self.count == self.step_duration:
            self.count = 0
            self.stepper += self.increment

            # Reverse the increment direction when the sup bound is reached
            if self.stepper >= self.sup_bound - self.increment:
                self.increment = -self.increment

            # Ensure the value is greater than the inf bound
            if self.stepper < self.inf_bound:
                value = self.inf_bound

        return value