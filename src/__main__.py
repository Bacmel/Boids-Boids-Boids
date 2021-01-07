import numpy as np
from argparse import ArgumentTypeError
from math import pi
from os import remove
from src import PALETTE, Universe, Canvas, Boid
from src import arguments as argu
from src.data_logger import DataLogger
from .borders import Wall, Toric, Infinite
from .perceptions import Range, KNN, Outlier, BlindSpot


if __name__ == "__main__":
    dl = DataLogger()
    args = argu.getArgs()

    try:
        argu.globalCond(args.boid_speed, args.time_step, args.repulsion_radius)
        # Creation of border
        border = None
        length = np.array([[int(s)] for s in args.res.split("x")])
        border_size = np.array([100, 100]).reshape(-1, 1)
        if args.border == "wall":
            border = Wall(border_size)
        elif args.border == "wrap":
            border = Toric(border_size)
        elif args.border == "none":
            border = Infinite(border_size)

        # Creation of perception: range > blindspot > knn > outlier
        perception = None

        directions = args.blindspot_direction
        openings = args.blindspot_opening
        # Conditions on blindspots arguments
        argu.blindspotCond(directions, openings)

        argu.perceptionCond(args.view_dist, directions,
                            openings, args.num_neighbors, args.diff_threshold)

        if args.view_dist is not None:
            perception = Range(args.view_dist, border, perception)

        if not (directions == None and openings == None):
            for i in range(len(directions)):
                perception = BlindSpot(
                    directions[i] / 180 * pi, openings[i] / 180 * pi, border,
                    perception)

        if args.num_neighbors is not None:
            perception = KNN(args.num_neighbors, border, perception)

        if args.diff_threshold is not None:
            perception = Outlier(args.diff_threshold, border, perception)

        argu.gaussCond(args.error_params)
        mu, std = args.error_params.split(":")
        mu = float(mu) / 180 * pi
        std = float(std) / 180 * pi

    except ArgumentTypeError as err:
        exit(err)

    # run simulation
    with Canvas(args.res.split("x"), border, args.time_step, args.render) as canvas:
        u = Universe(
            canvas,
            perception=perception,
            border=border,
            dt=args.time_step,
            ror=args.repulsion_radius,
            roo=args.orientation_radius,
            roa=args.attraction_radius,
            std=std
        )

        if args.highlight:
            u.boids.add_boid(color=PALETTE["highlight"], pos=(0, 0))
            args.n -= 1

        u.populate(args.n, speed=args.boid_speed,
                   turning_rate=args.turning_rate / 180 * pi)
        u.loop(args.step_nb, pretick=lambda uni: uni.boids.store_quantities(dl))
        u.boids.store_state(dl)
    dl.flush()
