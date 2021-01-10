# -*- coding: utf-8 -*-

import numpy as np

from . import BOID_NOSE_LEN
from .utils import normalize_angle, unit_vector


class Individual:
    def __init__(self, color, pos, ror, roo, roa, angle=0, speed=1.0, turning_rate=0.2):
        """Constructor of Individual.

        Args:
            color (Color): color for canvas visualisation.
            pos (numpy.ndarray): Initial position.
            angle (float, optional): Initial orientation.

        """
        self.pos = np.array(pos, dtype="float")
        """numpy.ndarray: The position (in length units)."""
        self.angle = normalize_angle(angle)
        """float: The orientation (in radians)."""
        self.color = color
        """The color to display."""
        self.speed = speed
        """float: The speed (in length units per seconds)."""
        self.turning_rate = turning_rate
        """float: The angular speed (in radians per seconds)."""
        self.ror = ror
        """float: The range of repulsion (in length units)."""
        self.roo = roo
        """float: The range of orientation (in length units)."""
        self.roa = roa
        """float: The range of attraction (in length units)."""

    @property
    def dir(self):
        """Get the unitary vector of direction.

        Returns:
            numpy.ndarray: The unitary vector of direction.

        """
        return unit_vector(normalize_angle(self.angle))

    @property
    def vel(self):
        """Get the velocity.

        Returns:
            numpy.ndarray: The velocity vector (in length units per seconds).

        """
        return self.speed * self.dir

    def turn_by(self, dangle, dt):
        """Movement from the given angular speed.

        Args:
            dangle (float): The angular variation (in radians).
            dt (float): The simulation time step (in seconds).

        """
        # Don't turn too fast
        self.angle += np.clip(dangle, -dt * self.turning_rate, dt * self.turning_rate)

        # Keep angle in range [-pi, pi)
        self.angle = normalize_angle(self.angle)

    def turn_to(self, angle, dt):
        """Turn to the desired angle.

        Args:
            angle (float): The desired orientation (in radians).
            dt (float): The simulation time step (in seconds).

        """
        a = normalize_angle(angle - self.angle)
        self.turn_by(a, dt)

    def tick(self, dt):
        """Update function.

        Update the position wrt. the velocity.

        Args:
            dt (float): simulation time step.

        """
        self.pos += self.vel * dt
