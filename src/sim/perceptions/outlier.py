# -*- coding: utf-8 -*-
from ..utils import normalize_angle
from .perception import Perception


def mean_orientation(pop):
    """Compute the mean orientation of the given population.

    Args:
        pop (list<Individual>): The population to study.

    Returns:
        float: The mean orientation of the population (in radians).

    """
    angle_sum = 0.0
    for ind in pop:
        angle_sum += normalize_angle(ind.angle)
    return angle_sum / len(pop)


class Outlier(Perception):
    """The class implements a outlier based perception of the neighbors.

    If there is an outlier, only the individual maximizing the difference to the group is perceived, otherwise,
    the whole group is perceived.

    """

    def __init__(self, diff_threshold, border, perception):
        """Build a new outlier filter.

        Args:
            diff_threshold (float): The threshold difference to the mean to tell that an individual is an outlier (in radians).
            border (Border): The borders of the environment.
            perception (Perception): The wrapped perception.

        """
        super().__init__(border, perception)
        self.diff_threshold = diff_threshold
        """float: The threshold difference to the mean to tell that an individual is an outlier (in radians)."""

    def _filter(self, ind, pop):
        mean_ori = mean_orientation(pop)
        max_diff = 0.0
        outlier = None
        # Identify an outlier
        for ind_pop in pop:
            angular_diff = abs(normalize_angle(ind_pop.angle - mean_ori))
            if angular_diff > max_diff and ind_pop is not ind:
                max_diff = angular_diff
                outlier = ind_pop
        # List the outlier if it exists otherwise the whole population
        return [outlier] if outlier else pop
