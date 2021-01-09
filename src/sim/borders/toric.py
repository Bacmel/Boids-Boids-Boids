# -*- coding: utf-8 -*-
import numpy as np

from .border import Border


class Toric(Border):
    """The class implements a toric world.

    The vector method perform its computation wrt. the toric propriety.

    """

    def wrap(self, point2d):
        return self._wrap_centered(self.origin, point2d)

    def vector(self, point2d_from, point2d_to):
        return self._wrap_centered(point2d_from, point2d_to) - point2d_from

    def _wrap_centered(self, center, point):
        relative_point = point - center
        size = np.array([self.length[0] / 2, self.length[1] / 2])
        return center + (relative_point + size) % (2 * size) - size
