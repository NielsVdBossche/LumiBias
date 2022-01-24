import math
import lib.VDMSim as vdm
from lib.VDMSim_Cleaned import RunVdmScanSim
import lib.beamPDFs as beamPDFs
import lib.pdfs as pdfs
import lib.truePdf as truepdfs
import lib.jsonTools as jsonTools
from scipy import integrate

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


## Tests of stuff that I used, given that this type of Python is long-time-no-see

def distrTestGauss(argsB1, argsB2):
    xSpace = np.linspace(-10., 10., 1000)
    ySpace = np.linspace(-10., 10., 1000)

    gridB1 = np.meshgrid(xSpace, ySpace)
    gridB2 = np.meshgrid(xSpace, ySpace)
    gridB3 = np.meshgrid(xSpace, ySpace)

    #argsB1 = [-2, 0, 4, 2, 0]

    #argsB2 = [2, 0, 4, 2, 0]

    distB1 = pdfs.singleGaussBeam(argsB1, gridB1)
    distB2 = pdfs.singleGaussBeam(argsB2, gridB2)

    fig, (beamOne, beamTwo, BeamMix) = plt.subplots(1, 3)

    beamOne.imshow(distB1, interpolation='bilinear')
    beamTwo.imshow(distB2, interpolation='bilinear')

    distCross = truepdfs.singleGaussBeamsCross(argsB1, argsB2, gridB3)

    BeamMix.imshow(distCross, interpolation='bilinear')
    plt.show()

def distrTestDoubleGauss(argsB1, argsB2):
    xSpace = np.linspace(-10., 10., 1000)
    ySpace = np.linspace(-10., 10., 1000)

    gridB1 = np.meshgrid(xSpace, ySpace)
    gridB1M = np.meshgrid(xSpace, ySpace)

    gridB2 = np.meshgrid(xSpace, ySpace)
    gridB2M = np.meshgrid(xSpace, ySpace)

    gridB3 = np.meshgrid(xSpace, ySpace)

    #argsB1 = [-2, 0, 4, 2, 0]

    #argsB2 = [2, 0, 4, 2, 0]

    weight1 = argsB1[-1]
    weight2 = argsB2[-1]
#
    distB1 = weight1 * pdfs.singleGaussBeam(argsB1[:5], gridB1) + (1-weight1) * pdfs.singleGaussBeam(argsB1[:2] + argsB1[5:-1], gridB1M)
    distB2 = weight2 * pdfs.singleGaussBeam(argsB2[:5], gridB2) + (1-weight2) * pdfs.singleGaussBeam(argsB2[:2] + argsB2[5:-1], gridB2M)

    #distB1 = truepdfs.doubleGaussBeamCross()
    #distB2 = truepdfs.doubleGaussBeamCross()

    fig, (beamOne, beamTwo, BeamMix) = plt.subplots(1, 3)

    beamOne.imshow(distB1, interpolation='bilinear')
    beamTwo.imshow(distB2, interpolation='bilinear')

    beamOne.title.set_text("Beam 1")
    beamTwo.title.set_text("Beam 2")


    distCross = truepdfs.singleGaussBeamsCross(argsB1, argsB2, gridB3)

    BeamMix.imshow(distCross, interpolation='bilinear')

    BeamMix.title.set_text("Overlap")

    plt.savefig("testBeamVis.png")

    plt.show()

def gaussFuncTest():
    meanOne = 0
    stdDevOne = 1
    meanTwo = 3
    stdDevTwo = 2
    x = np.linspace(-10, 10, 1000)

    gaussOne = stats.norm.pdf(x, loc=meanOne, scale=stdDevOne)
    gaussTwo = stats.norm.pdf(x, loc=meanTwo, scale=stdDevTwo)

    plt.plot(x, gaussOne)
    plt.plot(x, gaussTwo)
    plt.show()

def vdmTest():

    argsB1 = [0, 0, 1.978, 1.716, -0.073]
    argsB2 = [0, 0, 1.802, 1.644, -0.058]

    distrTestGauss(argsB1, argsB2)

    dxOne = np.linspace(-20., 20., num=50, endpoint=True)
    dyOne = np.zeros(50)
    dx = np.array([dxOne, dyOne])
    dy = np.array([dyOne, dyOne])

    #print(dx)
    #print(dy)

    xEv, xChiSq, xWidth = vdm.vdmScanSim(truepdfs.singleGaussBeamCrossIntegratable, argsB1, argsB2, dx, dy, 50, True)
    yEv, yChiSq, yWidth = vdm.vdmScanSim(truepdfs.singleGaussBeamCrossIntegratable, argsB1, argsB2, dy, dx, 50, False)

    area_VdM = 2 * np.pi * xWidth * yWidth

    area_True, err = integrate.dblquad(truepdfs.singleGaussBeamCrossIntegratable, -30., 30., lambda x : -30., lambda x : 30., args=(argsB1, argsB2))

    print(area_VdM)
    print(1/area_True)


def vdmTestDG():

    argsB1 = [0, 0, 1.978, 1.716, -0.073, 2.141, 2.13, -0.676, 0.940]
    argsB2 = [0, 0, 1.782, 1.641, -0.058, 1.834, 1.65, -0.057, 0.968]

    nSteps = 25

    #distrTestDoubleGauss(argsB1, argsB2)

    dxOne = np.linspace(-12., 12., num=nSteps, endpoint=True)
    dyOne = np.zeros(nSteps)
    dx = np.array([dxOne, dyOne])
    dy = np.array([dyOne, dyOne])

    #print(dx)
    #print(dy)

    xYields, xEv, xChiSq, xWidth = vdm.vdmScanSim(truepdfs.doubleGaussBeamCross, argsB1, argsB2, dx, dy, nSteps, True)

    file = jsonTools.openFile("Rates_HFOC_6016.json")
    hfocData = jsonTools.getData(file)

    plt.scatter(dx[0] - dx[1], xYields, label="VdM sim", s=10.)
    plt.scatter(dx[0] - dx[1], hfocData, label="VdM data", s=10.)

    plt.legend()

    plt.xlabel(r"$\Delta$x [a.u.]")
    plt.ylabel(r"Rate")
    plt.yscale("log")
    plt.grid(True, which="both")
    plt.savefig("SimVData.png")
    plt.show()

    dyOne = np.linspace(-12., 12., num=nSteps, endpoint=True)
    dxOne = np.zeros(nSteps)
    dy = np.array([dyOne, dxOne])
    dx = np.array([dxOne, dxOne])

    yYields, yEv, yChiSq, yWidth = vdm.vdmScanSim(truepdfs.doubleGaussBeamCross, argsB1, argsB2, dx, dy, nSteps, False)

    # same for dy now

    area_VdM = 2 * np.pi * xWidth * yWidth

    area_True, err = integrate.dblquad(truepdfs.doubleGaussBeamCross, -30., 30., lambda x : -30., lambda x : 30., args=(argsB1, argsB2))

    print("VDM obtained area: {}".format(area_VdM))
    print("True area: {}".format(1/area_True))

    print ((area_VdM - 1/area_True) * area_True)

    
    # from fit results, get a total sigma x, sigma y for each distr and use these to get a futted xy area

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