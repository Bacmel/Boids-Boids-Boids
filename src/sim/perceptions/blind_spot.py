# -*- coding: utf-8 -*-
from math import atan2, pi

from ..utils import normalize_angle
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
        """float: The direction (in radians)."""
        self.half_opening = opening / 2
        """float: The opening (in radians)."""

    def _filter(self, ind, pop):
        filtered_pop = []
        for other in pop:
            if other is ind:
                continue
            # Compute the relative orientation to the current individual
            relative_pos = self.border.vector(ind.pos, other.pos)
            abs_angle = atan2(relative_pos[1], relative_pos[0])
            relative_angle = normalize_angle(abs_angle - ind.angle)
            if abs(normalize_angle(relative_angle - self.bisector)) > self.half_opening:
                filtered_pop.append(other)  # The individual is not in the blind spot
        return filtered_pop
