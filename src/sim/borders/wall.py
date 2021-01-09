# -*- coding: utf-8 -*-
import numpy as np

from .border import Border


class Wall(Border):
    """The class implements an wall border.

    Wrapping clips the point in the rectangular area.

    """

    def wrap(self, point2d):
        half_len = self.length / 2
        return np.clip(point2d, self.origin - half_len, self.origin + half_len)

    def vector(self, point2d_from, point2d_to):
        return point2d_to - point2d_from
