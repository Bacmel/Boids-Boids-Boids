import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

### Get Logs ###
path = "logs/"
dirs = os.listdir(path)
analysis = "sorting"


def get_logs(dirs):
    """Get log files.

    Args:
        dirs (list<string>): List of directories.

    Returns:
        list<string>: "quantities" log files.
        list<string>: "states" log files.
    """
    for dire in dirs:
        files = os.listdir(path + dire + "/")
        for file in files:
            if "state" in file:
                state_logs.append(path + dire + "/" + file)
            elif "quantities" in file:
                quantities_logs.append(path + dire + "/" + file)
    return quantities_logs, state_logs


def get_med_e(data):
    """Compute median and errors of dataset.

    Args:
        data (numpy.ndarray): dataset to study.

    Returns:
        numpy.ndarray: medians.
        numpy.ndarray: errors.
    """
    med = np.median(data, axis=0)
    q = np.quantile(data, [0.25, 0.75], axis=0)
    e = np.array([med - q[0, :], q[1, :] - med])
    return med, e


def plot_c_d(c, d, x_c, x_d):
    """Plot croissant and décroissant graph.

    Args:
        c (numpy.ndarray): data of croissant case.
        d (numpy.ndarray): data of décroissant case.
        x_c (numpy.ndarray): absciss of croissant case.
        x_d (numpy.ndarray): absciss of décroissant case.
    """
    med_c, e_c = get_med_e(c)
    med_d, e_d = get_med_e(d)
    plt.errorbar(r_c, med_c, yerr=e_c, label="Croissant", markersize=8, capsize=20)
    plt.errorbar(r_d, med_d, yerr=e_d, label="Décroissant", markersize=8, capsize=20)
    plt.legend(loc="lower right")


def plot_memory(quantities_logs):
    """Plot memory graph.

    Args:
        quantities_logs (list<string>): "quantities" log files.
    """
    for ind, quantities_log in zip(range(len(quantities_logs)), quantities_logs):
        quantities = pd.read_csv(quantities_log)
        if ind == 0:
            r_d = quantities.loc[quantities["is_roo_rising"] == 0]["roo"].to_numpy()
            nb_d = len(r_d)
            r_c = quantities.loc[quantities["is_roo_rising"] == 1]["roo"].to_numpy()
            r_c = np.hstack((r_c, r_d[0]))
            nb_c = len(r_c)
            p_c = np.zeros((1, nb_c))
            p_d = np.zeros((1, nb_d))
            m_c = np.zeros((1, nb_c))
            m_d = np.zeros((1, nb_d))
        else:
            p_c = np.vstack((p_c, np.zeros((1, nb_c))))
            p_d = np.vstack((p_d, np.zeros((1, nb_d))))
            m_c = np.vstack((m_c, np.zeros((1, nb_c))))
            m_d = np.vstack((m_d, np.zeros((1, nb_d))))
        for i in range(len(quantities["roo"])):  # Le bonheur commence ici.
            if i < nb_c:  # Cas croissant
                p_c[ind, i] = quantities.loc[i]["pgroup"]
                m_c[ind, i] = quantities.loc[i]["mgroup"]
            if i >= nb_c - 1:  # Cas décroissant
                p_d[ind, i - nb_c + 1] = quantities.loc[i]["pgroup"]
                m_d[ind, i - nb_c + 1] = quantities.loc[i]["mgroup"]
    # Affichage
    # pgroup
    plot_c_d(p_c, p_d, r_c, r_d)
    plt.figure()
    # mgroup
    plot_c_d(p_c, p_d, r_c, r_d)
    plt.show()


