import json
import numpy as np

f = open("/home/njovdnbo/Documents/EPR/Lumi/lumiData/Rates_HFOC_6016.json")

data = json.load(f)
        
data = data["Scan_2"]

i = 0

while data[i]["ScanPoint"] != 13:
    i += 1

rates = data[i]["Rates"]
errors = data[i]["RateErrs"]

rates_list = []
errors_list = []

for key in rates.keys():
    if (key == "sum"): continue
    rates_list.append(rates[key])
    errors_list.append(errors[key])

rates = np.array(rates_list)
errors = np.array(errors_list)

print("Average rate: {}".format(np.average(rates)))
print("Average error: {}".format(np.average(errors)))
print("relative error: {}".format(np.average(errors) / np.average(rates)))