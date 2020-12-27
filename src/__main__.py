from argparse import ArgumentParser
from os import remove
from src import PALETTE, DEFAULT_NUM_NEIGHBORS, DEFAULT_VIEW_DIST
from src import Universe, Canvas, Boid
from src import getArgs


if __name__ == "__main__":
    
    args = getArgs()

    # run simulation
    with Canvas(args.res.split("x"), args.fps, args.render) as canvas:
        u = Universe(
            canvas,
            edge_behaviour=args.edge_behaviour,
            nearby_method="dist" if args.num_neighbors is None else "count",
            view_dist=args.dist or DEFAULT_VIEW_DIST,
            num_neighbors=args.num_neighbors or DEFAULT_NUM_NEIGHBORS,
            sep=args.sep,
            align=args.align,
            cohes=args.cohes,
        )

        if args.highlight:
            u.add_boid(color=PALETTE["highlight"], pos=(0, 0))
            args.n -= 1

        u.populate(args.n)
        u.loop()

    # delete file if wanted
    if args.preview_only or input("Save video? (Y/n) ").lower() == "n":
        remove(canvas.filename)
