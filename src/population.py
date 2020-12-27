from random import choice, random

import numpy as np

from src import Boid, PALETTE
from src.utils import normalize


class Population:
    def __init__(self, attr, orie, repu, per):
        self.pop = []  # list<Boid>
        self.roa = attr  # int
        self.roo = orie  # int
        self.ror = repu  # int
        self.perception = per  # Perception

    @property
    def cgroup(self):
        return np.mean([boid.pos for boid in self.pop])

    @property
    def dgroup(self):
        return np.mean([boid.vel for boid in self.pop])

    @property
    def pgroup(self):
        return np.abs(self.dgroup)

    @property
    def mgroup(self):
        cg = self.cgroup
        return np.abs(np.mean([boid.dist(cg) * boid.vel for boid in self.pop]))

    def add_boid(self, color=None, pos=None, angle=None, shape=None):
        color = color or choice(PALETTE["accents"])
        pos = pos or shape * (1 - 2 * random.random(shape))
        angle = angle or (2 * np.pi * random.random())
        self.pop.append(Boid(color, pos, angle))

    def tick(self, dt):
        # calculate new directions
        angles = []
        for boid in self.pop:
            angles.append(self.reorient(boid))

        for boid, angle in zip(self.pop, angles):
            boid.turn_to(angle, dt)
            boid.tick(dt)

    def draw(self, canvas):
        for boid in self.pop:
            boid.draw(canvas)
        bgroup = Boid("pink", self.cgroup, _angle(self.dgroup))
        bgroup.draw

    def reorient(self, boid):
        """
        calculates the new direction of the boid with 3 rules: cohesion,
        seperation, alignment
        """
        # get nearby boids
        nearby = self.perception.detect(boid, self.pop)

        des_a = np.array((0, 0), dtype="float")  # attraction
        des_o = np.array((0, 0), dtype="float")  # orientation
        des_r = np.array((0, 0), dtype="float")  # repulsion
        des_dir = np.array(None, dtype="float")  # direction

        # calculate all three forces if there are any boids nearby
        if len(nearby) != 0:
            for _, other in enumerate(nearby):
                diff = other.pos - boid.pos
                dist = other.dist(boid.pos)
                if dist <= self.ror:  # repulsion
                    des_r -= diff / abs(diff)
                elif dist <= self.roo:  # orientation
                    des_o += normalize(other.vel)
                else:  # attraction
                    des_a += diff / abs(diff)

        if not np.allclose(des_r, 0):
            des_dir = np.append(des_dir, des_r)
        if not np.allclose(des_o, 0):
            des_dir = np.append(des_dir, des_o)
        if not np.allclose(des_a, 0):
            des_dir = np.append(des_dir, des_a)
        # sum them up and if its not zero return it
        angle = np.mean(des_dir, axis=0)
        if np.allclose(angle, 0):
            return boid.angle
        else:
            return angle(angle)

    def store_data(self, df, df2):
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
