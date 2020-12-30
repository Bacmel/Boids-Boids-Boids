from math import pi
import os
import time

import numpy as np
from pandas import DataFrame


def save(data_frame, name=None, destination="data"):
    """Save the frame of data.

    Args:
        data_frame (DataFrame): The frame of data to save.
        name (str): The file name (if None, then the time is used).
        destination (str): The destination folder.
    """
    if not os.path.exists(destination):
        os.mkdir(destination)
    path = "{}/{}.csv".format(destination, name if name else str(time.time()))
    data_frame.to_csv(path)


def normalize_angle(angle):
    """Normalize the given angle to lie in [-pi, pi[.

    Args:
        angle (float): The angle (in radians).

    Returns:
        float: The normalized angle (in radians).
    """
    normalized_angle = angle
    two_pi = 2 * pi
    while normalized_angle < -pi:
        normalized_angle += two_pi
    while normalized_angle >= pi:
        normalized_angle -= two_pi
    return normalized_angle


def unit_vector(orientation):
    """Create a unit vector from its orientation.

    Args:
        orientation (float): The orientation of the vector (in radians).

    Returns:
        The unit vector from its orientation.
    """
    return np.array([np.cos(orientation),
                     np.sin(orientation)],
                    dtype="float").reshape(-1, 1)


def angle(x):
    """Compute the angle from the X axis to the given vector.

    Args:
        x (numpy.ndarray): The given 2D vector.

    Returns:
        float: The angle from the X axis to the given vector (in radians).
    """
    return np.arctan2(x[1], x[0])


def normalize(x):
    """Normalize the given vector.

    If the given vector is close to (0,0), then it is returned.

    Args:
        x (numpy.ndarray): The given 2D vector.

    Returns:
        numpy.ndarray: The normalized vector.
    """
    return x if np.allclose(x, 0) else x / np.linalg.norm(x)
