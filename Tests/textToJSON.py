import sys    

with open(sys.argv[1]) as f:
    params = f.readline().split()
    values = []

    for line in f:
        line = line.split()[1:]
        for el in line:
            if "µm" in el:
                el = el[:-2]
            if "%" in el:
                el = el[:-2]

            values.append(el)

for param, val in zip(params, values):
    outstring = '"' + param + '": {\n"14trks":"' + val+'"\n},\n'
    print(outstring)