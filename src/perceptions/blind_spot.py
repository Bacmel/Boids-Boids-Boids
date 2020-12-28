from math import atan2, pi

from src.utils import normalize_angle
from .perception import Perception


class BlindSpot(Perception):
    """The class implements a blind spot in the perception of the neighbors."""

    def __init__(self, bisector, opening, border, perception=None):
        """Build a new blind spot.

        Args:
            bisector (float): The bisector of the cone (in radians).
            opening (float): The opening of the cone (in radians). Must be positive and inferior to pi.
            border (Border): The border of the environment.
            perception (Perception): The wrapped perception.
        """
        super().__init__(border, perception)
        assert 0 < opening <= pi
        assert -pi <= bisector < pi
        self.bisector = bisector
        self.opening = opening

    def _filter(self, ind, pop):
        filtered_pop = list()
        orientation = ind.dir
        for ind_pop in pop:
            # Compute the relative orientation to the current individual
            relative_dir = self.border.vector(ind.pos, ind_pop.pos)
            diff_orientation = relative_dir - orientation
            angle = atan2(diff_orientation[1], diff_orientation[0])
            if (
                ind_pop is not ind
                and abs(normalize_angle(angle - self.bisector)) > self.opening
            ):
                filtered_pop.append(ind_pop)  # The individual is not in the blind spot
        return filtered_pop
