# -*- coding: utf-8 -*-
from . import Canvas, PALETTE, Population
from .borders import Border, Infinite


class Universe:
    def __init__(self, canvas, border, population, dt=1, verbose=False):
        """Build a universe.

        Args:
            canvas (Canvas): The canvas to draw on.
            border (Border): The border policy.
            population (Population): The population of particles in the universe
            dt (float): The time step (in seconds).
            verbose (bool): Flag to display population info in the canvas.
        """
        self.dt = dt
        """float: The time step duration (in seconds)."""
        self.pop = population
        """Population: The population to manage."""
        self.canvas = canvas
        """Canvas: The canvas to draw on."""
        self.border = border
        """Border: The border policy."""
        self.verbose = verbose
        """bool: Flag to display population info in the canvas."""

    def populate(self, n):
        """Populate with new individuals.

        Args:
            n (int): The number of individuals to add.
        """
        for _ in range(n):
            self.pop.add_individual()

    def draw(self, first=False, ind=-1):
        """Draw on the canvas."""
        if first:
            self.canvas.draw(self.border, self.pop, self.verbose)
        else:
            self.canvas.update(ind, self.pop, self.verbose)

    def tick(self):
        """Perform on tick.

        Recursively update the whole simulation.
        """
        self.pop.tick(self.dt)

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
            print(f"Simulation step {i} / {step_nb}")
            if pretick:
                pretick(self)
            self.spin_once()
            if posttick:
                posttick(self)
        print("Simulation: Done")
