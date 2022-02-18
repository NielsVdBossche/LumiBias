import lib.VDMSim as vdm
import lib.beamPDFs as beamPDFs
import lib.finalizeResults as res
import sys
import numpy as np
import json

def readGaussianBeamComponent(physParam, beamNmbr, beamType, name):
    """
    name = e.g. "14trks"
    beamNmbr = 1 or 2
    beamType = "N", "M", "W"
    """
    w = "Width" + beamType + str(beamNmbr)
    xw = "x" + w
    yw = "y" + w
    r = "rho" + beamType + str(beamNmbr)
    # comp = "w" + beamType + beamNmbr
    return float(physParam[xw][name]) / 49.20, float(physParam[yw][name]) / 49.20, float(physParam[r][name]) #, float(physParam[comp][name])

def readGaussian(model, physParam, names):
    if "Single Gauss" == model: 
        physModel = beamPDFs.SingleGaussBeamOverlap
        types = ["N"]
    elif "Double Gauss" == model or model == "Super Gauss": 
        physModel = beamPDFs.DoubleGaussBeamOverlap
        types = ["N", "M"]
    elif "Triple Gauss" == model or model == "Super Double Gauss": 
        physModel = beamPDFs.TripleGaussBeamOverlap
        types = ["N", "M", "W"]

    beamParameters = np.zeros((2, 2 + len(types) * 3 + len(types) - 1))
    for i in range(1,3):
        beamComponents = np.zeros(2 + len(types) * 3 + len(types) - 1)
        for j, type in enumerate(types):
            beamComponents[2+j*3:2+j*3+3] = readGaussianBeamComponent(physParam, i, type, names)
            if not "Single" in model and j < len(types) - 1:
                #if "Double" in model and type == "N":
                comp = "w" + str(i) + type
                beamComponents[- len(types) + 1 + j] = float(physParam[comp][names]) / 100
            #elif "Triple" in model:

        
        beamParameters[i-1,:] = beamComponents

    print(beamParameters)
    return physModel, beamParameters


def readParameterFile(paramFile):
    model = paramFile["modelname"]

    names = paramFile["names"][0]
    physParam = paramFile["physics"]

    # depends on model which parameters, start with N anyway

    # depending on model, have components ready

    if " Gauss" in model:
        return readGaussian(model, physParam, names)
    
    return None



if __name__ == "__main__":
    parameterFileName = sys.argv[1]

    # load json file
    # general opening function for json, reads type of fit
    # type of fit then gets used to choose pdf

    f = open(parameterFileName)
    parameterFile = json.load(f)

    model, parameters = readParameterFile(parameterFile)
    
    nSteps = 25
    nominalRun = True

    for i in range(2, len(sys.argv)):
        if (sys.argv[i] == "BI"): nSteps = 19

    results = vdm.RunVdmScanSim(model, parameters, nSteps=nSteps)
    sgBias, dgBias = res.areaCorrection(model, parameters, results)
    
    print("Single Gaussian correction factor: {}".format(sgBias))
    print("Double Gaussian correction factor: {}".format(dgBias))
