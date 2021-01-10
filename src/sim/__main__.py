#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from argparse import ArgumentTypeError
from math import ceil, pi

import numpy as np

from . import Canvas, Incrementor, PALETTE, Population, Universe, arguments as argu
from .borders import Infinite, Toric, Wall
from .data_logger import DataLogger
from .perceptions import BlindSpot, KNN, Outlier, Range

if __name__ == "__main__":
    args = argu.getArgs()

    dl = DataLogger()
    if args.output:
        dl.destination = f"../logs/{args.output}/"
    incrementor = None
    perception = None
    border = None
    roo = 0
    std = 0.0
    steps = 0
    try:
        argu.globalCond(args.speed, args.time_step, args.repulsion_radius)
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

        argu.perceptionCond(
            args.view_dist,
            directions,
            openings,
            args.num_neighbors,
            args.diff_threshold,
        )

        if args.view_dist is not None:
            perception = Range(args.view_dist, border, perception)

        if not (directions is None and openings is None):
            for i in range(len(directions)):
                perception = BlindSpot(
                    directions[i] / 180 * pi, openings[i] / 180 * pi, border, perception
                )

        if args.num_neighbors is not None:
            perception = KNN(args.num_neighbors, border, perception)

        if args.diff_threshold is not None:
            perception = Outlier(args.diff_threshold, border, perception)

        if argu.rooCond(args.orientation_var, args.roo_step_duration):
            inf_bound, increment, sup_bound = argu.getRooVar(args.orientation_var)
            incrementor = Incrementor(
                inf_bound, increment, sup_bound, args.roo_step_duration
            )

        # selection of the right roo
        if incrementor:
            roo = inf_bound
        else:
            roo = args.orientation_radius

        # selection of the right number of step
        if incrementor:
            steps = (
                ceil(
                    (incrementor.sup_bound - incrementor.inf_bound)
                    / incrementor.increment
                )
                * 2
                - 1
            ) * args.roo_step_duration
        else:
            steps = args.step_nb

    except ArgumentTypeError as err:
        exit(err)

    # run simulation
    with Canvas(args.res.split("x"), border, args.time_step, args.render) as canvas:
        pop = Population(
            args.attraction_radius,
            roo,
            args.repulsion_radius,
            perception,
            args.std,
            args.speed,
            args.turning_rate / 180 * pi,
            args.speed_sd,
            args.tr_sd,
            args.ror_sd,
        )
        u = Universe(
            canvas,
            border=border,
            population=pop,
            dt=args.time_step,
            verbose=args.verbose,
        )

        if args.highlight:
            u.pop.add_individual(color=PALETTE["highlight"], pos=np.zeros((2, 1)))
            args.n -= 1

        u.populate(args.n)
        dl.mkdir_dest()
        u.draw(False)
        canvas.snapshot(dl.destination + "initial_state.png")
        # Simulation loop
        if canvas.render:
            for i in range(steps):
                print(f"Simulation step {i} / {steps} ({i * 100 // steps}%)", end="\r")
                u.draw()
                u.tick()
                if incrementor:
                    if incrementor.will_change or i % 100 == 0:
                        u.pop.store_quantities(dl, incrementor.is_rising)
                        canvas.snapshot(
                            dl.destination
                            + f"intermidiate_roo-{u.pop.roo}_rising-{incrementor.is_rising}_step-{i}.png"
                        )
                    u.pop.roo = incrementor.next()
        else:
            for i in range(steps):
                print(f"Simulation step {i} / {steps} ({i * 100 // steps}%)", end="\r")
                u.tick()
                if incrementor:
                    if incrementor.will_change or i % 100 == 0:
                        u.pop.store_quantities(dl, incrementor.is_rising)
                        u.draw(False)
                        canvas.snapshot(
                            dl.destination
                            + f"intermidiate_roo-{u.pop.roo}_rising-{incrementor.is_rising}_step-{i}.png"
                        )
                    u.pop.roo = incrementor.next()
        print("\nSimulation: Done")

        # Store the final state
        if not incrementor:
            print("saving after")
            u.pop.store_quantities(dl)
        u.pop.store_state(dl)
    dl.flush()
    canvas.snapshot(dl.destination + "final_state.png")
