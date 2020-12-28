from numpy.linalg import norm

from .perception import Perception


class Range(Perception):
    """The class implements a range based perception of the neighbors."""

    def __init__(self, perception_range, border, perception=None):
        """Build a new Range perception.

        Args:
            perception_range (float): The maximum distance to a detected neighbors (in units).
            border (Border): The border of the environment.
            perception (Perception): The wrapped perception.
        """
        super().__init__(border, perception)
        self.perception_range = perception_range

    def _filter(self, ind, pop):
        return [
            pop_ind
            for pop_ind in pop
            if pop_ind is not ind
            and norm(self.border.vector(ind.pos, pop_ind.pos)) < self.perception_range
        ]
