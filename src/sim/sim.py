# -*- coding: utf-8 -*-

import time
from math import pi, ceil
import numpy as np
from . import Incrementor, Canvas, Population, Universe, DataLogger
from . import arguments as argu
from .borders import Wall, Toric, Infinite
from .perceptions import BlindSpot, KNN, Outlier, Range


class Sim:
    def __init__(self):
        super().__init__()
        self.border = None
        """Border: The border (aka. the type of world)."""
        self.perception = None
        """Perception: The particles perception."""
        self.incrementor = None
        """Incrementor: The incrementor to use for the range of orientation."""
        self.steps_nb = 0
        """int: The number of steps to perform."""
        self.roo = 0.0
        """float: The range of repulsion"""

    def build_border(self, kind, size=np.array([[100], [100]])):
        """Build a border of the given kind.

        Args:
            kind (str): The kind of border to create.
            size (np.ndarray, optional): The size of the simulation area (not used when the border kind is 'none').
        """
        border_size = np.array([100, 100]).reshape(-1, 1)
        if kind == "wall":
            self.border = Wall(border_size)
        elif kind == "wrap":
            self.border = Toric(border_size)
        elif kind == "none":
            self.border = Infinite(border_size)

    def build_perception(
        self,
        view_dist=None,
        directions=None,
        openings=None,
        num_neighbors=None,
        diff_threshold=None,
    ):
        """Build a perception used for every particles.

        Args:
            view_dist (float, optional): The view distance of a particle. Defaults to None.
            directions (list<float>, optional): The list of blindspot directions. Defaults to None.
            openings (list<float>, optional): The list of blindspot opening. Defaults to None.
            num_neighbors (int, optional): The k nearest neighbors seen by a particle. Defaults to None.
            diff_threshold (float, optional): The angular difference threshold to consider a neighbor as an outlier. Defaults to None.

        Raises:
            ValueError: When the border is not initialized or all arguments are None.
        """
        self.perception = None
        if self.border is None:
            raise ValueError("Border is not initialized")
        if (
            directions is None
            and openings is None
            and view_dist is None
            and num_neighbors is None
            and diff_threshold is None
        ):
            raise ValueError("All perception parameters are None")

        if view_dist is not None:
            self.perception = Range(view_dist, self.border, self.perception)

        if not (directions is None and openings is None):
            for i in range(len(directions)):
                self.perception = BlindSpot(
                    directions[i] / 180 * pi,
                    openings[i] / 180 * pi,
                    self.border,
                    self.perception,
                )

        if num_neighbors is not None:
            self.perception = KNN(num_neighbors, self.border, self.perception)

        if diff_threshold is not None:
            self.perception = Outlier(diff_threshold, self.border, self.perception)

    def use_roo_increment(self, incrementor: Incrementor):
        """Setup increments for the range of orientation.

        Args:
            incrementor (Incrementor): The given incrementor.
        """
        if incrementor is None:
            return
        self.incrementor = incrementor
        self.roo = self.incrementor.inf_bound
        # Selection of the right number of steps
        self.steps_nb = (
            ceil(
                (self.incrementor.sup_bound - self.incrementor.inf_bound)
                / self.incrementor.increment
            )
            * 2
            - 1
        ) * incrementor.step_duration

    def from_args(self, args):
        """Launch a simulation from command arguments.

        Args:
            args (dict): The given command arguments.
        """
        argu.global_cond(args.speed, args.time_step, args.repulsion_radius)

        # Creation of border
        self.build_border(args.border)

        # Creation of perception
        argu.blindspot_cond(args.blindspot_direction, args.blindspot_opening)
        argu.perception_cond(
            args.view_dist,
            args.blindspot_direction,
            args.blindspot_opening,
            args.num_neighbors,
            args.diff_threshold,
        )
        self.build_perception(
            args.view_dist,
            args.blindspot_direction,
            args.blindspot_opening,
            args.num_neighbors,
            args.diff_threshold,
        )

        self.roo = args.orientation_radius
        self.steps_nb = args.step_nb

        # Create an incrementor
        if argu.roo_cond(args.orientation_var, args.roo_step_duration):
            inf_bound, increment, sup_bound = argu.get_roo_var(args.orientation_var)
            incrementor = Incrementor(
                inf_bound, increment, sup_bound, args.roo_step_duration
            )
            self.use_roo_increment(incrementor)

        self.run(
            args.n,
            args.attraction_radius,
            args.repulsion_radius,
            args.std / 180 * pi,
            args.speed,
            args.turning_rate / 180 * pi,
            args.time_step,
            args.render,
            args.verbose,
            args.output,
            np.array(args.res.split("x"), dtype="int"),
            args.speed_sd,
            args.tr_sd / 180 * pi,
            args.ror_sd,
            args.roo_sd,
            args.roa_sd,
        )

    def run(
        self,
        pop_size,
        roa,
        ror,
        decision_noise_sd,
        speed,
        turning_rate,
        timestep=0.1,
        render=False,
        verbose=False,
        output=None,
        res=[500, 500],
        speed_sd=0.0,
        tr_sd=0.0,
        ror_sd=0.0,
        roo_sd=0.0,
        roa_sd=0.0,
    ):
        """Run one instance.

        Args:
            pop_size (int): The size of the population.
            roa (float): The range of attraction.
            ror (float): The range of repulsion.
            decision_noise_sd (float): The sd. of the centered Gaussien noise applied to particle decisions.
            speed (float): The particle speed (in length units per seconds)
            turning_rate (float): The particle angular speed (in radians per seconds)
            timestep (float, optional): The sampling period (in seconds). Defaults to 0.1.
            render (bool, optional): Whether a video is rendered or not. Defaults to False.
            verbose (bool, optional): Whether additionnal data are rendered or not. Defaults to False.
            output (str, optional): The specific path to output to. Defaults to None.
            res (list<int>, optional): The video resolution. Defaults to [500, 500].
            speed_sd (float, optional): The sd. of the speed Gaussien distribution. Defaults to 0.0.
            tr_sd (float, optional): The sd. of the angular speed Gaussien distribution. Defaults to 0.0.
            ror_sd (float, optional): The sd. of the range of repulsion Gaussien distribution. Defaults to 0.0.
            roo_sd (float, optional): The sd. of the range of orientation Gaussien distribution. Defaults to 0.0.
            roa_sd (float, optional): The sd. of the range of attraction Gaussien distribution. Defaults to 0.0.
        """
        # Initialize the data logger
        dl = DataLogger()
        if output:
            dl.destination = f"../logs/{output}/"  # Change the output directory

        # Initialize the simulation
        pop = Population(
            roa,
            self.roo,
            ror,
            self.perception,
            decision_noise_sd,
            speed,
            turning_rate,
            speed_sd,
            tr_sd,
            ror_sd,
            roo_sd,
            roa_sd,
        )
        start = time.perf_counter()
        with Canvas(timestep, render) as canvas:
            u = Universe(
                canvas,
                border=self.border,
                population=pop,
                dt=timestep,
                verbose=verbose,
            )

            u.populate(pop_size)
            dl.mkdir_dest()
            u.draw(first=True)
            canvas.snapshot(dl.destination + "initial_state")
            # Simulation loop
            if canvas.render:
                for i in range(self.steps_nb):
                    print(
                        f"Simulation step {i} / {self.steps_nb} ({i * 100 // self.steps_nb}%)",
                        end="\r",
                    )
                    u.draw(ind=i)
                    u.tick()
                    if self.incrementor is not None:
                        if self.incrementor.will_change:
                            u.pop.store_quantities(dl, self.incrementor.is_rising)
                            canvas.snapshot(
                                dl.destination
                                + f"intermidiate_roo-{u.pop.roo}_rising-{self.incrementor.is_rising}.png"
                            )
                        u.pop.roo = self.incrementor.next()
            else:
                for i in range(self.steps_nb):
                    print(
                        f"Simulation step {i} / {self.steps_nb} ({i * 100 // self.steps_nb}%)",
                        end="\r",
                    )
                    u.tick()
                    if self.incrementor is not None:
                        if self.incrementor.will_change:
                            u.pop.store_quantities(dl, self.incrementor.is_rising)
                            u.draw(first=True)
                            canvas.snapshot(
                                dl.destination
                                + f"intermidiate_roo-{u.pop.roo}_rising-{self.incrementor.is_rising}.png"
                            )
                        u.pop.roo = self.incrementor.next()
            end = time.perf_counter()
            print("\nSimulation: Done in {:.3f} s".format(end - start))

            # Store the final state
            if not self.incrementor:
                u.pop.store_quantities(dl)
            u.pop.store_state(dl)


        dl.flush() # Write on the disk

        # Save the final state of the population as an image
        u.draw(first=True)
        canvas.snapshot(dl.destination + "final_state")
