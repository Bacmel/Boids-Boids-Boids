# -*- coding: utf-8 -*-

import numpy as np

from src import BOID_NOSE_LEN, BOID_TURN_SPEED, BOID_VEL
from src.utils import normalize_angle, unit_vector


class Boid:
    def __init__(self, color, pos, angle=0):
        """Constructor of Boid.

        Args:
            color (Color): color for canvas visualisation.
            pos (numpy.ndarray): Initial position.
            angle (float, optional): Initial orientation.

        """
        self.pos = np.array(pos, dtype="float")
        self.angle = normalize_angle(angle)
        self.color = color

    @property
    def dir(self):
        """Direction property of the Boid.
        
        Returns:
            numpy.ndarray: unity vector of the boid's direction.

        """
        return unit_vector(normalize_angle(self.angle))

    @property
    def vel(self):
        """Velocity property of the Boid.
        
        Returns:
            numpy.ndarray: velocity vector of the boid.

        """
        return BOID_VEL * self.dir

    def turn_by(self, dangle, dt):
        """Movement by reference speed.

        Args:
            dangle (float): Reference speed (in radians).
            dt (float): simulation time step (in seconds).

        """
        # Don't turn too fast
        self.angle += np.clip(dangle, -dt * BOID_TURN_SPEED, dt * BOID_TURN_SPEED)

        # Keep angle in range [0, 2pi)
        self.angle = normalize_angle(self.angle)

    def turn_to(self, angle, dt):
        """Turn to the desired angle.

        Args:
            angle (float): The desired orientation (in radians).
            dt (float): The simulation time step (in seconds).

        """

        a = normalize_angle(angle - self.angle)
        self.turn_by(a, dt)

    def draw(self, canvas):
        """Draw on the canvas.

        Draw this particle as an arrow.

        Args:
            canvas (Canvas): Graphical object.

        """
        tip = self.pos + BOID_NOSE_LEN * self.dir
        left = self.pos + BOID_NOSE_LEN / 2 * unit_vector(self.angle + 2 * np.pi / 3)
        right = self.pos + BOID_NOSE_LEN / 2 * unit_vector(self.angle - 2 * np.pi / 3)
        canvas.draw_poly([tip, left, self.pos, right], self.color)

    def tick(self, dt):
        """Update function.

        Update the position wrt. the velocity.

        Args:
            dt (float): simulation time step.

        """
        self.pos += self.vel * dt
