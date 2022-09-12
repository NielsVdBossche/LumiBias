import numpy as np
import matplotlib.pyplot as plt

import RunVDMSim as vdmHandler
import lib.VDMSim as vdm
import lib.finalizeResults as res
import json
import lib.pdfs as pdfs


def runVDMSimFullOutput(jsonFilePath):
    # requires a JSON-file
    f = open(jsonFilePath)
    parameterFile = json.load(f)

    model, parameters = vdmHandler.readParameterFile(parameterFile)
    
    nSteps = 25

    results = vdm.RunVdmScanSim(model, parameters, nSteps=nSteps)
    sgArea, dgArea, trueArea, sgBias, dgBias = res.areaCorrectionFull(model, parameters, results)
    
    return results, sgBias, dgBias, sgArea, dgArea, trueArea

if __name__ == "__main__":
    # open files
    # run test
    bcid_1 = input("BCID 1: ")
    bcid_2 = input("BCID 2: ")

    models = [["SingleGauss", "SG"], ["DoubleGauss", "DG"], ["TripleGauss", "TG"], ["SuperGauss", "SupG"], ["SuperDoubleGauss", "SupDG"]]
    #models = [["SuperDoubleGauss", "SupDG"]]

    filepath = "/home/njovdnbo/Documents/EPR/LumiBias/Data/"
    px = 1/plt.rcParams['figure.dpi']

    for model in models:
        path_1 = filepath + model[0] + "/" + "Fill6016_" + model[1] + "_bcid" + bcid_1 + ".json"
        path_2 = filepath + model[0] + "/" + "Fill6016_" + model[1] + "_bcid" + bcid_2 + ".json"

        res_1, sg_1, dg_1, sgArea_1, dgArea_1, trueArea_1 = runVDMSimFullOutput(path_1)
        res_2, sg_2, dg_2, sgArea_2, dgArea_2, trueArea_2 = runVDMSimFullOutput(path_2)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(1000*px, 800*px))

        # show desired results
        dx, (xScan, yScan) = res_1
        print("bcid " + bcid_1 + " SG x width: {}".format(xScan[4][1]))
        print("bcid " + bcid_1 + " SG y width: {}".format(yScan[4][1]))
        print("bcid " + bcid_1 + " SG y fit components: {}".format(yScan[4]))
        print("bcid " + bcid_1 + " SG x fit components: {}".format(xScan[4]))

        print("bcid " + bcid_1 + " DG x width: {}".format(xScan[0]))
        print("bcid " + bcid_1 + " DG x width comp 1: {}".format(xScan[3][1]))
        print("bcid " + bcid_1 + " DG x width comp 2: {}".format(xScan[3][3]))
        print("bcid " + bcid_1 + " DG y width: {}".format(yScan[0]))
        print("bcid " + bcid_1 + " DG y width comp 1: {}".format(yScan[3][1]))
        print("bcid " + bcid_1 + " DG y width comp 2: {}".format(yScan[3][3]))
        print("bcid " + bcid_1 + " DG y fit components: {}".format(yScan[3]))
        print("bcid " + bcid_1 + " DG x fit components: {}".format(xScan[3]))


        print("bcid " + bcid_1 + " true area: {}".format(trueArea_1))
        print("bcid " + bcid_1 + " SG area: {}".format(sgArea_1))
        print("bcid " + bcid_1 + " DG area: {}".format(dgArea_1))

        print("bcid " + bcid_1 + " SG Bias: {}".format(sg_1))
        print("bcid " + bcid_1 + " DG Bias: {}".format(dg_1))

        # xscan BCID 1
        ax1.scatter(dx, xScan[2], s=15., label="Sim yields")

        scanSteps = np.linspace(-(25 - 1) / 2., (25 - 1) / 2., num=251, endpoint=True)
        sgFit_1_x = pdfs.oneDimGaussAlt(scanSteps, xScan[4])
        scale = sgFit_1_x[125]
        sgFit_1_x /= (scale)
        normFactor = 1 / 0.00633
        sgFit_1_x /= normFactor

        ax1.plot(scanSteps, sgFit_1_x, label="SG Fit", c='r')

        dgFit_1_x = pdfs.oneDimDoubleGaussAlt(scanSteps, xScan[3])
        scale = dgFit_1_x[125]
        dgFit_1_x /= (scale)
        dgFit_1_x /= normFactor

        ax1.plot(scanSteps, dgFit_1_x, label="DG Fit", c='g')

        ax1.title.set_text("bcid " + bcid_1)

        # yscan BCID 1
        ax3.scatter(dx, yScan[2], s=15., label="Sim yields")

        sgFit_1_y = pdfs.oneDimGaussAlt(scanSteps, yScan[4])
        scale = sgFit_1_y[125]
        sgFit_1_y /= (scale)
        normFactor = 1 / 0.00633
        sgFit_1_y /= normFactor

        ax3.plot(scanSteps, sgFit_1_y, label="SG Fit", c='r')

        dgFit_1_y = pdfs.oneDimDoubleGaussAlt(scanSteps, yScan[3])
        scale = dgFit_1_y[125]
        dgFit_1_y /= (scale)
        dgFit_1_y /= normFactor

        ax3.plot(scanSteps, dgFit_1_y, label="DG Fit", c='g')

        ax3.title.set_text("bcid " + bcid_1)


        # xscan BCID 2
        dx, (xScan, yScan) = res_2
        print("bcid " + bcid_2 + " SG x width: {}".format(xScan[4][1]))
        print("bcid " + bcid_2 + " SG y width: {}".format(yScan[4][1]))
        print("bcid " + bcid_2 + " SG y fit components: {}".format(yScan[4]))
        print("bcid " + bcid_2 + " SG x fit components: {}".format(xScan[4]))

        print("bcid " + bcid_2 + " DG x width: {}".format(xScan[0]))
        print("bcid " + bcid_2 + " DG x width comp 1: {}".format(xScan[3][1]))
        print("bcid " + bcid_2 + " DG x width comp 2: {}".format(xScan[3][3]))
        print("bcid " + bcid_2 + " DG y width: {}".format(yScan[0]))
        print("bcid " + bcid_2 + " DG y width comp 1: {}".format(yScan[3][1]))
        print("bcid " + bcid_2 + " DG y width comp 2: {}".format(yScan[3][3]))
        print("bcid " + bcid_2 + " DG y fit components: {}".format(yScan[3]))
        print("bcid " + bcid_2 + " DG x fit components: {}".format(xScan[3]))


        print("bcid " + bcid_2 + " true area: {}".format(trueArea_2))
        print("bcid " + bcid_2 + " SG area: {}".format(sgArea_2))
        print("bcid " + bcid_2 + " DG area: {}".format(dgArea_2))

        print("bcid " + bcid_2 + " SG Bias: {}".format(sg_2))
        print("bcid " + bcid_2 + " DG Bias: {}".format(dg_2))

        ax2.scatter(dx, xScan[2], s=15., label="Sim yields")

        scanSteps = np.linspace(-(25 - 1) / 2., (25 - 1) / 2., num=251, endpoint=True)
        sgFit_2_x = pdfs.oneDimGaussAlt(scanSteps, xScan[4])
        scale = sgFit_2_x[125]
        sgFit_2_x /= (scale)
        normFactor = 1 / 0.00633
        sgFit_2_x /= normFactor

        ax2.plot(scanSteps, sgFit_2_x, label="SG Fit", c='r')

        dgFit_2_x = pdfs.oneDimDoubleGaussAlt(scanSteps, xScan[3])
        scale = dgFit_2_x[125]
        dgFit_2_x /= (scale)
        dgFit_2_x /= normFactor

        ax2.plot(scanSteps, dgFit_2_x, label="DG Fit", c='g')

        ax2.title.set_text("bcid " + bcid_2)

        # yscan BCID 2
        ax4.scatter(dx, yScan[2], s=15., label="Sim yields")

        sgFit_2_y = pdfs.oneDimGaussAlt(scanSteps, yScan[4])
        scale = sgFit_2_y[125]
        sgFit_2_y /= (scale)
        normFactor = 1 / 0.00633
        sgFit_2_y /= normFactor

        ax4.plot(scanSteps, sgFit_1_y, label="SG Fit", c='r')

        dgFit_2_y = pdfs.oneDimDoubleGaussAlt(scanSteps, yScan[3])
        scale = dgFit_2_y[125]
        dgFit_2_y /= (scale)
        dgFit_2_y /= normFactor

        ax4.plot(scanSteps, dgFit_2_y, label="DG Fit", c='g')

        ax4.title.set_text("bcid " + bcid_2)

        ax1.legend()

        # finalize figures

        ax1.set_xlabel(r"$\Delta$ x [a.u.]")
        ax2.set_xlabel(r"$\Delta$ x [a.u.]")

        ax3.set_xlabel(r"$\Delta$ y [a.u.]")
        ax4.set_xlabel(r"$\Delta$ y [a.u.]")


        ax1.set_ylabel(r"Rate")
        ax3.set_ylabel(r"Rate")

        ax1.grid(True, which="both")
        ax2.grid(True, which="both")
        ax3.grid(True, which="both")
        ax4.grid(True, which="both")
        ax1.set_yscale("log")
        ax2.set_yscale("log")
        ax3.set_yscale("log")
        ax4.set_yscale("log")

        plt.savefig("Output/" + model[0] + "_bcids_" + bcid_1 + "_" + bcid_2)