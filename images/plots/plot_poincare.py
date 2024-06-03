import matplotlib.pyplot as plt
plt.style.use('lateky')
import numpy as np
from pathlib import Path
import argparse

def plot_poincare_pyoculus(xydata, ax):
    rdata, zdata = xydata
    for rs, zs in zip(rdata, zdata):
        ax.scatter(rs, zs, marker=".", color="black", s=1)

    ax.set_xlim(3.5, 9.2)
    ax.set_ylim(-6, 2.5)

    ax.set_xlabel(r"R")
    ax.set_ylabel(r"Z")
    return ax.get_figure(), ax

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute the Poincare plot from the poincare data.")
    parser.add_argument("folder", help="Folder containing the poincare data.", default="squared-profile")
    args = parser.parse_args()

    folder = Path(__file__).parent / args.folder

    xydata = np.load(folder / "poincare.npy")
    fig, ax = plt.subplots()
    plot_poincare_pyoculus(xydata, ax)
    plt.show()
    fig.savefig(folder / "poincare.pdf")