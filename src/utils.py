from math import pi


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
