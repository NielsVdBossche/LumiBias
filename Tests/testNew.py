import lib.beamPDFs as beamPDFs
import lib.plotCode as plotCode
from lib.VDMSim import RunVdmScanSim
from scipy import integrate
import matplotlib.pyplot as plt

import numpy as np

def DGParameters():
    argsB1 = [0, 0, 1.978, 1.716, -0.073, 2.141, 2.13, -0.676, 1.]
    argsB2 = [0, 0, 1.782, 1.641, -0.058, 1.834, 1.65, -0.057, 0.626]

    argsB1 = np.array(argsB1)
    argsB2 = np.array(argsB2)

    beamParams = np.array((argsB1, argsB2))

    return beamParams

def TGParameters():
    argsB1 = [0, 0, 1.874, 1.690, -0.074, 2.752, 1.691, -0.100, 2.753, 3.037, -0.020, 0.335, 0.412]
    argsB2 = [0, 0, 1.795, 1.635, -0.059, 3.290, 3.003, -0.856, 3.338, 3.028, -0.092, 0.089, 1.564]

    argsB1 = np.array(argsB1)
    argsB2 = np.array(argsB2)

    beamParams = np.array((argsB1, argsB2))

    return beamParams

def runVDMSimTest():
    beamParams = DGParameters()

    area_True, err = integrate.dblquad(beamPDFs.DoubleGaussBeamOverlap, -30., 30., lambda x : -30., lambda x : 30., args=(beamParams,))

    nrOfSteps = int(input("Number of steps: "))
    dx, (xScan, yScan) = RunVdmScanSim(beamPDFs.DoubleGaussBeamOverlap, beamParams, nSteps=nrOfSteps)

    area_VdM_DG = 2 * np.pi * xScan[0] * yScan[0]
    area_VdM_SG = 2 * np.pi * xScan[4][1] * yScan[4][1]

    print("VDM (DG) obtained area: {}".format(area_VdM_DG))
    print("VDM (SG) obtained area: {}".format(area_VdM_SG))

    print("True area: {}".format(1/area_True))

    print ((area_VdM_DG - 1/area_True) * area_True)

    fig = plotCode.plotVDMResults(dx, (xScan, yScan))
    #plotCode.plotFitResults(vdmResults[1], fig)
    _, (ax1, ax2) = fig
    ax1.legend()
    ax2.legend()

    plt.savefig("VDM_results_bothAxis.png")
    plt.show()


if (__name__ == "__main__"):
    runVDMSimTest()