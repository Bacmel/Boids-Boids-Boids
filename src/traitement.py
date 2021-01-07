import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

### Get Logs ###
path = "logs/"
dirs = os.listdir(path)
#dirs = ["07-01-2021_11-40-38"]
analysis = "sorting"

quantities_logs = []
state_logs = []

for dire in dirs:
    files = os.listdir(path + dire + "/")
    for file in files:
        if "state" in file:
            state_logs.append(path + dire + "/" + file)
        elif "quantities" in file:
            quantities_logs.append(path + dire + "/" + file)

for ind, state_log, quantities_log in zip(range(len(state_logs)), state_logs, quantities_logs):
    state = pd.read_csv(state_log)
    quantities = pd.read_csv(quantities_log)
    if analysis == "sorting":
        if ind == 0:
            if 
            pgroup = {}
            mgroup = {}
        droo = quantities.loc[0]["roo"]-quantities.loc[0]["ror"]
        droa = quantities.loc[0]["roa"]-quantities.loc[0]["roo"]
        if (droo, droa) not in pgroup :
            pgroup[droo, droa] = []
            mgroup[droo, droa] = []
        pgroup[droo, droa].append(quantities.loc[0]["pgroup"])
        mgroup[droo, droa].append(quantities.loc[0]["mgroup"])
# Affichage
if analysis == "sorting":
    # pgroup
    droo, droa = zip(*pgroup.keys()) 
    # we have to unpack the dictionary values into two variables, b and c 
    p = np.median(np.array(list(pgroup.values())), axis=0) 
    # Now plotting 
    fig = plt.figure() 
    pr = fig.gca(projection='3d') 
    pr.plot_trisurf(droo, droa, p)
    # mgroup
    plt.show()


'''
### Traitement ###

if sys.argv[1] == "memory":
    for i in data_hbt["is_roo_rising"]:
            if i : ## Croissant

    .quantile([.25, .5, .75])


def get_cb(datas, quantities):
    csv = pd.read_csv(quantities)
    pgroup = csv['pgroup'].to_numpy()
    mgroup = csv['mgroup'].to_numpy()
    data = {
            "pgroup": np.median(pgroup[len(pgroup)//2:]),
            "mgroup": np.median(mgroup[len(pgroup)//2:]),
            "droa": csv.get_value(0, "roa")-csv.get_value(0, "roo"),
            "droo": csv.get_value(0, "roo")-csv.get_value(0, "ror"),
        }
    return datas.append(data, ignore_index=True)

def get_hbt(datas, quantities):
    csv = pd.read_csv(quantities)
    for i in range(len(csv["roo"])):
        sens = np.sign(csv.get_value(i,'roo')-csv.get_value(i-1,'roo')) or 0
        if sens != 0:
            data = {
                "pgroup": csv.get_value(i, "pgroup"),
                "mgroup": csv.get_value(i, "mgroup"),
                "roo": csv.get_value(i, "roo"),
                "sens": sens,}
            datas = datas.append(data, ignore_index=True) 
    return datas

def get_ss(datas, poses):
    csv = pd.read_csv(poses)
    csv_
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
    data = {
            "rho_sf": np.transpose(csv['pgroup'].to_numpy()),
            "rho_sc": np.transpose(csv['mgroup'].to_numpy()),
            "speed": np.transpose(csv['roo'].to_numpy()),
            "rho_thetaf": np.transpose(np.array(sens)),
        }
    return datas.append(data, ignore_index=True)'''
    
'''### Get DataFrame ###
data_cb = pd.DataFrame(columns=["pgroup", "mgroup", "droo", "droa"])
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
)'''

