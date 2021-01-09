from math import cos, pi, sin
import random

import numpy as np
import numpy.linalg as lin
import numpy.random as np_rand

from src import Boid, PALETTE
from src.utils import angle, normalize


class Population:
    def __init__(
        self,
        roa,
        roo,
        ror,
        per,
        std,
        speed=1,
        turning_rate=0.2,
        speed_sd=0.0,
        tr_sd=0.0,
        ror_sd=0.0,
        roo_sd=0.0,
        roa_sd=0.0,
    ):
        """Population Constructor.

        Args:
            roa (float): The radius of attraction (in length units).
            roo (float): The radius of orientation (in length units).
            ror (float): The radius of repulsion (in length units).
            per (Perception): The perception of the population.
            std (float): The standard deviation in the decision process (in radians).
            speed (float): The mean speed (in length units per seconds).
            turning_rate (float): The maximal angular speed (in radians per seconds).
            speed_sd (float): The standard deviation of the speed (in length units per seconds).
            tr_sd (float): The standard deviation of the maximal angular speed (in radians per seconds).
            ror_sd (float): The standard deviation of the range of repulsion (in length units).
            roo_sd (float): The standard deviation of the range of orientation (in length units).
            roa_sd (float): The standard deviation of the range of attraction (in length units).

        """
        self.pop = []
        """list<Boid>: The list of individuals."""
        self.speed = speed
        """float: The mean speed (in length units per seconds)."""
        self.turning_rate = turning_rate
        """float: The maximal turning rate (in radians per seconds)."""
        self.roa = roa
        """float: The radius of attraction (in length units)."""
        self.roo = roo
        """float: The radius of orientation (in length units)."""
        self.ror = ror
        """float: The radius of repulsion (in length units)."""
        self.perception = per
        """Perception: The perception of the population."""
        self.std = std
        """float: The standard deviation in the decision process (in radians)."""
        self.speed_sd = speed_sd
        """float: The standard deviation of the speed (in length units per seconds)."""
        self.tr_sd = tr_sd
        """float: The standard deviation of the maximal angular speed (in radians per seconds)."""
        self.ror_sd = ror_sd
        """float: The standard deviation of the range of repulsion (in length units)."""
        self.roo_sd = roo_sd
        """float: The standard deviation of the range of orientation (in length units)."""
        self.roa_sd = roa_sd
        """float: The standard deviation of the range of attraction (in length units)."""

    @property
    def cgroup(self):
        """Compute the group center.

        Returns:
            numpy.ndarray: The position of the group center.

        """
        origin = np.zeros((2, 1))
        mean = np.mean(
            [self.perception.border.vector(origin, ind.pos) for ind in self.pop], axis=0
        )
        return mean

    @property
    def dgroup(self):
        """Compute the group direction.

        Returns:
            numpy.ndarray: The group direction.

        """
        return np.mean([ind.dir for ind in self.pop], axis=0)

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

        for ind in self.pop:
            r_ic = normalize(self.perception.border.vector(cg, ind.pos))
            m_ic = np.cross(r_ic, ind.dir, axis=0)
            m.append(m_ic)
        m_array = np.array(m)
        m_mean = np.mean(m_array)

        return np.linalg.norm(m_mean)

    @property
    def front_order(self):
        """Compute the list of rank for each individual when sorted by the front.

        Returns:
            The list of rank for each individual when sorted by the front.

        """
        cgroup = self.cgroup
        dgroup = self.dgroup.reshape(-1)
        pop_sorted = []
        order = [-1 for _ in range(len(self.pop))]  # Preallocate the list

        # Fill a list of tuple and sort the population by
        for i in range(len(self.pop)):
            ind = self.pop[i]
            relative_pos = (ind.pos - cgroup).reshape(-1)
            front = np.dot(relative_pos, dgroup)
            pop_sorted.append((front, i))
        pop_sorted.sort(key=lambda elem: elem[0])

        # Create the list of individual rank
        for i in range(len(pop_sorted)):
            _, ind_id = pop_sorted[i]
            order[ind_id] = i

        return order

    @property
    def center_order(self):
        """Compute the list of rank for each individual when sorted by the center.

        Returns:
            The list of rank for each individual when sorted by the center.

        """
        cgroup = self.cgroup
        pop_sorted = []
        order = [-1 for _ in range(len(self.pop))]  # Preallocate the list

        # Fill a list of tuple and sort the population by its distance to the center
        for i in range(len(self.pop)):
            ind = self.pop[i]
            relative_pos = (ind.pos - cgroup).reshape(-1)
            d_center = np.dot(relative_pos, relative_pos)
            pop_sorted.append((d_center, i))
        pop_sorted.sort(key=lambda elem: elem[0])

        # Create the list of individual rank
        for i in range(len(pop_sorted)):
            _, ind_id = pop_sorted[i]
            order[ind_id] = i

        return order

    def add_boid(self, color=None, pos=None, angle=None):
        """Add a individual to this population.

        Args:
            color (Color): color for canvas visualisation.
            pos (numpy.ndarray): Initial position.
            angle (float): The initial orientation.
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
                new_speed += random.gauss(0.0, self.speed_sd)
            if self.tr_sd is not None:
                new_tr += random.gauss(0.0, self.tr_sd)
            if self.ror_sd is not None:
                new_ror += random.gauss(0.0, self.ror_sd)
            if self.roo_sd is not None:
                new_roo += random.gauss(0.0, self.roo_sd)
            if self.roa_sd is not None:
                new_roa += random.gauss(0.0, self.roa_sd)

            # No specified pose, ensure the new individual sees another one
            for _ in range(100000):
                pos = self._generate_random_pos(new_roa)
                ind_angle = 2 * pi * (random.random() - 0.5)
                ind = Boid(
                    color, pos, new_ror, new_roo, new_roa, ind_angle, new_speed, new_tr
                )
                if (
                    len(self.pop) == 0
                    or len(self.perception.detect(ind, self.pop)) >= 1
                ):
                    break
            else:
                raise RuntimeError(
                    "Failed to find a valid configuration after 100 000 tries!"
                )
        else:
            # At least one pose element is specified, no warranty
            pos = pos or self._generate_random_pos(self.roa)
            ind_angle = angle or (2 * pi * (random.random() - 0.5))
            ind = Boid(
                color,
                pos,
                self.ror,
                self.roa,
                self.roo,
                ind_angle,
                speed=self.speed,
                turning_rate=self.turning_rate,
            )

        self.pop.append(ind)

    def _generate_random_pos(self, radius):
        """Generate a random position in circle centered on (0,0) and the given radius.

        Args:
            radius (float): The spawning range (in length units).

        Returns:
            numpy.ndarray: The randomly generated position.

        """
        border = self.perception.border
        r = radius * random.random()
        th = 2 * pi * (random.random() - 0.5)
        pos = np.array([[r * cos(th)], [r * sin(th)]]) + border.origin
        return border.wrap(pos)

    def tick(self, dt):
        """Update function.

        Compute new direction and update the position of every individuals.

        Args:
            dt (float): simulation time step.

        """
        # Compute new directions
        angles = []
        for ind in self.pop:
            angles.append(self.reorient(ind))

        # Update positions
        for ind, angle in zip(self.pop, angles):
            ind.turn_to(angle, dt)
            ind.tick(dt)
            ind.pos = self.perception.border.wrap(ind.pos)

    def draw(self, canvas):
        """Draw the population on the canvas.

        Ask each individual to draw itself then draw a fake individual at the mean
        position with the mean orientation.

        Args:
            canvas (Canvas): Graphical object.

        """
        for ind in self.pop:
            ind.draw(canvas)
        bgroup = Boid(0xFFFFF, self.cgroup, 0.0, 0.0, 0.0, angle(self.dgroup))
        bgroup.draw(canvas)

    def reorient(self, ind):
        """Compute a new orientation for the individual.

        Calculate the new direction of the individual with 3 rules:
        - Repulsion
        - Orientation
        - Attraction

        Args:
            ind (Boid): The given individual.

        Returns:
            float: The new orientation for the given individual (in radians).

        """
        nearby = self.perception.detect(ind, self.pop)  # The nearby boids
        border = self.perception.border  # The border policy
        des_r = np.zeros((2, 1), dtype="float")  # Desired repulsion
        des_o = np.zeros((2, 1), dtype="float")  # Desired orientation
        des_a = np.zeros((2, 1), dtype="float")  # Desired attraction
        nb_r = 0  # Number of individuals in repulsion zone
        nb_o = 0  # Number of individuals in orientation zone
        nb_a = 0  # Number of individuals in attraction zone
        roo = ind.roo if self.roo_sd > 0.0 else self.roo

        # Calculate all three forces if there are any boids nearby
        for other in nearby:
            diff = border.vector(ind.pos, other.pos)
            if np.allclose(diff, np.zeros((2, 1))):  # The boids are superposed
                # Compute a random vector to escape
                diff = np_rand.normal(0, 1, (2, 1))
            dist = np.linalg.norm(diff)
            dir2other = diff / dist
            if dist <= ind.ror:  # Repulsion zone
                des_r -= dir2other
                nb_r += 1
            elif dist <= roo:  # Orientation zone
                des_o += other.dir
                nb_o += 1
            elif dist <= ind.roa:  # Attraction zone
                des_a += dir2other
                nb_a += 1

        # Choose the rule to apply
        if nb_r > 0:  # Repulsion rule only
            des_dir = des_r
        elif nb_o > 0:
            if nb_a == 0:  # Orientation rule only
                des_dir = des_o
            else:  # Orientation and attraction rules
                des_dir = np.mean([des_o, des_a], axis=0)
        elif nb_a > 0:  # Attraction rule only
            des_dir = des_a
        else:  # No decision
            des_dir = ind.dir

        # Compute the new angle from the desired direction
        new_angle = angle(des_dir)
        new_angle += random.gauss(0.0, self.std)  # Apply noise to the decision

        return new_angle

    def store_quantities(self, data_logger, is_roo_rising=False):
        """Store data.

        Store data at instant t.

        Args:
            is_roo_rising (bool): Whether the radius of orientation is rising or not.
            data_logger (DataLogger): Data logger.

        """
        quantities = {
            "cgroup": self.cgroup.reshape(-1),
            "dgroup": self.dgroup.reshape(-1),
            "pgroup": self.pgroup,
            "mgroup": self.mgroup,
            "speed": self.speed,
            "turning_rate": self.turning_rate,
            "roa": self.roa,
            "roo": self.roo,
            "ror": self.ror,
            "speed_sd": self.speed_sd,
            "turning_rate_sd": self.tr_sd,
            "ror_sd": self.ror_sd,
            "roo_sd": self.roo_sd,
            "roa_sd": self.roa_sd,
            "is_roo_rising": is_roo_rising,
        }
        data_logger.quantities = data_logger.quantities.append(
            quantities, ignore_index=True
        )

    def store_state(self, data_logger):
        """Store the current state.

        Args:
            data_logger (DataLogger): The given data logger to fill.

        """
        front_order = self.front_order
        center_order = self.center_order
        for i in range(len(self.pop)):
            ind = self.pop[i]
            ind_state = {
                "id": i,
                "pos": ind.pos.reshape(-1),
                "angle": ind.angle[0],
                "speed": ind.speed,
                "turning_rate": ind.turning_rate,
                "ror": ind.ror,
                "roo": ind.roo,
                "roa": ind.roa,
                "front_idx": front_order[i],
                "center_idx": center_order[i],
            }
            data_logger.state = data_logger.state.append(ind_state, ignore_index=True)

    def get_properties(self):
        """Get a list of string describing the properties.

        Returns:
            A list of string describing the properties.

        """
        properties = [
            "cgroup = " + str(self.cgroup.reshape(-1)),
            "dgroup = " + str(self.dgroup.reshape(-1)),
            "pgroup = {:.5f}".format(self.pgroup),
            "mgroup = {:.5f}".format(self.mgroup),
            "roa = " + str(self.roa),
            "roo = " + str(self.roo),
            "ror = " + str(self.ror),
        ]
        return properties
