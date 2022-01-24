import json
import numpy as np

def openFile(filename):
    f = open("/home/njovdnbo/Documents/EPR/LumiBias/lumiData/" + filename)
    data = json.load(f)

    return data

def getPeakAverage(data, axis="X"):
    if (axis == "X"):
        scan = "Scan_1"
    else:
        scan = "Scan_2"

    scanData = data[scan]
    rates = scanData[12]["Rates"]
    rates_list = []

    for key in rates.keys():
        if (key == "sum"): continue
        rates_list.append(rates[key])
    
    rates = np.array(rates_list)

    return np.average(rates)

def getData(data, axis="X"):
    if (axis == "X"):
        scan = "Scan_1"
    else:
        scan = "Scan_2"

    scanData = data[scan]
    ratesFinal = []

    for i in range(25):
        rates_list = []
        for key in scanData[i]["Rates"].keys():
            if (key == "sum"): continue
            rates_list.append(scanData[i]["Rates"][key])

        ratesFinal.append(np.average(rates_list))     

    return ratesFinal

def getXandYData(data):

    xData = getData(data, axis="X")
    yData = getData(data, axis="Y")

    return (xData, yData)