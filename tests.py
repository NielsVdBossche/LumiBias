import math
from lib.VDMSim import RunVdmScanSim
import lib.beamPDFs as beamPDFs
import lib.pdfs as pdfs
import lib.truePdf as truepdfs
import lib.jsonTools as jsonTools
from scipy import integrate

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


## Tests of stuff that I used, given that this type of Python is long-time-no-see
def newVdmTest():
    argsB1 = [0, 0, 1.978, 1.716, -0.073, 2.141, 2.13, -0.676, 0.940]
    argsB2 = [0, 0, 1.782, 1.641, -0.058, 1.834, 1.65, -0.057, 0.968]

    argsB1 = np.array(argsB1)
    argsB2 = np.array(argsB2)

    beamParams = np.array((argsB1, argsB2))

    #beamPDFs.DoubleGaussBeamOverlap(0., 0., beamParams)
    
    area_True, err = integrate.dblquad(beamPDFs.DoubleGaussBeamOverlap, -30., 30., lambda x : -30., lambda x : 30., args=(beamParams,))

    vdmResults = RunVdmScanSim(beamPDFs.DoubleGaussBeamOverlap, beamParams)

    area_VdM = 2 * np.pi * vdmResults[1][0][0] * vdmResults[1][1][0]


    print("VDM obtained area: {}".format(area_VdM))
    print("True area: {}".format(1/area_True))

    print ((area_VdM - 1/area_True) * area_True)

    fig, (ax1, ax2) = plt.subplots(1,2)

    ax1.scatter(np.linspace(-12., 12., num=25, endpoint=True), vdmResults[1][0][2])
    ax2.scatter(np.linspace(-12., 12., num=25, endpoint=True), vdmResults[1][1][2])
    ax1.set_title("X-scan")

    ax1.set_yscale("log")
    ax2.set_yscale("log")

    plt.show()

def newBeamImageTest():
    argsB1 = [0, 0, 1.978, 1.716, -0.073, 2.141, 2.13, -0.676, 0.940]
    argsB2 = [0, 0, 1.782, 1.641, -0.058, 1.834, 1.65, -0.057, 0.968]

    argsB1 = np.array(argsB1, dtype=np.float64)
    argsB2 = np.array(argsB2, dtype=np.float64)

    beamParams = np.array((argsB1, argsB2), dtype=np.float64)

    xSpace = np.linspace(-10., 10., 1000, dtype=np.float64)
    ySpace = np.linspace(-10., 10., 1000, dtype=np.float64)

    gridB1 = np.meshgrid(xSpace, ySpace)

    distB1 = beamPDFs.DoubleGaussBeam(gridB1[1], gridB1[0], beamParams[0])
    distB2 = beamPDFs.DoubleGaussBeam(gridB1[1], gridB1[0], beamParams[1])

    fig, (beamOne, beamTwo, BeamMix) = plt.subplots(1, 3)

    beamOne.imshow(distB1, interpolation='bilinear')
    beamTwo.imshow(distB2, interpolation='bilinear')

    distCross = beamPDFs.DoubleGaussBeamOverlap(gridB1[1], gridB1[0], beamParams)

    BeamMix.imshow(distCross, interpolation='bilinear')
    #plt.show()

    newFig, newAx = plt.subplots()
    newAx.plot(distB1[:,500])
    plt.show()


if (__name__ == "__main__"):
    #distrTestGauss()

    #gaussFuncTest()
    #vdmTest()
    #vdmTestDG()
    #newBeamImageTest()
    newVdmTest()