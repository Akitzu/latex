import matplotlib.pyplot as plt
plt.style.use('lateky')
import numpy as np
from pathlib import Path
import argparse

def plot_poincare_pyoculus(xydata, ax):
    rdata, zdata = xydata
    for rs, zs in zip(rdata, zdata):
        ax.scatter(rs, zs, marker=".", color="black", s=1)
    ax.set_xlabel(r"R")
    ax.set_ylabel(r"Z")
    return ax.get_figure(), ax

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute the Poincare plot from the poincare data.")
    args = parser.parse_args()

    import os
    os.chdir("squared-profile")

    xydata = np.load("poincare.npy")
    fig, ax = plt.subplots()
    plot_poincare_pyoculus(xydata, ax)
    fig.savefig("poincare.pdf")
    plt.show()

    os.chdir("..")