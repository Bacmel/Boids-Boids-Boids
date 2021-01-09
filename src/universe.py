from src import Canvas, PALETTE, Population
from .borders import Border, Infinite
from .perceptions import Perception


class Universe:
    def __init__(
            self, canvas, perception, border, population, dt=1, verbose=False):
        """Build a universe.

        Args:
            canvas (Canvas): The canvas to draw on.
            perception (Perception): The perception used by the population.
            border (Border): The border policy.
            population (Population): The population of partiules in the universe
            dt (float): The time step (in seconds).
            verbose (Bool): Flag to display population info in the canvas.
        """
        self.dt = dt
        self.boids = population
        self.canvas = canvas
        self.border = border
        self.verbose = verbose

    def populate(self, n):
        """Populate with new individuals.

        Args:
            n (int): The number of individuals to add.
        """
        for _ in range(n):
            self.boids.add_boid()

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

    def spin_once(self):
        self.draw()
        self.tick()

    def spin(self, step_nb, pretick=None, posttick=None):
        """Loop the simulation.

        Draw then update the simulation until the canvas is closed.

        Args:
            step_nb: number of step in the simualtion.
            pretick: function to call before update of the simulation.
            posttick: function to call after the update of the simulation.
        """
        for i in range(step_nb):
            print(f'Simulation step {i} / {step_nb}')
            if pretick:
                pretick(self)
            self.spin_once()
            if posttick:
                posttick(self)
        print('Simulation: Done')
