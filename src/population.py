from random import choice, random

import numpy as np

from src import Boid, PALETTE
from src.utils import normalize, angle


class Population:
    def __init__(self, roa, roo, ror, per):
        """Population Constructor.
        
        Args:
            roa (int): Rayon of attraction.
            roo (int): Rayon of orientation.
            ror (int): Rayon of repulsion.
            per (Perception): Perception object of the population.

        """
        self.pop = []  # list<Boid>
        self.roa = roa  # int
        self.roo = roo  # int
        self.ror = ror  # int
        self.perception = per  # Perception

    @property
    def cgroup(self):
        """Group Center.
        
        Returns:
            numpy.ndarray: Group center position.

        """
        return np.mean([boid.pos for boid in self.pop])

    @property
    def dgroup(self):
        """Group Direction.
        
        Returns:
            numpy.ndarray: Group direction vector.

        """
        return np.mean([boid.vel for boid in self.pop])

    @property
    def pgroup(self):
        """Group Polarization.
        
        Returns:
            float: Group polarization value.

        """
        return np.abs(self.dgroup)

    @property
    def mgroup(self): # WARNING : DON'T USE Boid.dist
        """Group Momentum.
        
        Returns:
            float: Group momentum value.

        """
        cg = self.cgroup
        return np.abs(np.mean([boid.dist(cg) * boid.vel for boid in self.pop]))

    def add_boid(self, color=None, pos=None, angle=None, shape=None):
        """Add Boid on population.

        Args:
            color (Color, optional): color for canvas visualisation.
            pos (numpy.ndarray, optional): Initial position.
            angle (float, optional): Initial orientation.
            shape (numpy.ndarray, optional): Size of the world (if pose == None).

        """
        color = color or choice(PALETTE["accents"])
        pos = pos or shape * (1 - 2 * np.random.random(shape))
        angle = angle or (2 * np.pi * random())
        self.pop.append(Boid(color, pos, angle))

    def tick(self, dt):
        """Update function.

        Update the position of each boid.

        Args:
            dt (float): simulation time step.

        """
        # calculate new directions
        angles = []
        for boid in self.pop:
            angles.append(self.reorient(boid))

        for boid, angle in zip(self.pop, angles):
            boid.turn_to(angle, dt)
            boid.tick(dt)

    def draw(self, canvas):
        """Draw on the canvas.

        Draw the population.

        Args:
            canvas (Canvas): Graphical object.

        """
        for boid in self.pop:
            boid.draw(canvas)
        bgroup = Boid("FFC0CB", self.cgroup, angle(self.dgroup))
        bgroup.draw(canvas)

    def reorient(self, boid):
        """Calcul new orientation of the boid.

        calculates the new direction of the boid with 3 rules: attraction,
        orientation, orientation.

        Args:
            boid (Boid): Boid.

        Returns:
            float: new orientation.

        """
        # get nearby boids
        nearby = self.perception.detect(boid, self.pop)

        des_a = np.array((0, 0), dtype="float")  # attraction
        des_o = np.array((0, 0), dtype="float")  # orientation
        des_r = np.array((0, 0), dtype="float")  # orientation
        des_dir = np.array([], dtype="float")  # direction

        # calculate all three forces if there are any boids nearby
        if len(nearby) != 0:
            for _, other in enumerate(nearby):
                diff = other.pos - boid.pos
                dist = other.dist(boid.pos) # WARNING : DON'T USE Boid.dist
                if dist <= self.ror:  # repulsion
                    des_r -= diff / abs(diff)
                elif dist <= self.roo:  # orientation
                    des_o += normalize(other.vel)
                else:  # attraction
                    des_a += diff / abs(diff)

        if not np.allclose(des_r, 0):
            des_dir = np.append(des_dir, des_r)
        else: 
            if not np.allclose(des_o, 0):
                des_dir = np.append(des_dir, des_o)
            if not np.allclose(des_a, 0):
                des_dir = np.append(des_dir, des_a)
        # sum them up and if its not zero return it
        orien = np.mean(des_dir, axis=0)
        if np.allclose(orien, 0):
            return boid.angle
        else:
            return angle(orien)

    def store_data(self, df, df2):
        """store data.

        Store data at instant t.

        Args:
            df (pandas.Dataframe): group data.
            df2 (pandas.Dataframe): boid data.

        Returns:
            [pandas.Dataframe, pandas.Dataframe]: New data.
        """
        row = {"cgroup": self.cgroup, "dgroup": self.dgroup, "pgroup": self.pgroup, "mgroup": self.mgroup,
               "roa": self.roa, "roo": self.roo, "ror": self.ror}
        df = df.append(row, ignore_index=True)
        row2 = {}
        for i in range(len(self.pop)):
            pos = self.pop[i].pos
            row2["x" + str(i)] = pos[0]
            row2["y" + str(i)] = pos[i]
        df = df.append(row2, ignore_index=True)
        return [df, df2]
