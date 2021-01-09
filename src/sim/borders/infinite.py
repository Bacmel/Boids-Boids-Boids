# -*- coding: utf-8 -*-
from .border import Border


class Infinite(Border):
    """The class implements an infinite border.

    Wrapping a vector does not change it.
    The length and center of the area are not used.

    """

    def wrap(self, point2d):
        return point2d

    def vector(self, point2d_from, point2d_to):
        return point2d_to - point2d_from
