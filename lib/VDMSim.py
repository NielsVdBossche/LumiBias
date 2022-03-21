import numpy as np

from scipy import optimize, stats, integrate
import lib.pdfs as pdfs


def vdmLoop(pdf, beamParameters, beamPos, scaling, randomMode=1):
    """
    VDM scan simulation.
    pdf should be a function that accepts 'beamParameters' as an argument.
    nSteps: the number of steps you run the simulation over.
    beamPos: the distance between the beams at every step, of the form [[offsets at pos 1], [offsets at pos 2], ...]
    Axis: the axis along which you perform the scan
    RandomMode: [0, 1, 2]. 0 for nonRandom mode, 1 for random mode, 2 for testing mode (no randomization and extra figures)
    """
    eventYields = np.zeros(len(beamPos[:,0]))

    #beamOne, beamTwo = beamParameters

    for i, offsets in enumerate(beamPos):
        # Change beam parameters
        beamParameters[0, 0] = offsets[0]
        beamParameters[0, 1] = offsets[1]

        beamParameters[1, 0] = offsets[2]
        beamParameters[1, 1] = offsets[3]

        integral, err = integrate.dblquad(pdf, -35., 35., lambda x : -35., lambda x : 35., args=(beamParameters,))
        eventYields[i] = np.random.normal(integral / scaling, scale = 0.005 * integral / scaling) if randomMode >= 1 else integral / scaling
    

    return eventYields

def vdmScanSim(pdf, beamParameters, beamPos, scaling, axis=0):
    """
    Axis: 0 for x, 1 for y if beam 1 moves, otherwise +2
    """
    eventYield = vdmLoop(pdf, beamParameters, beamPos, scaling, randomMode=0)

    totalEventYield = np.sum(eventYield)
    # single gauss als first guess + force fit to be at 0 centered
    DGParam, cov = optimize.curve_fit(pdfs.oneDimDoubleGauss, beamPos[:, axis], eventYield / totalEventYield, bounds=((-0.00001, 1.5, -0.00001, 1.5, 0.), (0.00001, 30., 0.00001, 30., 1.)))
    vdmPredicted = pdfs.oneDimDoubleGauss(beamPos[:, axis], DGParam[0], DGParam[1], DGParam[2], DGParam[3], DGParam[4])
    width = 1 / (( (DGParam[4] / DGParam[1]) + ((1-DGParam[4]) / DGParam[3]) ))

    SGParam, cov = optimize.curve_fit(pdfs.oneDimGauss, beamPos[:, axis], eventYield / totalEventYield, bounds=((-0.001, 1.5), (0.001, 30.)))
    
    chiSq = stats.chisquare(eventYield / totalEventYield, f_exp=vdmPredicted / np.sum(vdmPredicted))

    return (width, chiSq, eventYield, DGParam, SGParam)
   
def RunVdmScanSim(pdf, beamParameters, nSteps=25, peakRate=0.00633):
    """
    Main function to use vdm sim
    """

    dx = np.linspace(-(nSteps - 1) / 2., (nSteps - 1) / 2., num=nSteps, endpoint=True)

    beamPosition = np.zeros((nSteps, 4))

    beamPosition[:, 0] = dx

    beamParameters[:, 0:2] = 0

    integral, err = integrate.dblquad(pdf, -30., 30., lambda x : -30., lambda x : 30., args=(beamParameters,))
    scaling = integral / peakRate

    xScanResults = vdmScanSim(pdf, beamParameters, beamPosition, scaling)

    beamPosition[:, 1] = beamPosition[:, 0]
    beamPosition[:, 0] = np.zeros(nSteps)

    yScanResults = vdmScanSim(pdf, beamParameters, beamPosition, scaling, axis=1)
    
    beamParameters[:, 0:2] = 0


    return (dx, (xScanResults, yScanResults))
