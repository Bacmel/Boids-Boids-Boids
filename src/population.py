from random import choice, random

import numpy as np

from src import Boid, PALETTE
from src.utils import normalize, angle


class Population:
    def __init__(self, roa, roo, ror, per, std):
        """Population Constructor.
        
        Args:
            roa (int): Rayon of attraction.
            roo (int): Rayon of orientation.
            ror (int): Rayon of repulsion.
            per (Perception): Perception object of the population.
            std (float): standard deviation for gaussian noise

        """
        self.pop = []  # list<Boid>
        self.roa = roa  # int
        self.roo = roo  # int
        self.ror = ror  # int
        self.perception = per  # Perception
        self.std = std  # float

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
        return np.mean([boid.dir for boid in self.pop])

    @property
    def pgroup(self):
        """Group Polarization.
        
        Returns:
            float: Group polarization value.

        """
        return np.linalg.norm(self.dgroup)

    @property
    def mgroup(self):
        """Group Momentum.
        
        Returns:
            float: Group momentum value.

        """
        cg = self.cgroup
        m = np.array([[]])
        for boid in self.pop:
            r_ic = normalize(self.perception.border.vector(cg, boid.pos))
            m_ic = np.cross(r_ic, boid.dir)
            m = np.append(m, [m_ic], axis=0)
        return np.linalg.norm(np.mean(m))

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

        Compute new direction and update the position of each boid.

        Args:
            dt (float): simulation time step.

        """
        # compute new directions
        angles = []
        for boid in self.pop:
            angles.append(self.reorient(boid))

        # update positions
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

        des_a = np.array((0, 0), dtype="float")  # desired attraction
        des_o = np.array((0, 0), dtype="float")  # desired orientation
        des_r = np.array((0, 0), dtype="float")  # desired repulsion
        des_dir = np.array([], dtype="float")  # desired direction
        nb_a = 0  # number of boid in attraction zone
        nb_o = 0  # number of boid in orientation zone
        nb_r = 0  # number of boid in repulsion zone
        # calculate all three forces if there are any boids nearby
        if len(nearby) != 0:
            for other in nearby:
                diff = self.perception.border.vector(other.pos, boid.pos)
                dist = np.linalg.norm(diff)
                if dist <= self.ror:  # repulsion
                    des_r -= diff / dist
                    nb_r += 1
                elif dist <= self.roo:  # orientation
                    des_o += other.dir
                    nb_o += 1
                elif dist <= self.roa:  # attraction
                    des_a += diff / dist
                    nb_a += 1

        if nb_r > 0:
            des_dir = des_r
        elif nb_o > 0:
            if nb_a == 0:
                des_dir = des_o
            else:
                des_dir = np.mean([des_o, des_a], axis=0)
        elif nb_a > 0:
            des_dir = des_a
        else:
            des_dir = boid.dir

        # sum them up and if its not zero return it
        if np.allclose(des_dir - boid.dir, 0):
            new_angle = boid.angle
        else:
            new_angle = angle(des_dir)
        new_angle += random.gauss(0, self.std)
        return new_angle

    def store_data(self, df, df2):
        """store data.

        Store data at instant t.

        Args:
            df (pandas.Dataframe): group data.
            df2 (pandas.Dataframe): boid data.

        Returns:
            [pandas.Dataframe, pandas.Dataframe]: New data.

        """
        row = {
            "cgroup": self.cgroup,
            "dgroup": self.dgroup,
            "pgroup": self.pgroup,
            "mgroup": self.mgroup,
            "roa": self.roa,
            "roo": self.roo,
            "ror": self.ror,
        }
        df = df.append(row, ignore_index=True)
        row2 = {}
        for i in range(len(self.pop)):
            pos = self.pop[i].pos
            row2["x" + str(i)] = pos[0]
            row2["y" + str(i)] = pos[i]
        df = df.append(row2, ignore_index=True)
        return [df, df2]
