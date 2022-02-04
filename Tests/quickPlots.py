import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

from testNew import DGParameters
import lib.VDMSim as vdm
import lib.beamPDFs as beamPDFs
import lib.plotCode as plotter
import lib.pdfs as pdfs
import lib.jsonTools as jsonTools


beamParameters = DGParameters()

ScanSteps = np.linspace(-(25 - 1) / 2., (25 - 1) / 2., num=25, endpoint=True)

fig, (ax1, ax2) = plt.subplots(1,2)

file = jsonTools.openFile("Rates_HFOC_6016.json")
hfocData = jsonTools.getXandYData(file)

ax1.scatter(ScanSteps, hfocData[0], label="VdM data", s=15.)
ax2.scatter(ScanSteps, hfocData[1], label="VdM data", s=15.)

ax1.title.set_text('X-scan')
ax1.set_xlabel(r"$\Delta$ x [a.u.]")
ax1.set_ylabel(r"Rate")
ax1.grid(True, which="both")

ax2.title.set_text('Y-scan')
ax2.set_xlabel(r"$\Delta$ y [a.u.]")
ax2.set_ylabel(r"Rate")
ax2.grid(True, which="both")

ax1.set_yscale("log")
ax2.set_yscale("log")

plt.savefig("hfocRatesPlot.png")
plt.show()

fig, (axSing) = plt.subplots(1,1)
axSing.scatter(ScanSteps, hfocData[0], label="VdM data", s=15.)

#ax1.title.set_text('X-scan')
axSing.set_xlabel(r"$\Delta$ x [a.u.]")
axSing.set_ylabel(r"Rate")
axSing.grid(True, which="both")
axSing.set_yscale("log")

plt.savefig("hfocRatesPlotX.png")
plt.show()


dx, (xScan, yScan) = vdm.RunVdmScanSim(beamPDFs.DoubleGaussBeamOverlap, beamParameters, nSteps=25)

fig, (axVdM) = plt.subplots(1,1)

axVdM.scatter(ScanSteps, xScan[2], s=15., label="X")

#ax1.title.set_text('X-scan')
axVdM.set_xlabel(r"$\Delta$ x [a.u.]")
axVdM.set_ylabel(r"Rate")
axVdM.grid(True, which="both")
axVdM.set_yscale("log")


plt.savefig("VDM_results_X.png")
plt.show()

fig, (axVdMFit) = plt.subplots(1,1)

axVdMFit.scatter(ScanSteps, xScan[2], s=15., label="VdM Simulation")

scaling = 1 / 0.00633
plotter.plotFitResultsOnAx(axVdMFit, 25, pdfs.oneDimGaussAlt, xScan[4], scaling, label="Single Gauss fit", c="g")

#ax1.title.set_text('X-scan')
axVdMFit.set_xlabel(r"$\Delta$ x [a.u.]")
axVdMFit.set_ylabel(r"Rate")
axVdMFit.grid(True, which="both")
axVdMFit.set_yscale("log")
axVdMFit.legend()

plt.savefig("VDM_results_with_fit_X.png")
plt.show()
