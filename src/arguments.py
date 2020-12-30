from argparse import ArgumentParser, ArgumentTypeError
from src import PALETTE, DEFAULT_NUM_NEIGHBORS, DEFAULT_VIEW_DIST, BOID_TURN_SPEED, BOID_VEL

def blindspotCond(directions, openings):
    """
    Verify if the directions argument and openings argument make sense.

    Args:
        directions (list<int>): list of int representing the direction of a blind spot.
        openings (list<int>): list of int representing the opening of a blind spot.

    Raise an argparse.ArugmentTypeError when the condition is not respected.
    """
    if directions == None and openings == None:
        print("***WARNING: in arguments: no blindspot specified")
    elif not(directions and openings):
        raise ArgumentTypeError("***ERROR: wrong arguments: miss either blindspot direction or blingspot opening")
    elif len(directions) != len(openings):
        raise ArgumentTypeError("***ERROR: wrong arguments: length of blindspot direction different than length of blindspot opening")

# vitesse x pas de temps < rayon de répulsion
def globalCond(velocity, time_step, repulsion_radius):
    """
    Global condition on the simulation.

    Args:
        velocity (int): The velocity of the particuls
        time_step (float): The time increment of each step in the simulation time
        repulsion_radius (int): The radius where particuls repulse each others.
    
    Raise an argparse.ArgumentTypeError when velocity * time_step > repulsion_radius
    """
    if not(velocity * time_step < repulsion_radius):
        raise ArgumentTypeError("***ERROR: global condition of the simulation: velocity * time_step > repulsion_radius when it should not.")

def perceptionCond(view_dist, bs_direction, bs_opening, knn, outlier):
    """
    Conditions on the creation of perception.

    Args:
        view_dist (int): The view distance of each particule
        bs_direction (list<int>): List of angular position value representing the bisector of a blindspot.
        bs_opening (list<int>): List of angle value representing the opening of a blind spot.
        knn (int): the number of neighbors a particul can take into acount.
        outlier (int): The threshold to detect an anormal behaviour in a boid surrounding.

    Raise an argparse.ArgumentTypeError when no perceptions will be created due to lack of arguments.
    """
    if (view_dist and bs_direction and bs_opening and knn and outlier) is None:
        raise ArgumentTypeError("***ERROR: not enough arguments: use either argument --view-dist, -bsd & -bso, --count, --diff-threshold.")

def gaussCond(params):
    """
    Conditions on the parameters of the gaussian law for errors.

    Args:
        params (str): define the mean and standard deviation.
    
    Raise an argparse.ArgumentTypeError when the argument is not correctly defined.
    """
    if ":" not in params or len(params.split(":")!=2):
        raise ArgumentTypeError("***ERROR: wrong argument: --error must follow 'mu:std' format.")

def getArgs():
    """
    Standard function to specify the default value of the hyper-parameters of experimental setups
    
    Return:
        parsed args: the complete list of arguments
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
    parser.add_argument("--time-step",
                        dest="time_step",
                        type=float,
                        default=0.1,
                        help="time step for the update of the simulation")
    parser.add_argument("--render",
                        action='store_true',
                        help="allow visual rendering during the simulation")
    parser.add_argument("--verbose",
                        action='store_true',
                        help="increase output verbosity")

    # weights
    parser.add_argument("-roa", "--attraction",
                        dest="attraction_radius",
                        type=int,
                        default=1,
                        help="the radius of the attraction zone of each boid")
    parser.add_argument("-roo", "--orientation",
                        dest="orientation_radius",
                        type=int,
                        default=1,
                        help="the radius of the orientation zone of each boid")
    parser.add_argument("-ror", "--repulsion",
                        dest="repulsion_radius",
                        type=int,
                        default=1,
                        help="the radius of the replusion zone of each boid")

    # behaviour near edges
    parser.add_argument("--border",
                        type=str,
                        # toric world, wall delimitation, no edges
                        choices=["wrap", "wall", "none"],
                        default="wall",
                        help="selection of the border of the univers: toric world, wall with collisions or no edges at all")

    # what method to use to decide which boids are close ('nearby')
    parser.add_argument("--count",
                        dest="num_neighbors",
                        type=int,
                        help=f"the COUNT closest boids are seen by the current boid (defaults to {DEFAULT_NUM_NEIGHBORS})")
    parser.add_argument("--diff-threshold",
                        dest="diff_threshold",
                        type=int,
                        help="threshold to detect an anormal behaviour in a boid surrounding")
    parser.add_argument("--view-dist",
                        dest="view_dist",
                        type=int,
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
                                dest="blindspot_opening",
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
                        default="0:1",
                        help="Parameters of the gaussian distribution used in noises of the simulation")

    args = parser.parse_args()
    return args