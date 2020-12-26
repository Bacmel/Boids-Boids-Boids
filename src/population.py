from src import Boid
from src import Perception
import numpy as np

def _angle(x):
    return np.arctan2(x[1], x[0])

def _norm(x):
    return x if np.allclose(x, 0) else x / np.linalg.norm(x)

class Population():
    def __init__(self, attr, orie, repu, per):
        self.pop = [] # list<Boid>
        self.roa = attr # int
        self.roo = orie # int
        self.ror = repu # int
        self.perception = per # Perception

    def add_boid(self, color=None, pos=None, angle=None, shape):
        color = color or choice(PALETTE["accents"])
        pos = pos or self.canvas.size * (1 - 2 * np.random.random(shape))
        angle = angle or (2 * np.pi * np.random.random())
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
        canvas.fill(PALETTE["background"])
        for boid in self.pop:
            boid.draw(canvas)
    
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
            for i, other in enumerate(nearby):
                diff = other.pos - boid.pos
                dist = other.dist(boid.pos)
                if dist <= self.ror : # repulsion
                    des_r -= diff / abs(diff)
                elif dist <= self.roo : # orientation
                    des_o += _norm(other.vel)
                else : # attraction
                    des_a += diff / abs(diff)

        if not np.allclose(des_r, 0):
            des_dir = numpy.append(des_dir, des_r)
        if not np.allclose(des_o, 0):
            des_dir = numpy.append(des_dir, des_o)
        if not np.allclose(des_a, 0):
            des_dir = numpy.append(des_dir, des_a)
        # sum them up and if its not zero return it
        angle = np.mean(des_dir, axis=0)
        if np.allclose(angle, 0):
            return boid.angle
        else:
            return _angle(angle)
