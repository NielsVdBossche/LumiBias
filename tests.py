import lib.VDMSim as vdm
import lib.pdfs as pdfs
import lib.truePdf as truepdfs

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

    distB1 = weight1 * pdfs.singleGaussBeam(argsB1[:5], gridB1) + (1-weight1) * pdfs.singleGaussBeam(argsB1[:2] + argsB1[5:-1], gridB1M)
    distB2 = weight2 * pdfs.singleGaussBeam(argsB2[:5], gridB2) + (1-weight2) * pdfs.singleGaussBeam(argsB2[:2] + argsB2[5:-1], gridB2M)

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

    argsB1 = [0, 0, 3, 1, 0.9]
    argsB2 = [0, 0, 1, 2, 0]

    distrTestGauss(argsB1, argsB2)

    dxOne = np.linspace(-10., 10., num=25, endpoint=True)
    dyOne = np.zeros(25)
    dx = np.array([dxOne, dyOne])
    dy = np.array([dyOne, dyOne])

    print(dx)
    print(dy)

    vdm.vdmScanSim(truepdfs.singleGaussBeamCrossIntegratable, argsB1, argsB2, dx, dy, 25, True)


def vdmTestDG():

    argsB1 = [0, 0, 1.978, 1.716, -0.073, 2.141, 2.13, -0.676, 0.940]
    argsB2 = [0, 0, 1.782, 1.641, -0.058, 1.834, 1.65, -0.057, 0.968]


    distrTestDoubleGauss(argsB1, argsB2)

    dxOne = np.linspace(-10., 10., num=25, endpoint=True)
    dyOne = np.zeros(25)
    dx = np.array([dxOne, dyOne])
    dy = np.array([dyOne, dyOne])

    print(dx)
    print(dy)

    vdm.vdmScanSim(truepdfs.singleGaussBeamCrossIntegratable, argsB1, argsB2, dx, dy, 25, True)

    dyOne = np.linspace(-10., 10., num=25, endpoint=True)
    dxOne = np.zeros(25)
    dy = np.array([dyOne, dxOne])
    dx = np.array([dxOne, dxOne])

    vdm.vdmScanSim(truepdfs.singleGaussBeamCrossIntegratable, argsB1, argsB2, dx, dy, 25, False)

    # same for dy now

    
    # from fit results, get a total sigma x, sigma y for each distr and use these to get a futted xy area

if (__name__ == "__main__"):
    #distrTestGauss()

    #gaussFuncTest()

    vdmTestDG()