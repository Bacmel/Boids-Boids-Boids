from abc import ABC, abstractmethod

import numpy as np


class Border(ABC):
    def __init__(self, length, origin=np.zeros(2, 1)):
        """Build a new border.

        Args:
            length (numpy.ndarray): The vector of length.
            origin (numpy.ndarray): The center position of the environment.
        """
        self.length = length
        self.origin = origin

    @abstractmethod
    def wrap(self, point2d):
        """Wrap a vector to stay within the border.
        
        Args:
            point2d (numpy.ndarray): The point to wrap. 

        Returns:
            numpy.ndarray: The wrapped point.
        """
        pass

    @abstractmethod
    def vector(self, point2d_from, point2d_to):
        """Compute the vector that connects the given points.

        Args:
            point2d_from (numpy.ndarray): The start point.
            point2d_to (numpy.ndarray): The end point.

        Returns:
            numpy.ndarray: The vector between these point wrt. the border type.
        """
        pass
