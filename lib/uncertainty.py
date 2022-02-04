import numpy as np
import lib.VDMSim as vdm
import lib.beamPDFs as beamPDFs

from scipy import optimize, stats, integrate


def RunVdmScanSimOnAll(pdf, beamParameters, nSteps=25, peakRate=0.00633):
    """
    Main function to run a lot of beam setups at once
    """

    dx = np.linspace(-(nSteps - 1) / 2., (nSteps - 1) / 2., num=nSteps, endpoint=True)

    beamPositionX = np.zeros((nSteps, 4))
    beamPositionX[:, 0] = dx
    
    beamPositionY = np.zeros((nSteps, 4))

    beamPositionY[:, 1] = beamPositionX[:, 0]
    beamPositionY[:, 0] = np.zeros(nSteps)

    allSGWidths = np.zeros((np.size(beamParameters, 0), 2))
    allDGWidths = np.zeros((np.size(beamParameters, 0), 2))
    trueOverlap = np.zeros(np.size(beamParameters, 0))

    for i, variation in enumerate(beamParameters):
        # TODO: is this variation constant for all variations or not?
        integral, err = integrate.dblquad(pdf, -30., 30., lambda x : -30., lambda x : 30., args=(variation,))
        scaling = integral / peakRate

        xScanResults = vdm.vdmScanSim(pdf, variation, beamPositionX, scaling)
        yScanResults = vdm.vdmScanSim(pdf, variation, beamPositionY, scaling, axis=1)

        allSGWidths[i, 0] = xScanResults[4][1]
        allSGWidths[i, 1] = yScanResults[4][1]

        allDGWidths[i, 0] = xScanResults[0]
        allDGWidths[i, 1] = yScanResults[0]

        trueOverlap[i] = integral


    return (trueOverlap, allSGWidths, allDGWidths)

def calcCorrectionAndUncertainty(trueOverlap, widths):
    """
    NOTE: stddev is calculated in regard to the avg of the correction factors, not the correction factor with nominal beam parameters
    
    """

    vdmArea = np.prod(widths, axis=1) * 2 * np.pi
    trueArea = 1. / trueOverlap

    corrFactors = (vdmArea - trueArea) * trueOverlap

    avgCorr = np.average(corrFactors)
    stdDevCorr = np.std(corrFactors)

    return avgCorr, stdDevCorr



def runUncertaintyTestOverlap(nominalBeams, relativeUncertainty, testSize=100):
    """
    store widths
    calc average and uncertainty
    make sure we can independantly vary parameters and combine result

    for each variation, check correction factor -> average and check result

    """

    variedBeams = np.random.normal(loc=nominalBeams, scale=relativeUncertainty, size = (testSize, 2, 9))

    result = RunVdmScanSimOnAll(beamPDFs.DoubleGaussBeamOverlap, variedBeams)

    avgCorr, stdDevCorr = calcCorrectionAndUncertainty(result[0], result[1])

    # get nominal beam, compare results of corrfactor to other stuff
    



    return