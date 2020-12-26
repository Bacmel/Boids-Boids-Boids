from argparse import ArgumentParser
from src import PALETTE, DEFAULT_NUM_NEIGHBORS, DEFAULT_VIEW_DIST, BOID_TURN_SPEED, BOID_VEL


def get_args():
    """
    Standard function to specify the default value of the hyper-parameters of experimental setups
    :return: the complete list of arguments
    """
    # setup args
    parser = ArgumentParser()

    # basic
    parser.add_argument("-n",
                        dest="n",
                        type=int,
                        default=60,
                        help="the number of boids in the simulation")
    parser.add_argument("--fps",
                        type=float,
                        default=30.0,
                        help="the (maximum) framerate")
    parser.add_argument("--res",
                        type=str,
                        default="1920x1080",
                        help="the resolution")
    parser.add_argument("--highlight",
                        action="store_true",
                        help="highlight a single boid")
    parser.add_argument("--preview-only",
                        dest="preview_only",
                        action="store_true",
                        help="dont save the video, just show the preview")
    parser.add_argument("--render",
                        action='store_true',
                        help="allow visual rendering during the simulation")
    parser.add_argument("--verbose",
                        action='store_true',
                        help="increase output verbosity")

    # weights
    parser.add_argument("-ra", "--attraction",
                        dest="attraction_radius",
                        type=int,
                        default=1,
                        help="the radius of the attraction zone of each boid")
    parser.add_argument("-ro", "--orientation",
                        dest="orientation_radius",
                        type=int,
                        default=1,
                        help="the radius of the orientation zone of each boid")
    parser.add_argument("-rr", "--repulsion",
                        dest="repulsion_radius",
                        type=int,
                        default=1,
                        help="the radius of the replusion zone of each boid")

    # behaviour near edges
    parser.add_argument("--border",
                        type=str,
                        # toric world, wall delimitation, no edges
                        choices={"wrap", "wall", "none"},
                        default="wall",
                        help="selection of the border of the univers: toric world, wall with collisions or no edges at all")

    # what method to use to decide which boids are close ('nearby')
    parser.add_argument("--count",
                        dest="num_neighbors",
                        type=int,
                        default=DEFAULT_NUM_NEIGHBORS,
                        help=f"the COUNT closest boids are seen by the current boid (defaults to {DEFAULT_NUM_NEIGHBORS})")
    parser.add_argument("--diff-threshold",
                        dest="diff_threshold",
                        type=int,
                        help="threshold to detect an anormal behaviour in a boid surrounding")
    parser.add_argument("--view-dist",
                        dest="view_dist",
                        type=int,
                        default=0,
                        help="define the view distance of the boids")
    # blindspot group
    blindspot_group = parser.add_argument_group('blindspot','blindspots description group')
    blindspot_group.add_argument("--blindspot-direction",
                                "-bsd",
                                type=int,
                                nargs='+',
                                dest="blindspot_direction",
                                help="list of directions of the bisector of each blindspot angle")
    blindspot_group.add_argument("--blindspot-opening",
                                "-bso",
                                type=int,
                                nargs='+',
                                help="list of the openings of each blindspot")

    # boids caracteristics
    parser.add_argument("-tr", "--turning-rate",
                        dest="turning_rate",
                        type=int,
                        default=BOID_TURN_SPEED,
                        help=f"the turning speed of boids in the simulation (default to {BOID_TURN_SPEED})")
    parser.add_argument("-bv", "--boid-velocity",
                        dest="boid_speed",
                        type=int,
                        default=BOID_VEL,
                        help=f"the velocity of boids in the simulation (default to {BOID_VEL}")
    parser.add_argument("--error",
                        dest="error_params",
                        type=str,
                        default="0,1",
                        help="Parameters of the gaussian distribution used in noises of the simulation")

    args = parser.parse_args()
    return args
