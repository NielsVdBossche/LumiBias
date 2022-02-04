import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

from testNew import DGParameters
import lib.VDMSim as vdm
import lib.beamPDFs as beamPDFs
import lib.plotCode as plotter
import lib.pdfs as pdfs

"""
Script to run a VDM and BI scan and compare results
"""

beamParameters = DGParameters()

true_inv_area, _ = integrate.dblquad(beamPDFs.DoubleGaussBeamOverlap, -30., 30., lambda x : -30., lambda x : 30., args=(beamParameters,))
scaling = 1 / 0.00633

area_true = 1. / true_inv_area

# vdm scan
dx_vdm, (vdmX, vdmY) = vdm.RunVdmScanSim(beamPDFs.DoubleGaussBeamOverlap, beamParameters, nSteps=25)

area_VdM_DG = 2 * np.pi * vdmX[0] * vdmY[0]
area_VdM_SG = 2 * np.pi * vdmX[4][1] * vdmY[4][1]

# BI scan
dx_BI, (biX, biY) = vdm.RunVdmScanSim(beamPDFs.DoubleGaussBeamOverlap, beamParameters, nSteps=19)

area_BI_DG = 2 * np.pi * biX[0] * biY[0]
area_BI_SG = 2 * np.pi * biX[4][1] * biY[4][1]

## output management
# not really interested in points, so only plot vdm points now and we plot the fit over this
fig, (ax1, ax2) = plotter.plotVDMResults(dx_vdm, (vdmX, vdmY), label="Scan results", log=True)

#ax1.scatter(dx_BI, biX[2], s=15., label="BI Scan")
#ax2.scatter(dx_BI, biY[2], s=15., label="BI Scan")
plotter.plotFitResultsOnAx(ax1, 19, pdfs.oneDimDoubleGaussAlt, biX[3], scaling, label="BI fit", c="r")
plotter.plotFitResultsOnAx(ax2, 19, pdfs.oneDimDoubleGaussAlt, biY[3], scaling, label="BI fit", c="r")

plotter.plotFitResultsOnAx(ax1, 25, pdfs.oneDimDoubleGaussAlt, vdmX[3], scaling, label="VdM fit", c="g")
plotter.plotFitResultsOnAx(ax2, 25, pdfs.oneDimDoubleGaussAlt, vdmY[3], scaling, label="VdM fit", c="g")

ax1.legend()
ax2.legend()


print("Correction factor from DG: ")
print("\t VdM: {}".format((area_VdM_DG - area_true) / area_true))
print("\t BI: {}".format((area_BI_DG - area_true) / area_true))

plt.savefig("VDMvsBI_Scan_DG.png")
plt.show()

fig, (ax1, ax2) = plotter.plotVDMResults(dx_vdm, (vdmX, vdmY), label="Scan results", log=True)

plotter.plotFitResultsOnAx(ax1, 19, pdfs.oneDimGaussAlt, biX[4], scaling, label="BI fit", c="r")
plotter.plotFitResultsOnAx(ax2, 19, pdfs.oneDimGaussAlt, biY[4], scaling, label="BI fit", c="r")

plotter.plotFitResultsOnAx(ax1, 25, pdfs.oneDimGaussAlt, vdmX[4], scaling, label="VdM fit", c="g")
plotter.plotFitResultsOnAx(ax2, 25, pdfs.oneDimGaussAlt, vdmY[4], scaling, label="VdM fit", c="g")

ax1.legend()
ax2.legend()

print("Correction factor from SG: ")
print("\t VdM: {}".format((area_VdM_SG - area_true) / area_true))
print("\t BI: {}".format((area_BI_SG - area_true) / area_true))

plt.savefig("VDMvsBI_Scan_SG.png")
plt.show()