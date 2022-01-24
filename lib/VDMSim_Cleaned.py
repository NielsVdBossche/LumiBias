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

        integral, err = integrate.dblquad(pdf, -30., 30., lambda x : -30., lambda x : 30., args=(beamParameters,))
        eventYields[i] = np.random.normal(integral / scaling, scale = 0.005 * integral / scaling) if randomMode >= 1 else integral / scaling
    

    return eventYields

def vdmScanSim(pdf, beamParameters, beamPos, scaling, axis=0):
    """
    Axis: 0 for x, 1 for y if beam 1 moves, otherwise +2
    """
    eventYield = vdmLoop(pdf, beamParameters, beamPos, scaling, randomMode=1)

    totalEventYield = np.sum(eventYield)

    paramOpt, cov = optimize.curve_fit(pdfs.oneDimDoubleGauss, beamPos[:, axis], eventYield / totalEventYield, bounds=((-np.inf, -np.inf, -np.inf, -np.inf, 0.), (np.inf, np.inf, np.inf, np.inf, 1.)))
    vdmPredicted = pdfs.oneDimDoubleGauss(beamPos[:, axis], paramOpt[0], paramOpt[1], paramOpt[2], paramOpt[3], paramOpt[4])
    width = 1 / (( (paramOpt[4] / paramOpt[1]) + ((1-paramOpt[4]) / paramOpt[3]) ))
    
    chiSq = stats.chisquare(eventYield / totalEventYield, f_exp=vdmPredicted / np.sum(vdmPredicted))

    return (width, chiSq, eventYield, paramOpt)
   
def RunVdmScanSim(pdf, beamParameters, peakRate=0.00633):
    """
    Main function to use vdm sim
    """

    dx = np.linspace(-12., 12., num=25, endpoint=True)

    beamPosition = np.zeros((25, 4))

    for i in range(25):
        beamPosition[i, 0] = dx[i]
        beamPosition[i, 1] = 0
        beamPosition[i, 2] = 0
        beamPosition[i, 3] = 0

    integral, err = integrate.dblquad(pdf, -30., 30., lambda x : -30., lambda x : 30., args=(beamParameters,))
    scaling = integral / peakRate

    xScanResults = vdmScanSim(pdf, beamParameters, beamPosition, scaling)

    beamPosition[:, 1] = beamPosition[:, 0]
    beamPosition[:, 0] = np.zeros(25)

    yScanResults = vdmScanSim(pdf, beamParameters, beamPosition, scaling, axis=1)

    return (dx, (xScanResults, yScanResults))
