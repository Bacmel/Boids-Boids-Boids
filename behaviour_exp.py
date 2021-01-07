#!/usr/bin/python3.8
import os
import subprocess


def run_memory_exp(nb_repeat, name, cmd, ror, droo_range, droa_range):
    # Create the required folders
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists(f"logs/{name}"):
        os.mkdir(f"logs/{name}")

    # Log the configuration
    with open("logs/memory/cmd_template.txt", "w") as cmd_log:
        cmd_log.write(cmd)
        cmd_log.write(f"ror: {ror}, droo_range: {droo_range}, droa_range: {droa_range}")

        # Repeat the simulation
        for droo in droo_range:
            roo = ror + droo
            for droa in droa_range:
                roa = roo + droa
                full_cmd = cmd.format(ror, roa, roo)
                for i in range(nb_repeat):
                    print(f"[Behaviour experience] droo: {droo} droa: {droa} - Progression: {i * 100 // nb_repeat}%")
                    itr_cmd = full_cmd + " --output {}/droo_{}_droa_{}_itr_{}".format(name, droo, droa, i)
                    process = subprocess.Popen(itr_cmd, shell=True, stdout=subprocess.PIPE)
                    process.wait()
    print("[Behaviour experience] Done !")


if __name__ == '__main__':
    nb_repeat = 5
    name = "behaviour"
    cmd = "python3.8 -m src " \
          "--border none " \
          "--turning-rate 50 " \
          "--boid-velocity 5 " \
          "--error 0:10 " \
          "-ror {} " \
          "-roa {} " \
          "-roo {} " \
          "--blindspot-direction -180 " \
          "--blindspot-opening 90 " \
          "--step-nb 1600"

    ror = 1
    droo_range = range(0, 15, 2)
    droa_range = range(0, 15, 2)

    run_memory_exp(nb_repeat, name, cmd, ror, droo_range, droa_range)
