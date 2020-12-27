from argparse import ArgumentParser
from os import remove
from src import PALETTE, DEFAULT_NUM_NEIGHBORS, DEFAULT_VIEW_DIST
from src import Universe, Canvas, Boid
from src import getArgs
from .borders import Wall, Toric, Infinite


if __name__ == "__main__":
    
    args = getArgs()

    # Creation of border
    border = None
    if args.border == "wall":
        border = Wall(args.res.split("x"))
    elif args.border == "wrap":
        border = Toric(args.res.split("x"))
    elif args.border == "none":
        border = Infinite(args.res.split("x"))
    
    # TODO: argument assert function to test border argument

    # Creation of perception: range > blind spot > knn > outlier

    # run simulation
    with Canvas(args.res.split("x"), args.fps, args.render) as canvas:
        u = Universe(
            canvas,
            border=args.border,
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
