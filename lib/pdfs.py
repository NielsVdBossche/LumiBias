import numpy as np
from scipy import stats

'''
generates all pdfs desired as the initial distribution
'''
# functions should be considered from a min till a max range
# give grid of points? Per point we consider the integral again? Idk
# function should be normalized to 1 tho, shouldnt it? Producet should be! overlap of functions is product

def singleGaussBeam(args, grid):
    offsetX = args[0]
    sigmaX = args[2]

    offsetY = args[1]
    sigmaY = args[3]

    corr = args[4]

    xGrid, yGrid = grid

    xGrid -= offsetX
    xGrid /= sigmaX

    yGrid -= offsetY
    yGrid /= sigmaY

    corrTerm = 2 * corr * xGrid * yGrid

    exponent = corrTerm - np.multiply(xGrid, xGrid) - np.multiply(yGrid, yGrid)
    preFactor = 1 * 0.5 / (1 - (corr * corr))

    exponent *= preFactor

    normFactor = 2 * np.pi * sigmaX * sigmaY * np.sqrt(1 - (corr * corr))

    result = (1/normFactor) * np.exp(exponent)

    return result

def singleGaussBeamNew(x, y, args):
    offsetX = args[0]
    sigmaX = args[2]

    offsetY = args[1]
    sigmaY = args[3]

    corr = args[4]

    newX = x - offsetX
    newX /= sigmaX

    newY = y - offsetY
    newY /= sigmaY

    corrTerm = 2 * corr * newX * newY

    exponent = corrTerm - np.multiply(newX, newX) - np.multiply(newY, newY)
    preFactor = 0.5 / (1 - (corr * corr))

    exponent *= preFactor

    normFactor = 2 * np.pi * sigmaX * sigmaY * np.sqrt(1 - (corr * corr))

    result = (1 / normFactor) * np.exp(exponent)

    return result

def oneDimDoubleGauss(x, meanOne, stdDevOne, meanTwo, stdDevTwo, coeff):
    #meanOne = args[0]
    #stdDevOne = args[1]
    #meanTwo = args[2]
    #stdDevTwo = args[3]
    #coeff = args[4]

    gaussOne = stats.norm.pdf(x, loc=meanOne, scale=stdDevOne)
    gaussTwo = stats.norm.pdf(x, loc=meanTwo, scale=stdDevTwo)

    return coeff * gaussOne + (1. - coeff) * gaussTwo

def oneDimGauss(x, meanOne, stdDevOne):
    gaussOne = stats.norm.pdf(x, loc=meanOne, scale=stdDevOne)
    return gaussOne


def oneDimDoubleGaussAlt(x, parameters):
    gaussOne = stats.norm.pdf(x, loc=parameters[0], scale=parameters[1])
    gaussTwo = stats.norm.pdf(x, loc=parameters[2], scale=parameters[3])

    return parameters[4] * gaussOne + (1. - parameters[4]) * gaussTwo

def oneDimGaussAlt(x, parameters):
    gaussOne = stats.norm.pdf(x, loc=parameters[0], scale=parameters[1])
    return gaussOne
