from src import PALETTE
from src import Boid
from random import choice
import numpy as np


def _angle(x):
    return np.arctan2(x[1], x[0])

def _norm(x):
    return x if np.allclose(x, 0) else x / np.linalg.norm(x)


class Universe():
    def __init__(self,
                 canvas,
                 edge_behaviour="avoid",
                 nearby_method="dist",
                 view_dist=80.0,
                 num_neighbors=5,
                 sep=1,
                 align=1,
                 cohes=1):
        self.boids = []
        self.canvas = canvas

        self.nearby_method = nearby_method
        self.view_dist = view_dist
        self.num_neighbors = num_neighbors

        self.edge_behaviour = edge_behaviour
        self.weights = {
            "seperation": sep,
            "alignment": align,
            "cohesion": cohes}

    def add_boid(self, color=None, pos=None, angle=None):
        color = color or choice(PALETTE["accents"])
        pos = pos or self.canvas.size * (1 - 2 * np.random.random(self.canvas.size.shape))
        angle = angle or (2 * np.pi * np.random.random())
        self.boids.append(Boid(color, pos, angle))

    def populate(self, n):
        for _ in range(n):
            self.add_boid()

    def get_nearby(self, boid):
        if self.nearby_method == "dist":
            out = []
            for other in self.boids:
                if boid.dist(other.pos) < self.view_dist and boid is not other:
                    out.append(other)
            return out
        elif self.nearby_method == "count":
            return sorted((other for other in self.boids if other is not boid), key=lambda other: boid.dist(other.pos))[:self.num_neighbors]

    def reorient(self, boid):
        """
        calculates the new direction of the boid with 3 rules: cohesion,
        seperation, alignment
        """
        # get nearby boids
        nearby = self.get_nearby(boid)

        avg_pos = np.array((0, 0), dtype="float")  # cohesion
        avg_dir = np.array((0, 0), dtype="float")  # alignment
        avoid_boids = np.array((0, 0), dtype="float")  # seperation
        avoid_walls = np.array((0, 0), dtype="float")  # turn away from walls (if enabled)

        # calculate all three forces if there are any boids nearby
        if len(nearby) != 0:
            for i, other in enumerate(nearby):
                diff = other.pos - boid.pos

                avg_pos += (diff - avg_pos) / (i + 1)  # running average
                avg_dir += (other.dir - avg_dir) / (i + 1)  # running average
                avoid_boids -= diff / np.dot(diff, diff)

            # normalize them
            avg_pos = _norm(avg_pos)
            avg_dir = _norm(avg_dir)
            avoid_boids = _norm(avoid_boids)


        # if an edge is in view range
        if self.edge_behaviour == "avoid" and (np.abs(boid.pos) > self.canvas.size - self.view_dist).any():
            for i, (coord, lower, upper) in enumerate(zip(boid.pos, -self.canvas.size, self.canvas.size)):
                if (diff := coord - lower) < self.view_dist:
                    avoid_walls[i] += np.abs(1 / diff)
                if (diff := upper - coord) < self.view_dist:
                    avoid_walls[i] -= np.abs(1 / diff)

        # sum them up and if its not zero return it
        sum = _norm(avoid_walls) + _norm(self.weights["seperation"] * avoid_boids + self.weights["cohesion"] * avg_pos + self.weights["alignment"] * avg_dir)
        if np.allclose(sum, 0):
            return boid.angle
        else:
            return _angle(sum)

    def draw(self):
        self.canvas.fill(PALETTE["background"])
        for boid in self.boids:
            boid.draw(self.canvas)
        self.canvas.update()

    def tick(self):
        # calculate new directions
        angles = []
        for boid in self.boids:
            angles.append(self.reorient(boid))

        for boid, angle in zip(self.boids, angles):
            if self.edge_behaviour == "wrap":
                self.wrap(boid)
            boid.turn_to(angle, 1 / self.canvas.fps)
            boid.tick(1 / self.canvas.fps)

    def wrap(self, boid):
        boid.pos = (boid.pos + self.canvas.size) % (2 * self.canvas.size) - self.canvas.size

    def loop(self):
        while self.canvas.is_open():
            self.draw()
            self.tick()

