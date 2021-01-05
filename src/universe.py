from .borders import Border, Infinite
from .perceptions import Perception
from src import PALETTE, Population, Canvas


class Universe:
    def __init__(
        self, canvas, perception, border, dt=1, ror=1, roo=1, roa=1,
            bais=0, std=0, verbose=False):
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
        self.boids = Population(roa, roo, ror, perception, std)
        self.canvas = canvas
        self.border = border
        self.verbose = verbose

    def populate(self, n, speed=1,
                 turning_rate=0.17453292519943295):
        """Populate with new individuals.

        Args:
            n (int): The number of individuals to add.
        """
        for _ in range(n):
            self.boids.add_boid(speed=speed, turning_rate=turning_rate)

    def draw(self):
        """Draw on the canvas."""
        self.canvas.fill(PALETTE["background"])
        if isinstance(self.border, Infinite):
            self.canvas.fit(self.boids)
        self.boids.draw(self.canvas)
        if self.verbose:
            self.canvas.show_properties(self.boids.get_properties())
        self.canvas.update()

    def tick(self):
        """Perform on tick.

        Recursively update the whole simulation.
        """
        self.boids.tick(self.dt)

    def loop(self, step_nb, pretick=None, posttick=None):
        """Loop the simulation.

        Draw then update the simulation until the canvas is closed.
        """
        for i in range(step_nb):
            print(f'Simulation step {i} / {step_nb}')
            if pretick:
                pretick(self)
            self.draw()
            self.tick()
            if posttick:
                posttick(self)
        print('Simulation: Done')
