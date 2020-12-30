from argparse import ArgumentTypeError
from os import remove
from src import PALETTE, DEFAULT_NUM_NEIGHBORS, DEFAULT_VIEW_DIST, BOID_TURN_SPEED, BOID_VEL
from src import Universe, Canvas, Boid
from .borders import Wall, Toric, Infinite
from .perceptions import Range, KNN, Outlier, BlindSpot
from src import arguments as argu
import numpy as np
from math import pi

if __name__ == "__main__":

    args = argu.getArgs()

    try:
        argu.globalCond(args.boid_speed, args.time_step, args.repulsion_radius)
        BOID_TURN_SPEED = args.turning_rate / 180 * pi
        BOID_VEL = args.boid_speed
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

        if args.view_dist is not None:
            perception = Range(args.view_dist, border, perception)

        directions = args.blindspot_direction
        openings = args.blindspot_opening
        # Conditions on blindspots arguments
        argu.blindspotCond(directions, openings)

        if not (directions == None and openings == None):
            for direction, opening in zip(directions, openings):
                perception = BlindSpot(
                    direction / 180 * pi, opening / 180 * pi, border,
                    perception)

        if args.num_neighbors is not None:
            perception = KNN(args.num_neighbors, border, perception)

        if args.diff_threshold is not None:
            perception = Outlier(args.diff_threshold, border, perception)

    except ArgumentTypeError as err:
        print(err)
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
            std=float(args.error_params.split(':')[1]),
        )

        if args.highlight:
            u.add_boid(color=PALETTE["highlight"], pos=(0, 0))
            args.n -= 1

        u.populate(args.n)
        u.loop()
