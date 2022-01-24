import numpy as np

def SingleGaussBeam(y, x, beam):
    """
    beam: contains all parameters required to generate a single gaussian beam: 
            (x-mean, y-mean, x-width, y-width, correlation)
    """
    xDiff = x - beam[0]
    xDiff /= beam[2]

    yDiff = y - beam[1]
    yDiff /= beam[3]

    corrTerm = 2. * beam[4] * xDiff * yDiff

    exponent = corrTerm - np.multiply(xDiff, xDiff) - np.multiply(yDiff, yDiff)
    preFactor = 0.5 / (1 - (beam[4] * beam[4]))

    exponent *= preFactor

    normFactor = 2 * np.pi * beam[2] * beam[3] * np.sqrt(1 - (beam[4] * beam[4]))

    result = (1 / normFactor) * np.exp(exponent)

    return result

def DoubleGaussBeam(y, x, beam):
    """
    beam: array of all information for a double gaussian beam:
            (x-mean, y-mean, x-width1, y-width1, correlation1, x-width2, y-width2, correlation2, coefficient)
    """

    partOne = SingleGaussBeam(y, x, beam[:5])
    partTwo = SingleGaussBeam(y, x, np.concatenate((beam[:2], beam[5:8])))

    return beam[-1] * partOne + (1-beam[-1]) * partTwo

def tripleGaussBeam(y, x, beam):
    """
    Beam: (x-mean, y-mean, x-width1, y-width1, correlation1, x-width2, y-width2, correlation2, x-width3, y-width3, correlation3, coeff1, coeff2)
    """
    partOne = SingleGaussBeam(y, x, beam[:5])
    partTwo = SingleGaussBeam(y, x, np.concatenate((beam[:2], beam[5:8])))
    partThree = SingleGaussBeam(y, x, np.concatenate((beam[:2], beam[8:11])))


    return beam[-2] * partOne + beam[-1] * partTwo + (1 - beam[-2] - beam[-1]) * partThree


def SingleGaussBeamOverlap(y, x, beams):
    """
    Beams: array containing 2 arrays, each providing the parameters for a single gaussian beam 
            in the same order as singleGaussBeam
    """

    beamOne = SingleGaussBeam(y, x, beams[0])
    beamTwo = SingleGaussBeam(y, x, beams[1])

    return beamOne * beamTwo

def DoubleGaussBeamOverlap(y, x, beams):
    """
    beams: array containing 2 arrays, each for one double gauss beam
    """

    beamOne = DoubleGaussBeam(y, x, beams[0])
    beamTwo = DoubleGaussBeam(y, x, beams[1])

    return beamOne * beamTwo


def beamOverlap(y, x, beamFunc, beamParams):
    """
    Generalization of single/double gauss beam overlap
    """
    beamOne = beamFunc(y, x, beamParams[0])
    beamTwo = beamFunc(y, x, beamParams[1])

    return beamOne * beamTwo


    