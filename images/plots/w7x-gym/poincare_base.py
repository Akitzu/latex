#!/usr/bin/env python

import time
import os
import logging
from pathlib import Path
import numpy as np
import simsoptpp as sopp
from simsopt.geo import SurfaceRZFourier # CurveHelical, CurveXYZFourier, curves_to_vtk
from simsopt.field import BiotSavart
from simsopt.field import (InterpolatedField, SurfaceClassifier, particles_to_vtk,
                           LevelsetStoppingCriterion, load_coils_from_makegrid_file,
                           MinRStoppingCriterion, MaxRStoppingCriterion,
                           MinZStoppingCriterion, MaxZStoppingCriterion,
                           compute_fieldlines
                           )
from simsopt.util import proc0_print, comm_world
from simsopt.field import Current, coils_via_symmetries
from simsopt.configs import get_w7x_data
from pyoculus.problems import SimsoptBfieldProblem
from pyoculus.solvers import FixedPoint
import matplotlib.pyplot as plt
from horus import poincare

###############################################################################
# Define the W7X cpnfiguration.
###############################################################################

nfp = 5  # Number of field periods
curves, currents, ma = get_w7x_data()

# GYM00+1750 currents
currents = [Current(1.109484) * 1e6 for _ in range(5)]
currents.append(Current(-0.3661) * 1e6)
currents.append(Current(-0.3661) * 1e6)

coils = coils_via_symmetries(curves, currents, 5, True)

R0, _, Z0 = ma.gamma()[0,:]
bs = BiotSavart(coils)
ps = SimsoptBfieldProblem.without_axis([5.98, 0], nfp, bs)
R0, Z0 = ps._R0, ps._Z0
ps = SimsoptBfieldProblem(R0=R0, Z0=Z0, Nfp=nfp, mf=bs, interpolate=True, ncoils=7, mpol=7, ntor=7, n=40)

###############################################################################
# Poincare plot
###############################################################################

proc0_print("Computing the Poincare plot")
phis = [(i)*(2*np.pi/nfp) for i in range(nfp)]

nfieldlines = 60
p1 = np.array([ps._R0, ps._Z0])
p2 = np.array([5.73, -0.669])
Rs = np.linspace(p1[0], p2[0], nfieldlines)
Zs = np.linspace(p1[1], p2[1], nfieldlines)
RZs = np.array([[r, z] for r, z in zip(Rs.flatten(), Zs.flatten())])

nfieldlines = 10
p1 = np.array([5.6144507858315915, -0.8067790944375764])
p2 = np.array([5.78, -0.6])
Rs = np.linspace(p1[0], p2[0], nfieldlines)
Zs = np.linspace(p1[1], p2[1], nfieldlines)
Rs, Zs = np.meshgrid(Rs, Zs)
RZs2 = np.array([[r, z] for r, z in zip(Rs.flatten(), Zs.flatten())])

RZs = np.concatenate((RZs, RZs2))

# Poincare plot
logging.basicConfig()
logger = logging.getLogger('simsopt.field.tracing')
logger.setLevel(1)

pplane = poincare(ps._mf_B, RZs, phis, ps.surfclassifier, tmax = 10000, tol = 1e-13, plot=False, comm=comm_world)
fig, ax = pplane.plot([0])
ax = ax[0,0]

pplane.save("poincare.pkl")
plt.show()