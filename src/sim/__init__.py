# -*- coding: utf-8 -*-
from os.path import join

DEFAULT_VIEW_DIST = 80.0
DEFAULT_NUM_NEIGHBORS = 5
BOID_NOSE_LEN = 1  # in length units
BOID_TURN_SPEED = 1  # in units per seconds
VELOCITY = 10  # in degrees per seconds

OUT_DIR = join("..", "out", "")
PALETTE = {
    "background": "#0B182A",
    "highlight": "#F87060",
    "accents": ["#EFC7C2", "#CDD7D6", "#FFE5D4"],
}

from .canvas import Canvas
from .incrementor import Incrementor
from .individual import Individual
from .population import Population
from .universe import Universe
