#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from argparse import ArgumentTypeError
from math import ceil, pi
import time
import numpy as np
from .sim import Sim
from . import Canvas, Incrementor, PALETTE, Population, Universe, arguments as argu
from .borders import Infinite, Toric, Wall
from .data_logger import DataLogger
from .perceptions import BlindSpot, KNN, Outlier, Range

if __name__ == "__main__":
    args = argu.getArgs()
    sim = Sim()
    sim.from_args(args)
