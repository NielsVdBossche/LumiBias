import lib.beamPDFs as beamPDFs
import lib.pdfs as pdfs
import lib.jsonTools as jsonTools

import matplotlib.pyplot as plt
import numpy as np

def plotVDMResults(ScanSteps, results):
    xRes = results[0]
    yRes = results[1]

    fig, (ax1, ax2) = plt.subplots(1,2)

    ax1.scatter(ScanSteps, xRes[2], s=15., label="VdM Sim")
    ax1.title.set_text('X-scan')
    ax1.set_xlabel(r"$\Delta$ x [a.u.]")
    ax1.set_yscale("log")
    ax1.set_ylabel(r"Rate")
    ax1.grid(True, which="both")

    ax2.scatter(ScanSteps, yRes[2], s=15., label="VdM Sim")
    ax2.title.set_text('Y-scan')
    ax2.set_xlabel(r"$\Delta$ y [a.u.]")
    ax2.set_yscale("log")
    ax2.set_ylabel(r"Rate")
    ax2.grid(True, which="both")

    return (fig, (ax1, ax2))

def plotVDMResultsAndData(ScanSteps, results):

    fig, (ax1, ax2) = plotVDMResults(ScanSteps, results)

    file = jsonTools.openFile("Rates_HFOC_6016.json")
    hfocData = jsonTools.getXandYData(file)

    ax1.scatter(ScanSteps, hfocData[0], label="VdM data", s=15.)
    ax2.scatter(ScanSteps, hfocData[1], label="VdM data", s=15.)

    return (fig, (ax1, ax2))

def plotFitResults(results, fig):
    _, (ax1, ax2) = fig

    scanSteps = np.linspace(-12., 12., 250)

    xParams = results[0][3]
    xPredictedYield = pdfs.oneDimDoubleGauss(scanSteps, xParams[0], xParams[1], xParams[2], xParams[3], xParams[4])
    xNorm = np.sum(results[0][2])
    ax1.plot(scanSteps, xPredictedYield / xNorm, label="Best fit")

    yParams = results[1][3]
    yPredictedYield = pdfs.oneDimDoubleGauss(scanSteps, yParams[0], yParams[1], yParams[2], yParams[3], yParams[4])
    yNorm = np.sum(results[1][2])
    ax2.plot(scanSteps, yPredictedYield / yNorm, label="Best fit")

    return fig





