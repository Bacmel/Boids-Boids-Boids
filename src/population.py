import random
import numpy as np
import numpy.random as np_rand

from src import Boid, PALETTE
from src.utils import normalize, angle


class Population:
    def __init__(self, roa, roo, ror, per, bias, std):
        """Population Constructor.

        Args:
            roa (float): The radius of attraction.
            roo (float): The radius of orientation.
            ror (float): The radius of repulsion.
            per (Perception): The perception of the population.
            bias (float): The biais in the decision process (in radians).
            std (float): The standard deviation in the decision process (in radians).

        """
        self.pop = []  # list[Boid]
        self.roa = roa  # float
        self.roo = roo  # float
        self.ror = ror  # float
        self.perception = per  # Perception
        self.bias = bias  # float
        self.std = std  # float

    @property
    def cgroup(self):
        """Compute the group center.

        Returns:
            numpy.ndarray: The position of the group center.

        """
        mean = np.mean([boid.pos for boid in self.pop], axis=0)
        # print(mean)
        return mean

    @property
    def dgroup(self):
        """Compute the group direction.

        Returns:
            numpy.ndarray: The group direction.

        """
        return np.mean([boid.dir for boid in self.pop], axis=0)

    @property
    def pgroup(self):
        """Compute the group polarization.

        Returns:
            float: The group polarization value.

        """
        return np.linalg.norm(self.dgroup)

    @property
    def mgroup(self):
        """Compute the group momentum.

        Returns:
            float: The group momentum.

        """
        cg = self.cgroup
        m = np.array([[]])
        for boid in self.pop:
            r_ic = normalize(self.perception.border.vector(cg, boid.pos))
            m_ic = np.cross(r_ic, boid.dir)
            m = np.append(m, [m_ic], axis=0)
        return np.linalg.norm(np.mean(m))

    def add_boid(self, color=None, pos=None, angle=None, border=None):
        """Add a boid to this population.

        Args:
            color (Color, optional): color for canvas visualisation.
            pos (numpy.ndarray, optional): Initial position.
            angle (float, optional): Initial orientation.
            shape (numpy.ndarray, optional): Size of the world (if pose == None).

        """
        color = color or random.choice(PALETTE["accents"])
        if pos == None:
            shape = border.length
            pos = (
                border.origin + shape *
                (1 - 2 * np.random.random(shape.shape)))
        angle = angle or (2 * np.pi * random.random())
        self.pop.append(Boid(color, pos, angle))

    def tick(self, dt):
        """Update function.

        Compute new direction and update the position of every boids.

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
            boid.pos = self.perception.border.wrap(boid.pos)

    def draw(self, canvas):
        """Draw the population on the canvas.

        Ask each boid to draw itself then draw a fake boid at the mean
        position with the mean orientation.

        Args:
            canvas (Canvas): Graphical object.

        """
        for boid in self.pop:
            boid.draw(canvas)
        bgroup = Boid(0xfffff, self.cgroup, angle(self.dgroup))
        bgroup.draw(canvas)

    def reorient(self, boid):
        """Compute a new orientation for the boid.

        Calculate the new direction of the boid with 3 rules:
        - Repulsion
        - Orientation
        - Attraction

        Args:
            boid (Boid): The given boid.

        Returns:
            float: The new orientation for the given boid (in radians).

        """
        nearby = self.perception.detect(boid, self.pop)  # get nearby boids
        border = self.perception.border  # the border policy
        des_r = np.zeros((2, 1), dtype="float")  # desired repulsion
        des_o = np.zeros((2, 1), dtype="float")  # desired orientation
        des_a = np.zeros((2, 1), dtype="float")  # desired attraction
        des_dir = np.zeros((2, 1), dtype="float")  # desired direction
        nb_r = 0  # number of boid in repulsion zone
        nb_o = 0  # number of boid in orientation zone
        nb_a = 0  # number of boid in attraction zone
        # calculate all three forces if there are any boids nearby
        for other in nearby:
            diff = border.vector(boid.pos, other.pos)
            if np.allclose(diff, np.zeros((2, 1))):  # the boids are superposed
                # compute a random vector to escape
                diff = np_rand.normal(0, 1, (2, 1))
            dist = np.linalg.norm(diff)
            if dist <= self.ror:  # repulsion zone
                des_r -= diff / dist
                nb_r += 1
            elif dist <= self.roo:  # orientation zone
                des_o += other.dir
                nb_o += 1
            elif dist <= self.roa:  # attraction zone
                des_a += diff / dist
                nb_a += 1
        # choose the rule to apply
        if nb_r > 0:  # repulsion rule only
            des_dir = des_r
        elif nb_o > 0:
            if nb_a == 0:  # orientation rule only
                des_dir = des_o
            else:  # orientation and attraction rules
                des_dir = np.mean([des_o, des_a], axis=0)
        elif nb_a > 0:  # attraction rule only
            des_dir = des_a
        else:  # no decision
            des_dir = boid.dir
        # compute the new angle from the desired direction
        new_angle = angle(des_dir)
        new_angle += random.gauss(0.0, self.std)  # apply noise to the decision
        return new_angle

    def store_data(self, df, df2):
        """Store data.

        Store data at instant t.

        Args:
            df (pandas.Dataframe): group data.
            df2 (pandas.Dataframe): boid data.

        Returns:
            list[pandas.Dataframe]: New data.

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
