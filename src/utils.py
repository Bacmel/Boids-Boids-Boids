from math import pi
import numpy as np


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


def _unit_vector(angle):
    return np.array([np.cos(angle), np.sin(angle)], dtype="float")


def _angle(x):
    return np.arctan2(x[1], x[0])


def _norm(x):
    return x if np.allclose(x, 0) else x / np.linalg.norm(x)
