from os.path import join

DEFAULT_VIEW_DIST = 80.0
DEFAULT_NUM_NEIGHBORS = 5
BOID_NOSE_LEN = 1  # in units
BOID_TURN_SPEED = 1  # in units per seconds
BOID_VEL = 10  # in degrees per seconds

OUT_DIR = join(".", "out", "")
PALETTE = {  # in bgr (expected by opencv)
    "background": (0x2A, 0x18, 0x0B),
    "highlight": (0x60, 0x70, 0xF8),
    "accents": [(0xC2, 0xC7, 0xEF), (0xD6, 0xD7, 0xCD), (0xD4, 0xE5, 0xFF)],
}

from .individual import Individual
from .canvas import Canvas
from .population import Population
from .universe import Universe
from .incrementor import Incrementor