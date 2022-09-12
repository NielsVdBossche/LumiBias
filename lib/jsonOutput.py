import json
import numpy as np

def write_output_as_npz(vdmSimResults, sgBias, dgBias, filename="out.npz"):
    #### do stuff
    dx, (xScanResults, yScanResults) = vdmSimResults

    np.savez(filename, sgBias=sgBias, dgBias=dgBias, dx=dx, xWidth=xScanResults[0], xChiSq=xScanResults[1], xEvYield=xScanResults[2], xDGParam=xScanResults[3], xSGParam=xScanResults[4], yWidth=yScanResults[0], yChiSq=yScanResults[1], yEvYield=yScanResults[2], yDGParam=yScanResults[3], ySGParam=yScanResults[4])

if __name__ == "__main__":
    exit(0)