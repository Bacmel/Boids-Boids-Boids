#!/usr/bin/python3.8

from math import pi
import os
from sim.sim import Sim
from sim.arguments import get_args
import numpy as np


def run_behaviour_exp(nb_repeat, name, cmd, ror, droo_range, droa_range):
    """Run the behaviour experience.

    Args:
        nb_repeat (int): The number of repetitions.
        name (str): The name of this experience.
        cmd (str): The command template to use.
        ror (float): The range of repulsion (in length units).
        droo_range (float): The range of values to explore with delta r_o (in length units).
        droa_range (float): The range of values to explore with delta r_a (in length units).
    """
    # Create the required folders
    if not os.path.exists("../logs"):
        os.mkdir("../logs")
    if not os.path.exists(f"../logs/{name}"):
        os.mkdir(f"../logs/{name}")

    # Log the configuration
    with open(f"../logs/{name}/cmd_template.txt", "w") as cmd_log:
        cmd_log.write(cmd)
        cmd_log.write(f"ror: {ror}, droo_range: {droo_range}, droa_range: {droa_range}")

        # Repeat the simulation
        for i in range(nb_repeat):
            for droo in droo_range:
                roo = ror + droo
                for droa in droa_range:
                    roa = roo + droa
                    full_cmd = cmd.format(ror, roo, roa)
                    print(
                        f"[Behaviour experience] droo: {droo} droa: {droa} - Progression: {i * 100 // nb_repeat}%"
                    )
                    itr_cmd = full_cmd + " --output {}/droo_{}_droa_{}_itr_{}".format(
                        name, droo, droa, i
                    )
                    ar = get_args(itr_cmd.split(" "))
                    sim = Sim()
                    sim.from_args(ar)
    print("[Behaviour experience] Done !")


if __name__ == "__main__":
    nb_repeat = 10
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
    droo_range = np.arange(0, 16, 2)
    droa_range = np.arange(0, 16, 2)

    run_behaviour_exp(nb_repeat, name, cmd, ror, droo_range, droa_range)
