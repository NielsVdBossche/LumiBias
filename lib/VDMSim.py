import numpy as np
from scipy import optimize, stats, integrate
from scipy.stats.stats import chisquare

import lib.pdfs as pdfs
import lib.truePdf as truePDFs

import matplotlib.pyplot as plt

# import a random number generator
## Functions to generate the MC simulation of a given curve

## and classes

###### Pseudocode
'''
Get true PDF, stepsize for x and y separation between beams <- generate these somewhere

Start with X separation, use VDM setup of separation, do the same for y afterwards


For each sep in separation;
    Get integral of true PDF at this sep and multiply with normalization factor
    Simulate as a poisson distributed variable, this is the number of events for this separation
    Save this value in a sep vs dN/dt figure HIST

Set to nominal separation

Fit 2 Gaussians to VDM scan result
'''

# do stuff
def vdmScanSim(pdf, paramB1, paramB2, dx, dy, nSteps, isX):
    '''
    Base function for simulating a vdm scan

    pdf: a pdf function for the beamoverlap
    paramB1: parameters for the first beam with the required length for pdf. [0] must be the x-offset, [1] the y-offset
    paramB2: parameters for the second beam with the required length for pdf. [0] must be the x-offset, [1] the y-offset
    dx, dy: np array withthe steps for x and y-offsets, with the first element being for B1, second for B2
    nSteps: number of steps we take
    '''

    # grid for beams could run from -30 to +30 but with varying precision, providing a very fine grid in the center and the max range over which the beam center + 1 (or 2) stddev shift
    # check this? I guess if we do this it becomes difficult to process the movement in the way i wrote in the for loop...
    
    vdmEventYields = np.zeros(nSteps)

    #xSpace = np.linspace(-10., 10., 1000)
    #ySpace = np.linspace(-10., 10., 1000)
#
    #grid = np.meshgrid(xSpace, ySpace)


    if isX:
        xAxisYields = dx[0] - dx[1]
        # we require an x-axis for fitting, this is given by the variable over which we step. In this case, a single variable is considered, might need to be reconsidered
    else:
        xAxisYields = dy[0] - dy[1]


    for i in range(nSteps):
        paramB1[0] = dx[0, i]
        paramB1[1] = dy[0, i]

        paramB2[0] = dx[1, i]
        paramB2[1] = dy[1, i]
        
        
        # change pdf to work with new parameters
        ########
        # Generally you expect a change in x to just move the gaussian, right? This means we could avoid recalculating the individual beams by just shifting these and using a limited part of the grids for our integral? 

        # anyway, integrate
        integral, err = integrate.dblquad(pdf, -30., 30., lambda x : -30., lambda x : 30., args=(paramB1, paramB2))
        #print(integral)
        #eventRate = np.random.poisson(800 * integral)
        eventRate = np.random.normal(integral, scale = 2e-5)
        vdmEventYields[i] = eventRate
    
    # change pdf to nominal
    paramB1[0] = 0
    paramB1[1] = 0

    paramB2[0] = 0
    paramB2[1] = 0
    totalEvents = np.sum(vdmEventYields)
    #print(vdmEventYields / totalEvents)
    plt.scatter(xAxisYields, vdmEventYields, label="VdM sim", s=10.)

    # fit two gauss to vdmEventYields
    # minimize diff betw gauss and vdmEventYields by changing parameters
    # this yields a result

    # fit sum of 2 gaussians to it
    paramOpt, cov = optimize.curve_fit(pdfs.oneDimDoubleGauss, xAxisYields, vdmEventYields / totalEvents, bounds=((-np.inf, -np.inf, -np.inf, -np.inf, 0.), (np.inf, np.inf, np.inf, np.inf, 1.)))
    vdmPredicted = pdfs.oneDimDoubleGauss(xAxisYields, paramOpt[0], paramOpt[1], paramOpt[2], paramOpt[3], paramOpt[4])

    width = min(paramOpt[1],paramOpt[3])
    #print (paramOpt[1])
    #print (paramOpt[3])
#
    #print(paramOpt[4] ** 2 * paramOpt[1] + (1 - paramOpt[4]) ** 2 * paramOpt[3])

    chiSq = stats.chisquare(vdmEventYields / totalEvents, f_exp=vdmPredicted / np.sum(vdmPredicted))

    #paramOpt, cov = optimize.curve_fit(pdfs.oneDimGauss, xAxisYields, vdmEventYields / totalEvents, bounds=((-np.inf, -np.inf), (np.inf, np.inf)))
    #vdmPredicted = pdfs.oneDimGauss(xAxisYields, paramOpt[0], paramOpt[1])

    #print(vdmPredicted)
    print(width)
    plt.plot(xAxisYields, vdmPredicted * totalEvents, label="fit", color='r')
    #plt.plot(xAxisYields, pdfs.oneDimGauss(xAxisYields, paramOpt[0], paramOpt[1]) * totalEvents, label="CompOne", color='g')
    #plt.plot(xAxisYields, pdfs.oneDimGauss(xAxisYields, paramOpt[2], paramOpt[3]) * totalEvents, label="CompTwo", color='y')

    plt.legend()

    plt.xlabel(r"$\Delta$x [arbitrary units]")
    plt.ylabel(r"Rate")
    plt.yscale("log")
    plt.gca().set_ylim(bottom=0.3)
    plt.savefig("testVDM.png")
    plt.show()

    #print(totalEvents)
    #print(chiSq)
    # manage fit results

    return (totalEvents, chiSq, width)
