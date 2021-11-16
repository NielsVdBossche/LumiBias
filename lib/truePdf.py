import lib.pdfs as pdfs

import numpy as np

# Contains all machinery to set up true pdfs
'''
def singleGaussBeams(arguments1, arguments2):
    distB1 = pdfs.singleGauss(arguments1)
    distB2 = pdfs.singleGauss(arguments2)

    xSpace = np.linspace(-30., 30., 500)
    ySpace = np.linspace(-30., 30., 500)

    xGrid, yGrid = np.meshgrid(xSpace, ySpace)

    ## match pdf to grid
    z = xGrid

    zGrid = np.reshape(xGrid.shape())
'''

def singleGaussBeamsCross(argB1, argB2, grid):
    gridB1 = np.copy(grid)
    gridB2 = np.copy(grid)
    beam1 = pdfs.singleGaussBeam(argB1, gridB1)
    beam2 = pdfs.singleGaussBeam(argB2, gridB2)

    beamCross = np.multiply(beam1, beam2)

    return beamCross

def singleGaussBeamCrossIntegratable(y, x, argB1, argB2):
    valOne = pdfs.singleGaussBeamNew(x, y, argB1)
    valTwo = pdfs.singleGaussBeamNew(x, y, argB2)

    return valOne * valTwo

def doubleGaussBeamCross(y, x, argB1, argB2):
    '''
    argB1: [offset X, offset Y, sigmaX N, sigmaY N, corN, sigmaX M, sigmaY M, corrM, wN]
    idem for argB2
    '''
    wNB1 = argB1[-1]
    wNB2 = argB2[-1]

    valNB1 = pdfs.singleGaussBeamNew(x, y, argB1[:5])
    valMB1 = pdfs.singleGaussBeamNew(x, y, argB1[:2] + argB1[5:-1])

    valNB2 = pdfs.singleGaussBeamNew(x, y, argB2[:5])
    valMB2 = pdfs.singleGaussBeamNew(x, y, argB2[:2] + argB2[5:-1])

    return (wNB1 * valNB1 + (1-wNB1) * valMB1) * (wNB2 * valNB2 + (1-wNB2)* valMB2)