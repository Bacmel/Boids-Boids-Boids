# -*- coding: utf-8 -*-
from numpy.linalg import norm

from .perception import Perception


class KNN(Perception):
    """The class implements a k-nearest neighbors perception of the neighbors."""

    def __init__(self, k, border, perception):
        """Build a new k-nearest neighbors filter.

        Args:
            k (int): The maximum number of neighbors.
            border (Border): The borders of the environment.
            perception (Perception): The wrapped perception.

        """
        super().__init__(border, perception)
        self.k = k

    def _filter(self, ind, pop):
        dpop = list()
        for ind_pop in pop:
            relative_pos = self.border.vector(ind.pos, ind_pop.pos)
            if ind_pop is not ind:
                dpop.append((norm(relative_pos), ind_pop))
        dpop.sort(key=lambda elem: elem[0])
        knn = dpop[: min(self.k, len(dpop))]
        return [ind for d, ind in knn]
