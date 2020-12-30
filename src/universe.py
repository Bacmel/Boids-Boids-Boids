from .borders import Border
from .perceptions import Perception
from src import PALETTE, Population, Canvas


class Universe:
    def __init__(self, canvas, perception, border, dt=1, ror=1, roo=1, roa=1, std=0):
        """Build a universe.

        Args:
            canvas (Canvas): The canvas to draw on.
            perception (Perception): The perception used by the population.
            border (Border): The border policy.
            dt (float): The time step (in seconds).
            ror (float): The radius of repulsion.
            roo (float): The radius of orientation.
            roa (float): The radius of alignment.
        """
        self.dt = dt
        self.boids = Population(ror, roo, roa, perception, std)
        self.canvas = canvas
        self.border = border

    def populate(self, n):
        """Populate with new individuals.

        Args:
            n (int): The number of individuals to add.
        """
        for _ in range(n):
            self.boids.add_boid(border=self.border)

    def draw(self):
        """Draw on the canvas."""
        self.canvas.fill(PALETTE["background"])
        self.boids.draw(self.canvas)
        self.canvas.update()

    def tick(self):
        """Perform on tick.

        Recursively update the whole simulation.
        """
        self.boids.tick(self.dt)

    def loop(self, fonction=None):
        """Loop the simulation.

        Draw then update the simulation until the canvas is closed.
        """
        for i in range(100):
            print(f'Simulation step {i}/100')
            if fonction:
                fonction(self)
            self.draw()
            self.tick()
