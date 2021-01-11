import numpy as np
from .borders import Wall, Toric, Infinite
from .perceptions import BlindSpot, KNN, Outlier, Range
from . import Incrementor, Canvas, Population, Universe
from math import pi, ceil
from . import arguments as argu
from .data_logger import DataLogger
import time


class Sim:
    def __init__(self):
        super().__init__()
        self.border = None
        self.perception = None
        self.incrementor = None
        self.steps_nb = 0
        self.roo = 0.0

    def build_border(self, kind, size=np.array([[100], [100]])):
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
        if incrementor is None:
            return
        self.incrementor = incrementor
        self.roo = self.incrementor.inf_bound
        # selection of the right number of step
        self.steps_nb = (
            ceil(
                (self.incrementor.sup_bound - self.incrementor.inf_bound)
                / self.incrementor.increment
            )
            * 2
            - 1
        ) * incrementor.step_duration

    def from_args(self, args):
        argu.globalCond(args.speed, args.time_step, args.repulsion_radius)

        # Creation of border
        self.build_border(args.border)

        # Creation of perception
        argu.blindspotCond(args.blindspot_direction, args.blindspot_opening)
        argu.perceptionCond(
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
        if argu.rooCond(args.orientation_var, args.roo_step_duration):
            inf_bound, increment, sup_bound = argu.getRooVar(args.orientation_var)
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
            args.roa_sd
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
        roa_sd=0.0
    ):
        dl = DataLogger()
        if output:
            dl.destination = f"../logs/{output}/"
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
            roa_sd
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
        dl.flush()
        u.draw(first=True)
        canvas.snapshot(dl.destination + "final_state")
