import matplotlib.pyplot as plt
plt.style.use('lateky')
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np

def plot_q_profile(r, q, ax):
    ax.plot(r, q, marker=".", linestyle="-", color="black")
    # ax.set_xlabel(r"Minor radius $\rho$")
    ax.set_ylabel(r"Safety factor $q$")
    return ax.get_figure(), ax

def plot_iota_profile(r, iota, ax):
    ax.plot(r, iota, marker=".", linestyle="-", color="black")
    ax.set_xlabel(r"Minor radius $\rho$")
    ax.set_ylabel(r"Rotationnal transform $\bar{\iota}$")
    return ax.get_figure(), ax

def plot_both(r, iota, q):
    pass

if __name__ == "__main__":
    import os
    os.chdir("squared-profile")
    r = np.loadtxt("r-squared.txt")
    q = np.loadtxt("q-squared.txt")
    iota = np.loadtxt("iota-squared.txt")

    fig, ax = plt.subplots()
    plot_iota_profile(r, iota, ax)
    axins = inset_axes(ax, width="100%", height="100%", 
                       bbox_to_anchor=(.1, .07, .4, .3),
                       bbox_transform=ax.transAxes, loc=3)
    plot_q_profile(r, q, axins)
    fig.savefig("q-iota-squared.pdf")

    plt.show()
    os.chdir("..")