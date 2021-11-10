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