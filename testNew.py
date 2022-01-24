import lib.beamPDFs as beamPDFs
import lib.plotCode as plotCode
from lib.VDMSim import RunVdmScanSim
from scipy import integrate
import matplotlib.pyplot as plt

import numpy as np

def DGParameters():
    argsB1 = [0, 0, 1.978, 1.716, -0.073, 2.141, 2.13, -0.676, 0.940]
    argsB2 = [0, 0, 1.782, 1.641, -0.058, 1.834, 1.65, -0.057, 0.968]

    argsB1 = np.array(argsB1)
    argsB2 = np.array(argsB2)

    beamParams = np.array((argsB1, argsB2))

    return beamParams

def runVDMSimTest():
    beamParams = DGParameters()

    area_True, err = integrate.dblquad(beamPDFs.DoubleGaussBeamOverlap, -30., 30., lambda x : -30., lambda x : 30., args=(beamParams,))

    vdmResults = RunVdmScanSim(beamPDFs.DoubleGaussBeamOverlap, beamParams)

    area_VdM = 2 * np.pi * vdmResults[1][0][0] * vdmResults[1][1][0]

    print("VDM obtained area: {}".format(area_VdM))
    print("True area: {}".format(1/area_True))

    print ((area_VdM - 1/area_True) * area_True)

    fig = plotCode.plotVDMResultsAndData(vdmResults[0], vdmResults[1])
    #plotCode.plotFitResults(vdmResults[1], fig)
    _, (ax1, ax2) = fig
    ax1.legend()
    ax2.legend()


    plt.show()


if (__name__ == "__main__"):
    runVDMSimTest()