from pathlib import Path
import matplotlib.pyplot as plt
plt.style.use('lateky')
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import argparse

def plot_q_profile(r, q, ax, r_shift):
    r = r + r_shift
    ax.plot(r, q, marker=".", linestyle="-", color="black")
    # ax.set_xlabel(r"Minor radius $\rho$")
    ax.set_ylabel(r"Safety factor $q$", fontsize=16)
    return ax.get_figure(), ax

def plot_iota_profile(r, iota, ax, r_shift):
    r = r + r_shift
    ax.plot(r, iota, marker=".", linestyle="-", color="black")
    ax.set_xlabel(r"Minor radius $\rho$", fontsize=16)
    ax.set_ylabel(r"Rotationnal transform $\iota/2\pi$", fontsize=16)
    return ax.get_figure(), ax

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute the q/iota plot from the poincare data.")
    parser.add_argument("folder", help="Folder containing the poincare data.", default="squared-profile")
    # parser.add_argument("--bb", type=tuple, default=(.1, .07, .4, .3), help="bbox_to_anchor for the inset axes.")
    parser.add_argument("--r_shift", type=float, default=-6, help="Shift the minor radius.")
    args = parser.parse_args()

    folder = Path(args.folder)
    r = np.loadtxt(folder / "r-squared.txt")
    q = np.loadtxt(folder / "q-squared.txt")
    iota = np.loadtxt(folder / "iota-squared.txt")

    fig, ax = plt.subplots()
    # bbox = (.55, .6, .4, .35)
    bbox = (.15, .07, .4, .3)
    plot_iota_profile(r, iota, ax, r_shift=args.r_shift)
    axins = inset_axes(ax, width="100%", height="100%", 
                       bbox_to_anchor=bbox,
                       bbox_transform=ax.transAxes, loc=3)
    plot_q_profile(r, q, axins, r_shift=args.r_shift)
    plt.show()
    fig.savefig(folder / "q-iota-squared.pdf", bbox_inches="tight", pad_inches=0.1)
    fig.savefig(folder / "q-iota-squared.png", bbox_inches="tight", pad_inches=0.1)