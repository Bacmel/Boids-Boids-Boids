import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

### Get Logs ###
path = "logs/"
dirs = os.listdir(path)

quantities_logs = []
poses_logs = []

for dir in dirs:
    files = os.listdir(path + dir + "/")
    for file in files:
        if "poses" in file:
            poses_logs.append(path + dir + "/" + file)
        elif "quantities" in file:
            quantities_logs.append(path + dir + "/" + file)

### Get DataFrame ###
data_cb = pd.DataFrame(columns=["pgroupM", "pgroupQ1", "pgroupQ3", "mgroupM", "mgroupQ1", "mgroupQ3", "droo", "droa"])
data_hbt = pd.DataFrame(columns=["pgroup", "mgroup", "roo", "sens"])
data_ss = pd.DataFrame(
    columns=[
        "rho_sf",
        "rho_sc",
        "speed",
        "rho_thetaf",
        "rho_thetac",
        "turning_rate",
        "rho_rorf",
        "rho_rorc",
        "ror",
        "rho_roof",
        "rho_rooc",
        "roo",
    ]
)

for poses, quantities in zip(poses_logs, quantities_logs):
    pass






def get_cb(quantities):
    

def get_hbt(poses, quantities):
    pass

def get_ss(poses, quantities):
    pass

    