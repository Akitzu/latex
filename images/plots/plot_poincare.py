import matplotlib.pyplot as plt
plt.style.use('lateky')
import numpy as np
from pathlib import Path
import argparse
from horus import PoincarePlanes
import pickle

def plot_poincare_pyoculus(xydata, ax, xlims = [3.5, 9.2], ylims = [-6, 2.5], **kwargs):
    options = {
        "color": "black",
        "s": 1,
        "linewidths": 1,
        "zorder": 10,
        "marker": ".",
    }
    options.update(kwargs)

    rdata, zdata = xydata
    for rs, zs in zip(rdata, zdata):
        ax.scatter(rs, zs, **options)

    if xlims is not None:
        ax.set_xlim(xlims)
    if ylims is not None:
        ax.set_ylim(ylims)

    ax.set_xlabel(r"R", fontsize=16)
    ax.set_ylabel(r"Z", fontsize=16)
    ax.set_aspect("equal")
    return ax.get_figure(), ax

def plot_poincare_simsopt(fieldlines_phi_hits, ax, idx=None, **kwargs):
    options = {
        "color": "black",
        "s": 1,
        "linewidths": 0,
        "zorder": 10,
        "marker": ".",
    }
    options.update(kwargs)

    for j in range(len(fieldlines_phi_hits)):
        if idx is None:
            where = np.where(fieldlines_phi_hits[j][:, 1] >= 0)[0]
        else:
            where = np.where(fieldlines_phi_hits[j][:, 1] == idx)[0]

        data_this_phi = fieldlines_phi_hits[j][
            where, :
        ]
        if data_this_phi.size == 0:
            continue
        r = np.sqrt(data_this_phi[:, 2] ** 2 + data_this_phi[:, 3] ** 2)
        ax.scatter(
            r, data_this_phi[:, 4], **options
        )
    
    ax.set_xlabel(r"R [m]")
    ax.set_ylabel(r"Z [m]")
    ax.set_aspect("equal")
    return ax.get_figure(), ax


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute the Poincare plot from the poincare data.")
    parser.add_argument("folder", help="Folder containing the poincare data.", default="squared-profile")
    parser.add_argument("-name", help="Name of the poincare data file.", default="poincare.npy")
    parser.add_argument("-simsopt", action="store_true", help="Use simsopt data")
    args = parser.parse_args()

    folder = Path(args.folder)

    fig, ax = plt.subplots()
    if args.simsopt:
        tys, phi_hits = pickle.load(open(folder / args.name, "rb"))
        phi_hits = [np.array(phis) for phis in phi_hits]
        plot_poincare_simsopt(phi_hits, ax)
    else:
        xydata = np.load(folder / args.name)
        plot_poincare_pyoculus(xydata, ax)
    
    plt.show()
    fig.savefig(folder / "poincare.pdf", bbox_inches="tight", pad_inches=0.1)
    fig.savefig(folder / "poincare.png", bbox_inches="tight", pad_inches=0.1)