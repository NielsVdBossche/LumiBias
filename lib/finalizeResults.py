from scipy import integrate
import numpy as np

def areaCorrection(pdf, parameters, scanResults):

    area_True, err = integrate.dblquad(pdf, -30., 30., lambda x : -30., lambda x : 30., args=(parameters,))

    dx, (xScan, yScan) = scanResults

    area_VdM_DG = 2 * np.pi * xScan[0] * yScan[0]
    area_VdM_SG = 2 * np.pi * xScan[4][1] * yScan[4][1]

    return (area_VdM_SG - 1/area_True) * area_True, (area_VdM_DG - 1/area_True) * area_True
