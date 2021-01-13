#!/usr/bin/python3.8
from math import pi
import os
from sim.sim import Sim
from sim.arguments import get_args


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
        args = get_args(itr_cmd.split(" "))
        sim = Sim()
        sim.from_args(args)
    print("[Memory experience] Done !")


if __name__ == "__main__":
    nb_repeat = 1 #15
    name = "memory_try2"
    cmd = (
        "--border none "
        "-n 60 "
        "-ror 1 "
        "-roo-var 5:0.5:11.5 "
        "--roo-step-duration 500 "
        "-roa 14 "
        "--blindspot-direction -180 "
        "--blindspot-opening 90 "
        "--turning-rate 40 "
        "--velocity 3 "
        "-d-sd 0.05"
    )

    run_memory_exp(nb_repeat, name, cmd)
