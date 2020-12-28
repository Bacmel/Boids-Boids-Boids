from argparse import ArgumentTypeError
from os import remove
from src import PALETTE, DEFAULT_NUM_NEIGHBORS, DEFAULT_VIEW_DIST
from src import Universe, Canvas, Boid
from .borders import Wall, Toric, Infinite
from .perceptions import Range, KNN, Outlier, BlindSpot
from . import arguments as argu 

if __name__ == "__main__":
    
    args = argu.getArgs()

    try:
        argu.globalCond(args.boid_speed, args.time_step, args.repulsion_radius)

        # Creation of border
        border = None
        if args.border == "wall":
            border = Wall(args.res.split("x"))
        elif args.border == "wrap":
            border = Toric(args.res.split("x"))
        elif args.border == "none":
            border = Infinite(args.res.split("x"))


        # Creation of perception: range > blindspot > knn > outlier
        perception = None

        if args.view_dist is not None:
            perception = Range(args.view_dist, border, perception)
        
        directions = args.blindspot_direction
        openings = args.blindspot_opening
        # Conditions on blindspots arguments
        argu.blindspotCond(directions, openings)
        
        if not (directions == None and openings == None):
            for i in range(directions):
                perception = BlindSpot(directions[i], openings[i], border, perception)

        if args.num_neighbors is not None:
            perception = KNN(args.num_neighbors, border, perception)
        
        if args.diff_threshold is not None:
            perception = Outlier(args.diff_threshold, border, perception)
    
    except ArgumentTypeError as err:
        print(err)
        return

    # run simulation
    with Canvas(args.res.split("x"), args.fps, args.render) as canvas:
        u = Universe(
            canvas,
            perception=perception,
            border=border,
            dt=args.time_step,
            ror=args.repulsion_radius,
            roo=args.orientation_radius,
            roa=args.attraction_radius,
        )

        if args.highlight:
            u.add_boid(color=PALETTE["highlight"], pos=(0, 0))
            args.n -= 1

        u.populate(args.n)
        u.loop()

    # delete file if wanted
    if args.preview_only or input("Save video? (Y/n) ").lower() == "n":
        remove(canvas.filename)
