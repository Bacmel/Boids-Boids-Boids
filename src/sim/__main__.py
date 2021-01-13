#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from .sim import Sim
from . import arguments as argu

if __name__ == "__main__":
    args = argu.get_args()
    sim = Sim()
    sim.from_args(args)