def plot_memory(quantities_logs):
    for ind, quantities_log in zip(range(len(quantities_logs)), quantities_logs):
        quantities = pd.read_csv(quantities_log)
        if ind == 0:
            r_d = quantities.loc[quantities["is_roo_rising"]==0]["roo"].to_numpy()
            nb_d = len(r_d)
            r_c = quantities.loc[quantities["is_roo_rising"]==1]["roo"].to_numpy()
            r_c = np.hstack((r_c, r_d[0])) # + valeur finale
            nb_c = len(r_c)
            p_c = np.zeros((1,nb_c))
            p_d = np.zeros((1,nb_d))
            m_c = np.zeros((1,nb_c))
            m_d = np.zeros((1,nb_d))
        else :
            p_c = np.vstack((p_c, np.zeros((1,nb_c))))
            p_d = np.vstack((p_d, np.zeros((1,nb_d))))
            m_c = np.vstack((m_c, np.zeros((1,nb_c))))
            m_d = np.vstack((m_d, np.zeros((1,nb_d))))
        for i in range(len(quantities["roo"])): # Le bonheur commence ici.
            if i < nb_c: # Cas croissant
                p_c[ind,i] = quantities.loc[i]["pgroup"]
                m_c[ind,i] = quantities.loc[i]["mgroup"]
            if i>=nb_c-1: # Cas décroissant
                p_d[ind,i-nb_c+1] = quantities.loc[i]["pgroup"]
                m_d[ind,i-nb_c+1] = quantities.loc[i]["mgroup"]
    # Affichage
    # pgroup
    med_p_c = np.median(p_c, axis=0)
    q_p_c = np.quantile(p_c, [.25, .75], axis=0)
    e_p_c = np.array([med_p_c-q_p_c[0,:],q_p_c[1,:]-med_p_c])
    med_p_d = np.median(p_d, axis=0)
    q_p_d = np.quantile(p_d, [.25, .75], axis=0)
    e_p_d = np.array([med_p_d-q_p_d[0,:],q_p_d[1,:]-med_p_d])
    plt.errorbar(r_c, med_p_c, yerr=e_p_c, label="Croissant", markersize=8, capsize=20)
    plt.errorbar(r_d, med_p_d, yerr=e_p_d, label="Décroissant", markersize=8, capsize=20)
    plt.legend(loc="lower right")
    plt.figure()
    # mgroup
    med_m_c = np.median(m_c, axis=0)
    q_m_c = np.quantile(m_c, [.25, .75], axis=0)
    e_m_c = np.array([med_m_c-q_m_c[0,:],q_m_c[1,:]-med_m_c])
    med_m_d = np.median(m_d, axis=0)
    q_m_d = np.quantile(m_d, [.25, .75], axis=0)
    e_m_d = np.array([med_m_d-q_m_d[0,:],q_m_d[1,:]-med_m_d])
    plt.errorbar(r_c, med_m_c, yerr=e_m_c, label="Croissant", markersize=8, capsize=20)
    plt.errorbar(r_d, med_m_d, yerr=e_m_d, label="Décroissant", markersize=8, capsize=20)
    plt.legend(loc="lower right")
    plt.show()

def plot_behaviours(quantities_logs):
    for ind, quantities_log in zip(range(len(quantities_logs)), quantities_logs):
        quantities = pd.read_csv(quantities_log)
        if ind == 0:
            pgroup = {}
            mgroup = {}
        droo = quantities.loc[0]["roo"]-quantities.loc[0]["ror"]
        droa = quantities.loc[0]["roa"]-quantities.loc[0]["roo"]
        if (droo, droa) not in pgroup :
            pgroup[droo, droa] = []
            mgroup[droo, droa] = []
        pgroup[droo, droa].append(quantities.loc[0]["pgroup"])
        mgroup[droo, droa].append(quantities.loc[0]["mgroup"])
    # Affichage
    # pgroup
    droo, droa = zip(*pgroup.keys()) 
    p = np.median(np.array(list(pgroup.values())), axis=0) 
    # Now plotting 
    fig = plt.figure() 
    pr = fig.gca(projection='3d') 
    pr.plot_trisurf(droo, droa, p)
    # mgroup
    droo, droa = zip(*mgroup.keys()) 
    m = np.median(np.array(list(mgroup.values())), axis=0) 
    # Now plotting 
    fig = plt.figure() 
    pr = fig.gca(projection='3d') 
    pr.plot_trisurf(droo, droa, m)
    plt.show()