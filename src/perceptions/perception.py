from abc import ABC, abstractmethod

from src import Individual


class Perception(ABC):
    def __init__(self, border, perception):
        """

        Args:
            border (Border): The borders of the environment.
            perception (Perception): The wrapped perception.
        """
        self.border = border
        self.wrapped = perception

    def detect(self, ind, pop):
        """Detect individuals from the given population around the given individual.

        Args:
            ind (Individual): The given individual.
            pop (list<Individual>): The given population.

        Returns:
            list<Individual>: The detected neighbors.
        """
        pop_filtered = pop
        if self.wrapped:
            pop_filtered = self.wrapped.detect(ind, pop)
        return self._filter(ind, pop_filtered)

    @abstractmethod
    def _filter(self, ind, pop):
        """Filter the individuals from the population that are not seen by the given individual

        Args:
            ind (Individual): The given individual.
            pop (list<Individual>): The given population.

        Returns:
            list<Individual>: The filtered population.
        """
        pass
