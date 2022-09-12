import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, stats, integrate
import lib.pdfs as pdfs

from math import sqrt

# load data
# visualize

baseDir = "InputVtx/"

stepInfo = "6016_steps.txt"
yieldInfo = "6016_vertex_steps.npz"
# stepInfo = "6868_steps.txt"
# yieldInfo = "6868_vertex_steps.npz"

if __name__ == "__main__":
    ####   

    inputYields = np.load(baseDir+yieldInfo)['data']
    steps = np.loadtxt(baseDir+stepInfo, delimiter=',')[15:40]

    yieldsPerTimestampWidth = np.zeros(25)
    uncPerTimestampWidth = np.zeros(25)
    x = np.linspace(-12., 12., num=25, endpoint=True)

    inputYields = inputYields[inputYields[:, 3]>14]


    for i, step in enumerate(steps): 
        yieldsInTimerange = inputYields[np.logical_and(inputYields[:,0]>=step[0], inputYields[:,0]<=step[1])]

        values, counts = np.unique(yieldsInTimerange[:,0], return_counts=True)
        poissonErrorsOnCounts = np.sqrt(counts)
        avgCount = np.average(counts)
        stdDevOnAvg = np.std(counts, ddof=1)

        yieldsPerTimestampWidth[i] = len(yieldsInTimerange) / (step[1] - step[0]) #avgCount #
        uncPerTimestampWidth[i] = stdDevOnAvg # np.sqrt(avgCount)

    
    px = 1/plt.rcParams['figure.dpi']
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', sharey='row', figsize=(500*px, 600*px), gridspec_kw={'height_ratios': [5, 1]})

    ax1.errorbar(x, yieldsPerTimestampWidth, fmt="none", yerr=uncPerTimestampWidth, elinewidth=1.)
    ax1.scatter(x, yieldsPerTimestampWidth, s=15., label="Data")
    ax1.set_yscale("log")

    ax2.hlines(1., x[0], x[-1], colors='k', linestyles='dashed', linewidths=1.)


    totalEventYield = np.sum(yieldsPerTimestampWidth)
    # single gauss als first guess + force fit to be at 0 centered
    DGParam, cov = optimize.curve_fit(pdfs.oneDimDoubleGauss, x, yieldsPerTimestampWidth / totalEventYield, p0=(0., 2.5, 0., 25., 0.5), bounds=((-0.00001, 1.5, -0.00001, 1.5, 0.), (0.00001, 30., 0.00001, 30., 1.)))
    vdmPredicted = pdfs.oneDimDoubleGauss(x, DGParam[0], DGParam[1], DGParam[2], DGParam[3], DGParam[4])
    width = 1 / (( (DGParam[4] / DGParam[1]) + ((1-DGParam[4]) / DGParam[3]) ))

    SGParam, cov = optimize.curve_fit(pdfs.oneDimGauss, x, yieldsPerTimestampWidth / totalEventYield, bounds=((-0.001, 1.5), (0.001, 30.)))
    
    scanSteps = np.linspace(-(25 - 1) / 2., (25 - 1) / 2., num=251, endpoint=True)
    sgFit_1_x = pdfs.oneDimGaussAlt(scanSteps, SGParam)
    scale = sgFit_1_x[125]
    sgFit_1_x /= (scale)
    normFactor = 1 / yieldsPerTimestampWidth[12]
    sgFit_1_x /= normFactor

    ax1.plot(scanSteps, sgFit_1_x, label="SG Fit", c='r')
    ax1.legend()

    sgFit_1_x_sparse = pdfs.oneDimGaussAlt(x, SGParam)
    scale = sgFit_1_x_sparse[12]
    sgFit_1_x_sparse /= (scale)
    normFactor = 1 / yieldsPerTimestampWidth[12]
    sgFit_1_x_sparse /= normFactor

    ax2.scatter(x, yieldsPerTimestampWidth/sgFit_1_x_sparse, s=15.)
    ax2.errorbar(x, yieldsPerTimestampWidth/sgFit_1_x_sparse, fmt="none", yerr=uncPerTimestampWidth/sgFit_1_x_sparse)

    plt.subplots_adjust(hspace=0., top=0.95, bottom=0.05)
    plt.savefig("OutputVtx/test.png")
    
    


    ## select right range of data based on txt file i guess
    # next: 
    
    # bunch per timerange, divide by timing, also try division by number of entries ofzo, idk average out in a logical way
    # get statistical uncertainty related to this... Start with sqrt and think more logically about it afterwards
    # plot for each separation -> Should already be split based on separation
    
    # plot & visualize

    # 
