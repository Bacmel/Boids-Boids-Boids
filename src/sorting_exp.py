#!/usr/bin/python3.8
from math import pi
import os
import subprocess

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

    for var_name, var_pattern, var_range in variable:
        for val in var_range:
            param_cmd = cmd + " " + var_pattern.format(val)

            # Repeat the simulation
            for i in range(nb_repeat):
                print(
                    "[Sorting experience] Variable: {} = {} - Repeat: {}%".format(var_name, val, i * 100 // nb_repeat))
                itr_cmd = param_cmd + " --output {}/{}_{}_itr_{}".format(name, var_name, val, i)
                process = subprocess.Popen(itr_cmd, shell=True, stdout=subprocess.PIPE)
                process.wait()
    print("[Memory experience] Done !")


if __name__ == '__main__':
    nb_repeat = 30
    name = "sorting"
    cmd = "python3.8 -m sim " \
          "--border none " \
          "-n 100 " \
          "-ror 1 " \
          "-roo 6 " \
          "-roa 14 " \
          "--blindspot-direction -180 " \
          "--blindspot-opening 90 " \
          "--turning-rate 40 " \
          "--velocity 3 " \
          f"-d-sd {0.05 / pi * 180} " \
          "--step-nb 5000 "

    speed_sd_range = np.array([0.0125, 0.025, 0.05, 0.1, 0.15, 0.2])
    turning_rate_range = np.arange(1, 10, 2)
    roa_range = np.arange(0.5, 2.75, 0.25)
    roo_range = np.arange(0.05, 0.35, 0.05)
    ror_range = np.arange(0.5, 2.75, 0.25)

    variable = [
        ("speed-sd", "--speed-sd {}", speed_sd_range),
        ("tr-sd", "--tr-sd {}", turning_rate_range),
        ("ror-sd", "--ror-sd {}", ror_range),
        ("roo-sd", "--roo-sd {}", roo_range),
        ("roa-sd", "--roa-sd {}", roa_range)
    ]

    run_sorting_exp(nb_repeat, name, cmd, variable)
