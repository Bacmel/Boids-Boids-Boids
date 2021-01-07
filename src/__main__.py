from argparse import ArgumentTypeError
from math import ceil, pi

import numpy as np

from src import Canvas, Incrementor, PALETTE, Universe, arguments as argu
from src.data_logger import DataLogger
from .borders import Infinite, Toric, Wall
from .perceptions import BlindSpot, KNN, Outlier, Range

if __name__ == "__main__":
    dl = DataLogger()
    args = argu.getArgs()

    incrementor = None
    perception = None
    border = None
    roo = 0
    std = 0.
    steps = 0
    try:
        argu.globalCond(args.boid_speed, args.time_step, args.repulsion_radius)
        # Creation of border
        length = np.array([[int(s)] for s in args.res.split("x")])
        border_size = np.array([100, 100]).reshape(-1, 1)
        if args.border == "wall":
            border = Wall(border_size)
        elif args.border == "wrap":
            border = Toric(border_size)
        elif args.border == "none":
            border = Infinite(border_size)

        # Creation of perception: range > blindspot > knn > outlier

        directions = args.blindspot_direction
        openings = args.blindspot_opening
        # Conditions on blindspots arguments
        argu.blindspotCond(directions, openings)

        argu.perceptionCond(args.view_dist, directions, openings, args.num_neighbors, args.diff_threshold)

        if args.view_dist is not None:
            perception = Range(args.view_dist, border, perception)

        if not (directions is None and openings is None):
            for i in range(len(directions)):
                perception = BlindSpot(directions[i] / 180 * pi, openings[i] / 180 * pi, border, perception)

        if args.num_neighbors is not None:
            perception = KNN(args.num_neighbors, border, perception)

        if args.diff_threshold is not None:
            perception = Outlier(args.diff_threshold, border, perception)

        argu.gaussCond(args.error_params)
        mu, std = args.error_params.split(":")
        mu = float(mu) / 180 * pi
        std = float(std) / 180 * pi

        if argu.rooCond(args.orientation_var, args.roo_step_duration):
            inf_bound, increment, sup_bound = argu.getRooVar(args.orientation_var)
            incrementor = Incrementor(inf_bound, increment, sup_bound, args.roo_step_duration)

        # selection of the right roo
        if incrementor:
            roo = inf_bound
        else:
            roo = args.orientation_radius

        # selection of the right number of step
        if incrementor:
            steps = (ceil((
                                      incrementor.sup_bound - incrementor.inf_bound) / incrementor.increment) * 2 -
                     1) * args.roo_step_duration
        else:
            steps = args.step_nb

    except ArgumentTypeError as err:
        exit(err)

    # run simulation
    with Canvas(args.res.split("x"), border, args.time_step, args.render) as canvas:
        u = Universe(canvas, perception=perception, border=border, dt=args.time_step, ror=args.repulsion_radius,
                     roo=roo, roa=args.attraction_radius, std=std, verbose=args.verbose)

        if args.highlight:
            u.boids.add_boid(color=PALETTE["highlight"], pos=(0, 0))
            args.n -= 1

        u.populate(args.n, speed=args.boid_speed, turning_rate=args.turning_rate / 180 * pi)

        # Simulation loop
        for i in range(steps):
            print(f'Simulation step {i} / {steps} ({i * 100 // steps}%)')
            u.spin_once()
            if incrementor:
                if incrementor.will_change:
                    u.boids.store_quantities(dl, incrementor.is_rising)
                incrementor.next(u)
        print('Simulation: Done')

        # Store the final state
        if not incrementor:
            print("saving after")
            u.boids.store_quantities(dl)
        u.boids.store_state(dl)
    dl.flush()
