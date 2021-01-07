#!/usr/bin/python3.8
from math import pi
import os
import subprocess


def run_memory_exp(nb_repeat, name, cmd):
    # Create the required folders
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists(f"logs/{name}"):
        os.mkdir(f"logs/{name}")

    # Log the configuration
    with open("logs/memory/cmd_template.txt", "w") as cmd_log:
        cmd_log.write(cmd)

    # Repeat the simulation
    for i in range(nb_repeat):
        print("[Memory experience] Progression: {}%".format(i * 100 // nb_repeat))
        itr_cmd = cmd + " --output {}/itr_{}".format(name, i)
        process = subprocess.Popen(itr_cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
    print("[Memory experience] Done !")


if __name__ == '__main__':
    nb_repeat = 15
    name = "memory"
    cmd = "python3.8 -m src " \
          "--border none " \
          "-n 100 " \
          "-ror 1 " \
          "-roo-var 1:0.25:2.25 " \
          "--roo-step-duration 2000 " \
          "-roa 14 " \
          "--blindspot-direction -180 " \
          "--blindspot-opening 90 " \
          "--turning-rate 40 " \
          "--boid-velocity 3 " \
          f"-d-sd {0.05 / pi * 180} "

    run_memory_exp(nb_repeat, name, cmd)