def plot_behaviours(quantities_logs):
    """Plot behaviours graph.

    Args:
        quantities_logs (list<string>): "quantities" log files.
    """
    for ind, quantities_log in zip(range(len(quantities_logs)), quantities_logs):
        quantities = pd.read_csv(quantities_log)
        if ind == 0:
            pgroup = {}
            mgroup = {}
        droo = quantities.loc[0]["roo"] - quantities.loc[0]["ror"]
        droa = quantities.loc[0]["roa"] - quantities.loc[0]["roo"]
        if (droo, droa) not in pgroup:
            pgroup[droo, droa] = []
            mgroup[droo, droa] = []
        pgroup[droo, droa].append(quantities.loc[0]["pgroup"])
        mgroup[droo, droa].append(quantities.loc[0]["mgroup"])
    # Affichage
    # pgroup
    droo, droa = zip(*pgroup.keys())
    p = np.median(np.array(list(pgroup.values())), axis=0)
    fig = plt.figure()
    pr = fig.gca(projection="3d")
    pr.plot_trisurf(droo, droa, p)
    # mgroup
    droo, droa = zip(*mgroup.keys())
    m = np.median(np.array(list(mgroup.values())), axis=0)
    fig = plt.figure()
    pr = fig.gca(projection="3d")
    pr.plot_trisurf(droo, droa, m)
    plt.show()


def store(f, c, sd, data, title):
    """Collect specific data.

    Args:
        f (dict<float><list<float> >): dictionnary for front data.
        c (dict<float><list<float> >): dictionnary for center data.
        sd (float): key of the dict.
        data (dataFrame): Book of unlimited knowledge of rho.
        title (string): specific data name.
    """
    if sd not in f:
        f[sd] = []
        c[sd] = []
    f[sd].append(data.loc[title]["front_idx"])
    c[sd].append(data.loc[title]["center_idx"])
    return f, c


def plot_f_c(f, c):
    sd = list(f.keys())
    med_f, e_f = get_med_e(np.array(list(f.values())))
    med_c, e_c = get_med_e(np.array(list(c.values())))
    plt.errorbar(sd, med_f, yerr=e_f, label="front", markersize=8, capsize=20)
    plt.errorbar(sd, med_c, yerr=e_c, label="center", markersize=8, capsize=20)
    plt.legend(loc="lower right")


def plot_sorting(state_logs, quantities_logs):
    """Plot sorting graph.

    Args:
        state_logs (list<string>): "states" log files.
        quantities_logs (list<string>): "quantities" log files.
    """
    for ind, state_log, quantities_log in zip(
        range(len(state_logs)), state_logs, quantities_logs
    ):
        state = pd.read_csv(state_log)
        quantities = pd.read_csv(quantities_log)
        if ind == 0:
            # Initialisation
            rho_speed_f = rho_speed_c = rho_turning_f = rho_turning_c = {}
            rho_roo_f = rho_roo_c = rho_ror_f = rho_ror_c = {}
        data = state.corr(method="spearman")
        if quantities.loc[0]["speed_sd"] != 0:  # Cas Vitesse
            sd = quantities.loc[0]["speed_sd"]
            rho_speed_f, rho_speed_c = store(
                rho_speed_f, rho_speed_c, sd, data, "speed"
            )
        if quantities.loc[0]["turning_rate_sd"] != 0:  # Cas Turning Rate
            sd = quantities.loc[0]["turning_rate_sd"]
            rho_turning_f, rho_turning_c = store(
                rho_turning_f, rho_turning_c, sd, data, "turning_rate"
            )
        if quantities.loc[0]["roo_sd"] != 0:  # Cas roo
            sd = quantities.loc[0]["roo_sd"]
            rho_roo_f, rho_roo_c = store(rho_roo_f, rho_roo_c, sd, data, "roo")
        if quantities.loc[0]["ror_sd"] != 0:  # Cas ror
            sd = quantities.loc[0]["ror_sd"]
            rho_ror_f, rho_ror_c = store(rho_ror_f, rho_ror_c, sd, data, "ror")
    # Affichage
    # speed
    plot_f_c(rho_speed_f, rho_speed_c)
    plt.figure()
    # turning
    plot_f_c(rho_turning_f, rho_turning_c)
    plt.figure()
    # roo
    plot_f_c(rho_roo_f, rho_roo_c)
    plt.figure()
    # ror
    plot_f_c(rho_ror_f, rho_ror_c)
    plt.show()


if __name__ == "__main__":
    quantities_logs = []
    state_logs = []

    quantities_logs, state_logs = get_logs(dirs)

    if "sorting" in analysis:
        plot_sorting(state_logs, quantities_logs)
    if "behaviours" in analysis:
        plot_behaviours(quantities_logs)
    if "memory" in analysis:
        plot_memory(quantities_logs)
