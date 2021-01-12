#!/usr/bin/python3.8
from math import pi
import os
from sim.sim import Sim
from sim.arguments import getArgs
import numpy as np


def run_behaviour_exp(nb_repeat, name, a, ror, droo_range, droa_range):
    # Create the required folders
    if not os.path.exists("../logs"):
        os.mkdir("../logs")
    if not os.path.exists(f"../logs/{name}"):
        os.mkdir(f"../logs/{name}")

    # Log the configuration
    with open(f"../logs/{name}/cmd_template.txt", "w") as cmd_log:
        cmd_log.write(a)
        cmd_log.write(f"ror: {ror}, droo_range: {droo_range}, droa_range: {droa_range}")

        # Repeat the simulation
        for i in range(nb_repeat):
            for droo in droo_range:
                roo = ror + droo
                for droa in droa_range:
                    roa = roo + droa
                    full_cmd = a.format(ror, roo, roa)
                    print(
                        f"[Behaviour experience] droo: {droo} droa: {droa} - Progression: {i * 100 // nb_repeat}%"
                    )
                    itr_cmd = full_cmd + " --output {}/droo_{}_droa_{}_itr_{}".format(
                        name, droo, droa, i
                    )
                    a = getArgs(itr_cmd.split(" "))
                    sim = Sim()
                    sim.from_args(a)
    print("[Behaviour experience] Done !")


if __name__ == "__main__":
    nb_repeat = 5
    name = "behaviour"
    cmd = (
        "--border none "
        "-n 60 "
        "-ror {} "
        "-roo {} "
        "-roa {} "
        "--blindspot-direction -180 "
        "--blindspot-opening 90 "
        "--turning-rate 40 "
        "--velocity 3 "
        f"-d-sd {0.05} "
        "--step-nb 500"
    )

    ror = 1
    droo_range = np.arange(0, 16, 2) #0, 14.5, 0.5
    droa_range = np.arange(0, 16, 2) #0, 14.5, 0.5

    run_behaviour_exp(nb_repeat, name, cmd, ror, droo_range, droa_range)
