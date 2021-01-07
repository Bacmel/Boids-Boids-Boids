#!/usr/bin/python3.8
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
    nb_repeat = 5
    name = "memory"
    cmd = "python3.8 -m src " \
          "--border none " \
          "--turning-rate 50 " \
          "--boid-velocity 5 " \
          "-d-sd 10 " \
          "-ror 1 " \
          "-roa 31 " \
          "--blindspot-direction -180 " \
          "--blindspot-opening 90 " \
          "--step-nb 1600 " \
          "-roo-var 1:0.25:2.25 " \
          "--roo-step-duration 20"

    run_memory_exp(nb_repeat, name, cmd)
