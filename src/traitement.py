#!/usr/bin/python3.8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

### For Latex Render ###
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})

### Get Logs ###
path =
dirs = os.listdir(path)
analysis = ""


def get_logs(dirs):
    """Get log files.

    Args:
        dirs (list<string>): List of directories.

    Returns:
        list<string>: "quantities" log files.
        list<string>: "states" log files.
    """
    for dire in dirs:
        if not os.path.isdir(path + dire):
            continue
        files = os.listdir(path + dire + "/")
        for file in files:
            if "state" in file and file.endswith(".csv"):
                state_logs.append(path + dire + "/" + file)
            elif "quantities" in file and file.endswith(".csv"):
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
        c (numpy.ndarray): data of increasing case.
        d (numpy.ndarray): data of decreasing case.
        x_c (numpy.ndarray): absciss of increasing case.
        x_d (numpy.ndarray): absciss of decreasing case.
    """
    med_c, e_c = get_med_e(c)
    med_d, e_d = get_med_e(d)
    plt.errorbar(x_c, med_c, yerr=e_c, label="Croissant", markersize=8, capsize=5)
    plt.errorbar(x_d, med_d, yerr=e_d, label="Décroissant", markersize=8, capsize=5)
    plt.legend(loc="upper left", framealpha=0.5)


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
        for i in range(len(quantities["roo"])):
            if i < nb_c:  # Cas croissant
                p_c[ind, i] = quantities.loc[i]["pgroup"]
                m_c[ind, i] = quantities.loc[i]["mgroup"]
            if i >= nb_c - 1:  # Cas décroissant
                p_d[ind, i - nb_c + 1] = quantities.loc[i]["pgroup"]
                m_d[ind, i - nb_c + 1] = quantities.loc[i]["mgroup"]
    # Affichage
    # pgroup
    plot_c_d(p_c, p_d, r_c, r_d)
    plt.xlabel(r"Rayon d'orientation $r_o$(en unité de longueur)")
    plt.ylabel("Polarisation du groupe")
    plt.title("Polarisation du groupe en fonction du rayon d'orientation")
    plt.figure()
    # mgroup
    plot_c_d(m_c, m_d, r_c, r_d)
    plt.xlabel(r"Rayon d'orientation $r_o$(en unité de longueur)")
    plt.ylabel("Moment angulaire du groupe")
    plt.title("Moment angulaire du groupe en fonction du rayon d'orientation")
    plt.show()

def plot_3D(group, X, Y, title):
    """Plot behaviour graph.

    Args:
        group (dict<(float,float)><list<float> >): "group" data.
        X (numpy.ndarray): X meshgrid.
        Y (numpy.ndarray): Y meshgrid.
        title (string): title.
    """
    values = np.array([[np.median(group[a, b]) for a, b in zip(x, y)] for x, y in zip(X, Y)])
    fig = plt.figure()
    pr = fig.gca(projection="3d")
    pr.plot_surface(X, Y, values)
    pr.set_xlabel(r"\bf $\Delta r_o$")
    pr.set_ylabel(r"\bf $\Delta r_a$")
    pr.set_zlabel(title)
    pr.invert_xaxis()

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
    droo, droa = zip(*pgroup.keys())
    b = [element for element in set(droo)]
    c = [element for element in set(droa)]
    X, Y = np.meshgrid(b, c)
    # pgroup
    plot_3D(pgroup, X, Y, r"\bf $p_{group}$")
    plt.title(r'Polarisation du groupe')
    # mgroup
    plot_3D(mgroup, X, Y, r"\bf $m_{group}$")
    plt.title(r'Moment angulaire du groupe')
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


def plot_f_c(f, c):
    """Plot sorting graph.

    Args:
        f (dict<float><list<float> >): dictionnary for front data.
        c (dict<float><list<float> >): dictionnary for center data.
    """
    values = [(sd, f[sd], c[sd]) for sd in f.keys()]
    values.sort(key=lambda v: v[0])

    sd = np.array([sd for sd, _, _ in values])
    # Take the opposite as the index is decreasing with the position
    f_array = -np.array([f for _, f, _ in values])
    c_array = -np.array([c for _, _, c in values])

    med_f, e_f = get_med_e(np.transpose(f_array))
    med_c, e_c = get_med_e(np.transpose(c_array))

    plt.errorbar(sd, med_f, yerr=e_f, label="Front", markersize=8, capsize=5)
    plt.errorbar(sd, med_c, yerr=e_c, label="Centre", markersize=8, capsize=5)
    plt.legend(bbox_to_anchor=(1, 1), loc="lower right")


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
            rho_speed_f = {}
            rho_speed_c = {}
            rho_turning_f = {}
            rho_turning_c = {}
            rho_roo_f = {}
            rho_roo_c = {}
            rho_ror_f = {}
            rho_ror_c = {}
            rho_roa_f = {}
            rho_roa_c = {}
        data = state.corr(method="spearman")
        if quantities.loc[0]["speed_sd"] > 0:  # Cas Vitesse
            sd = quantities.loc[0]["speed_sd"]
            store(rho_speed_f, rho_speed_c, sd, data, r"$s$")
        if quantities.loc[0]["turning_rate_sd"] > 0:  # Cas Turning Rate
            sd = quantities.loc[0]["turning_rate_sd"]
            store(rho_turning_f, rho_turning_c, sd, data, r"$\theta$")
        if quantities.loc[0]["roo_sd"] > 0:  # Cas roo
            sd = quantities.loc[0]["roo_sd"]
            store(rho_roo_f, rho_roo_c, sd, data, r"$\Delta r_o$")
        if quantities.loc[0]["ror_sd"] > 0:  # Cas ror
            sd = quantities.loc[0]["ror_sd"]
            store(rho_ror_f, rho_ror_c, sd, data, r"$\Delta r_r$")
        if quantities.loc[0]["roa_sd"] > 0:  # Cas roa
            sd = quantities.loc[0]["roa_sd"]
            store(rho_roa_f, rho_roa_c, sd, data, r"$\Delta r_a$")
    # Affichage
    # speed
    if len(rho_speed_c) != 0:
        plt.figure()
        plot_f_c(rho_speed_f, rho_speed_c)
        plt.xlabel("Écart type sur la vitesse (en unité de longueur par secondes)")
        plt.ylabel("Coefficient de corrélation de Spearman")
    # turning
    if len(rho_turning_c) != 0:
        plt.figure()
        plot_f_c(rho_turning_f, rho_turning_c)
        plt.xlabel("Écart type sur la vitesse angulaire (en radians par secondes)")
        plt.ylabel("Coefficient de corrélation de Spearman")
    # roo
    if len(rho_roo_c) != 0:
        plt.figure()
        plot_f_c(rho_roo_f, rho_roo_c)
        plt.xlabel("Écart type sur le rayon d'orientation (en unité de longueur)")
        plt.ylabel("Coefficient de corrélation de Spearman")
    # ror
    if len(rho_ror_c) != 0:
        plt.figure()
        plot_f_c(rho_ror_f, rho_ror_c)
        plt.xlabel("Écart type sur le rayon de répulsion (en unité de longueur)")
        plt.ylabel("Coefficient de corrélation de Spearman")
    # roa
    if len(rho_roa_c) != 0:
        plt.figure()
        plot_f_c(rho_roa_f, rho_roa_c)
        plt.xlabel("Écart type sur le rayon d'attraction (en unité de longueur)")
        plt.ylabel("Coefficient de corrélation de Spearman")
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
