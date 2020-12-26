from src import PALETTE
from src import Boid
from src import Population
from random import choice
import numpy as np

class Universe():
    def __init__(self,
                 canvas,
                 view_dist=80.0,
                 dt=1,
                 ror=1,
                 roo=1,
                 roa=1):
        self.dt = dt
        self.boids = Population(ror, roo, roa)
        self.canvas = canvas

    def populate(self, n):
        for _ in range(n):
            self.boids.add_boid()

    def draw(self):
        self.canvas.fill(PALETTE["background"])
        self.boids.draw(self.canvas)
        self.canvas.update()

    def tick(self):
        # calculate new directions
        self.boids.tick(self.dt)

    def loop(self):
        while self.canvas.is_open():
            self.draw()
            self.tick()