import lib.VDMSim as vdm
import lib.pdfs as pdfs
import lib.truePdf as truepdfs

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


## Tests of stuff that I used, given that this type of Python is long-time-no-see

def distrTestGauss():
    xSpace = np.linspace(-10., 10., 1000)
    ySpace = np.linspace(-10., 10., 1000)

    gridB1 = np.meshgrid(xSpace, ySpace)
    gridB2 = np.meshgrid(xSpace, ySpace)
    gridB3 = np.meshgrid(xSpace, ySpace)

    argsB1 = [-2, 0, 4, 2, 0]

    argsB2 = [2, 0, 4, 2, 0]

    distB1 = pdfs.singleGaussBeam(argsB1, gridB1)
    distB2 = pdfs.singleGaussBeam(argsB2, gridB2)

    fig, (beamOne, beamTwo, BeamMix) = plt.subplots(1, 3)

    beamOne.imshow(distB1, interpolation='bilinear')
    beamTwo.imshow(distB2, interpolation='bilinear')

    distCross = truepdfs.singleGaussBeamsCross(argsB1, argsB2, gridB3)

    BeamMix.imshow(distCross, interpolation='bilinear')
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

    argsB1 = [-2, 0, 1, 2, 0]
    argsB2 = [2, 0, 1, 2, 0]

    dxOne = np.linspace(-6., 6., num=25, endpoint=True)
    dx = np.array([dxOne, dxOne[::-1]])
    dyOne = np.zeros(25)
    dy = np.array([dyOne, dyOne])

    print(dx)
    print(dy)

    vdm.vdmScanSim(truepdfs.singleGaussBeamCrossIntegratable, argsB1, argsB2, dx, dy, 25, True)

if (__name__ == "__main__"):
    #distrTestGauss()

    #gaussFuncTest()

    vdmTest()