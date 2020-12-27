from os.path import join
import numpy as np


DEFAULT_VIEW_DIST = 80.0
DEFAULT_NUM_NEIGHBORS = 5

BOID_VEL = 90
BOID_NOSE_LEN = 20
BOID_TURN_SPEED = 3.6

OUT_DIR = join(".", "out", "")
SCALE = 1.0  # in px/unit
PALETTE = {  # in bgr (expected by opencv)
    "background": (0x2A, 0x18, 0x0B),
    "highlight": (0x60, 0x70, 0xF8),
    "accents": [(0xC2, 0xC7, 0xEF), (0xD6, 0xD7, 0xCD), (0xD4, 0xE5, 0xFF)],
}


from src.boid import Boid
from src.canvas import Canvas
from src.universe import Universe
from src.arguments import getArgs
from src.population import Population
