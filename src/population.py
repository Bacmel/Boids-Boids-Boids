from math import cos, pi, sin
import random

import numpy as np
import numpy.linalg as lin
import numpy.random as np_rand

from src import Boid, PALETTE
from src.utils import angle, normalize


class Population:
    def __init__(self, speed=1, turning_rate=0.2, roa, roo, ror, per, std, speed_sd=None, tr_sd=None, ror_sd=None,
                 roo_sd=None, roa_sd=None):
        """Population Constructor.

        Args:
            roa (float): The radius of attraction.
            roo (float): The radius of orientation.
            ror (float): The radius of repulsion.
            per (Perception): The perception of the population.
            std (float): The standard deviation in the decision process (in radians).

        """
        self.pop = []  # list[Boid]
        self.speed = speed  # float
        self.turning_rate = turning_rate  # float
        self.roa = roa  # float
        self.roo = roo  # float
        self.ror = ror  # float
        self.perception = per  # Perception
        self.std = std  # float
        self.speed_sd = speed_sd  # float
        self.tr_sd = tr_sd  # float
        self.roo_sd = roo_sd  # float
        self.ror_sd = ror_sd  # float
        self.roa_sd = roa_sd  # float

    @property
    def cgroup(self):
        """Compute the group center.

        Returns:
            numpy.ndarray: The position of the group center.

        """
        origin = np.zeros((2, 1))
        mean = np.mean([self.perception.border.vector(origin, boid.pos) for boid in self.pop], axis=0)
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
        m = []
        for boid in self.pop:
            r_ic = normalize(self.perception.border.vector(cg, boid.pos))
            m_ic = np.cross(r_ic, boid.dir, axis=0)
            m.append(m_ic)
        m_array = np.array(m)
        m_mean = np.mean(m_array)
        return np.linalg.norm(m_mean)

    def add_boid(self, color=None, pos=None, angle=None, speed=1, turning_rate=0.2):
        """Add a boid to this population.

        Args:
            color (Color): color for canvas visualisation.
            pos (numpy.ndarray): Initial position.
            angle (float): The initial orientation.
            speed (float): The speed (in length unit per seconds).
            turning_rate (float): The maximal angular speed (in radians per seconds).
        """
        color = color or random.choice(PALETTE["accents"])
        if pos is None and angle is None:
            # Generate gaussian distribution for each parameter
            new_speed = self.speed
            new_tr = self.turning_rate
            new_ror = self.ror
            new_roo = self.roo
            new_roa = self.roa

            if self.speed_sd is not None:
                speed += random.gauss(0.0, self.speed_sd)
            if self.tr_sd is not None:
                new_tr += random.gauss(0.0, self.tr_sd)
            if self.ror_sd is not None:
                new_ror += random.gauss(0.0, self.ror_sd)
            if self.roo_sd is not None:
                new_roo += random.gauss(0.0, self.roo_sd)
            if self.roa_sd is not None:
                new_roa += random.gauss(0.0, self.roa_sd)

            # No specified pose, ensure the new boid sees another one
            for _ in range(100000):
                pos = self._random_pos(new_roa)
                angle = 2 * pi * (random.random() - 0.5)
                boid = Boid(color, pos, angle, speed=new_speed, turning_rate=new_tr, ror=new_ror, roo=new_roo,
                            roa=new_roa)
                if len(self.pop) == 0 or len(self.perception.detect(boid, self.pop)) >= 1:
                    break
            else:
                raise RuntimeError("Failed to find a valid configuration after 100 000 tries!")
        else:
            # At least one pose element is specified, no warranty
            pos = pos or self._random_pos(self.roa)
            angle = angle or (2 * pi * (random.random() - 0.5))
            boid = Boid(color, pos, angle, speed=speed, turning_rate=turning_rate, ror=self.ror, roo=self.roo,
                        roa=self.roa)
        self.pop.append(boid)

    def _random_pos(self, roa):
        border = self.perception.border
        r = self.roa * random.random()
        th = 2 * pi * (random.random() - 0.5)
        pos = np.array([[r * cos(th)], [r * sin(th)]]) + border.origin
        return border.wrap(pos)

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
            dir2other = diff / dist
            if dist <= boid.ror:  # repulsion zone
                des_r -= dir2other
                nb_r += 1
            elif dist <= boid.roo:  # orientation zone
                des_o += other.dir
                nb_o += 1
            elif dist <= boid.roa:  # attraction zone
                des_a += dir2other
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

    def store_quantities(self, data_logger, is_roo_rising=False):
        """Store data.

        Store data at instant t.

        Args:
            is_roo_rising (bool): Whether the radius of orientation is rising or not.
            data_logger (DataLogger): Data logger.

        """
        quantities = {"cgroup": self.cgroup.reshape(-1), "dgroup": self.dgroup.reshape(-1), "pgroup": self.pgroup,
                      "mgroup": self.mgroup, "speed": self.speed, "turning_rate": self.turning_rate, "roa": self.roa,
                      "roo": self.roo, "ror": self.ror, "speed_sd": self.speed_sd, "turning_rate_sd": self.tr_sd,
                      "ror_sd": self.ror_sd, "roo_sd": self.roo_sd, "roa_sd": self.roa_sd,
                      "is_roo_rising": is_roo_rising}
        data_logger.quantities = data_logger.quantities.append(quantities, ignore_index=True)

    def store_state(self, data_logger):
        front_order = self.front_order
        center_order = self.center_order
        for i in range(len(self.pop)):
            ind = self.pop[i]
            ind_state = {"id": i, "pos": ind.pos.reshape(-1), "angle": ind.angle[0], "speed": ind.speed,
                         "turning_rate": ind.turning_rate, "ror": ind.ror, "roo": ind.roo, "roa": ind.roa,
                         "front_idx": front_order[i], "center_idx": center_order[i]}
            data_logger.state = data_logger.state.append(ind_state, ignore_index=True)

    def get_properties(self):
        properties = ["cgroup = " + str(self.cgroup.reshape(-1)), "dgroup = " + str(self.dgroup.reshape(-1)),
                      "pgroup = {:.5f}".format(self.pgroup), "mgroup = {:.5f}".format(self.mgroup),
                      "roa = " + str(self.roa), "roo = " + str(self.roo), "ror = " + str(self.ror)]
        return properties

    @property
    def front_order(self):
        cgroup = self.cgroup
        dgroup = self.dgroup
        pop_sorted = []
        for i in range(len(self.pop)):
            ind = self.pop[i]
            relative_pos = ind.pos - cgroup
            front = np.dot(relative_pos, dgroup)
            pop_sorted.append((front, i))
        pop_sorted.sort(key=lambda elem: elem[0])
        order = [-1 for _ in range(len(self.pop))]  # Preallocate the list
        for i in range(len(pop_sorted)):
            _, ind_id = pop_sorted[i]
            order[ind_id] = i
        return order

    @property
    def center_order(self):
        cgroup = self.cgroup
        pop_sorted = []
        for i in range(len(self.pop)):
            ind = self.pop[i]
            relative_pos = (ind.pos - cgroup).reshape(-1)
            d_center = np.dot(relative_pos, relative_pos)
            pop_sorted.append((d_center, i))
        pop_sorted.sort(key=lambda elem: elem[0])
        order = [-1 for _ in range(len(self.pop))]  # Preallocate the list
        for i in range(len(pop_sorted)):
            _, ind_id = pop_sorted[i]
            order[ind_id] = i
        return order
