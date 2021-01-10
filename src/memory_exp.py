#!/usr/bin/python3.8
from math import pi
import os
from sim.sim import Sim
from sim.arguments import getArgs


def run_memory_exp(nb_repeat, name, cmd):
    # Create the required folders
    if not os.path.exists("../logs"):
        os.mkdir("../logs")
    if not os.path.exists(f"../logs/{name}"):
        os.mkdir(f"../logs/{name}")

    # Log the configuration
    with open(f"../logs/{name}/cmd_template.txt", "w") as cmd_log:
        cmd_log.write(cmd)

    # Repeat the simulation
    for i in range(nb_repeat):
        print("[Memory experience] Progression: {}%".format(i * 100 // nb_repeat))
        itr_cmd = cmd + " --output {}/itr_{}".format(name, i)
        args = getArgs(itr_cmd.split(" "))
        sim = Sim()
        sim.from_args(args)
    print("[Memory experience] Done !")


if __name__ == "__main__":
    nb_repeat = 10 #15
    name = "memory"
    cmd = (
        "--border none "
        "-n 60 "
        "-ror 1 "
        "-roo-var 1:0.25:4.25 " #1:0.25:4.25
        "--roo-step-duration 500 "
        "-roa 14 "
        "--blindspot-direction -180 "
        "--blindspot-opening 90 "
        "--turning-rate 40 "
        "--velocity 3 "
        f"-d-sd {0.05 / pi * 180}"
    )

    run_memory_exp(nb_repeat, name, cmd)
