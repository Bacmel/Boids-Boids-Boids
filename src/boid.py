# -*- coding: utf-8 -*-

from random import choice
from src import BOID_VEL, BOID_NOSE_LEN, BOID_TURN_SPEED, PALETTE
from src.utils import unit_vector
import numpy as np


class Boid:
    def __init__(self, color, pos, angle=0):
        """Constructor of Boid.

        Args:
            color (Color): color for canvas visualisation.
            pos (numpy.ndarray): Initial position.
            angle (float, optional): Initial orientation.

        """
        self.pos = np.array(pos, dtype="float")
        self.angle = angle % (2 * np.pi)
        self.color = color

    @property
    def dir(self):
        """Direction proprety of the Boid.
        
        Returns:
            numpy.ndarray: unity vector of the boid's direction.

        """
        return unit_vector(self.angle)

    @property
    def vel(self):
        """Velocity proprety of the Boid.
        
        Returns:
            numpy.ndarray: velocity vector of the boid.

        """
        return BOID_VEL * self.dir

    def dist(self, pos):
        """Distance from pos to Boid.

        Args:
            pos (numpy.array): Reference position.
        
        Returns:
            numpy.array: distance between them.

        """
        return np.linalg.norm(self.pos - pos)

    def turn_by(self, dangle, dt):
        """Movement by reference speed.

        Args:
            dangle (float): Reference speed.
            dt (float): simulation time step.

        """
        # dont turn too fast
        self.angle += np.clip(dangle, -dt * BOID_TURN_SPEED, dt * BOID_TURN_SPEED)

        # keep angle in range [0, 2pi)
        self.angle %= 2 * np.pi

    def turn_to(self, angle, dt):
        """Movement by reference position.

        Args:
            angle (float): Reference position.
            dt (float): simulation time step.

        """
        a = (angle - self.angle) % (2 * np.pi)
        b = -(-a % (2 * np.pi))
        self.turn_by(min(a, b, key=lambda x: np.abs(x)), dt)

    def draw(self, canvas):
        """Draw function.

        Args:
            canvas (Canvas): Graphical object.

        """
        tip = self.pos + BOID_NOSE_LEN * self.dir
        left = self.pos + BOID_NOSE_LEN / 2 * unit_vector(self.angle + 2 * np.pi / 3)
        right = self.pos + BOID_NOSE_LEN / 2 * unit_vector(self.angle - 2 * np.pi / 3)
        canvas.draw_poly([tip, left, self.pos, right], self.color)

    def tick(self, dt):
        """Update function.

        Args:
            dt (float): simulation time step.

        """
        self.pos += self.vel * dt