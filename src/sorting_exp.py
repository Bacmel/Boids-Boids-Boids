#!/usr/bin/python3.8
from math import pi
import os
from sim.sim import Sim
from sim.arguments import getArgs

import numpy as np


def run_sorting_exp(nb_repeat, name, cmd, variable):
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
        for var_name, var_pattern, var_range in variable:
            for val in var_range:
                param_cmd = cmd + " " + var_pattern.format(val)
                print(
                    "[Sorting experience] Variable: {} = {} - Repeat: {}%".format(
                        var_name, val, i * 100 // nb_repeat
                    )
                )
                itr_cmd = param_cmd + " --output {}/{}_{}_itr_{}".format(
                    name, var_name, val, i
                )
                args = getArgs(itr_cmd.split(" "))
                sim = Sim()
                sim.from_args(args)
    print("[Sorting experience] Done !")


if __name__ == "__main__":
    nb_repeat = 10 #15
    name = "sorting"
    cmd = (
        "--border none "
        "-n 60 "
        "-ror 1 "
        "-roo 6 "
        "-roa 14 "
        "--blindspot-direction -180 "
        "--blindspot-opening 90 "
        "--turning-rate 40 "
        "--velocity 3 "
        f"-d-sd {0.05 / pi * 180} "
        "--step-nb 500" #5000
    )

    speed_sd_range = np.array([0.0125, 0.05, 0.1, 0.15, 0.2]) #[0.0125, 0.025, 0.05, 0.1, 0.15, 0.2]
    turning_rate_range = np.arange(1, 10, 2)
    roa_range = np.arange(0.05, 0.35, 0.05) # 0.05, 0.35, 0.05
    roo_range = np.arange(0.5, 3, 0.5) # 0.5, 2.5, 0.25
    ror_range = np.arange(0.05, 0.35, 0.05) # 0.05, 0.35, 0.05

    variable = [
        ("speed-sd", "--speed-sd {}", speed_sd_range),
        ("tr-sd", "--tr-sd {}", turning_rate_range),
        ("ror-sd", "--ror-sd {}", ror_range),
        ("roo-sd", "--roo-sd {}", roo_range),
        ("roa-sd", "--roa-sd {}", roa_range),
    ]

    run_sorting_exp(nb_repeat, name, cmd, variable)
