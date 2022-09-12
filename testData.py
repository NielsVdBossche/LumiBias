import numpy as np
import matplotlib.pyplot as plt

baseDir = "InputVtx/"

stepInfo = "6016_steps.txt"
yieldInfo = "6016_vertex_steps.npz"
# stepInfo = "6868_steps.txt"
# yieldInfo = "6868_vertex_steps.npz"


inputYields = np.load(baseDir+yieldInfo)['data']
steps = np.loadtxt(baseDir+stepInfo, delimiter=',')[29:30]

yieldsPerTimestampWidth = np.zeros(25)
inputYields = inputYields[inputYields[:, 3]>14]

yieldsTotalRange = inputYields[np.logical_and(inputYields[:,0]>=steps[0,0], inputYields[:,0]<=steps[-1,1])]

for i, step in enumerate(steps): 
    yieldsInTimerange = inputYields[np.logical_and(inputYields[:,0]>=step[0], inputYields[:,0]<=step[1])]
    yieldsPerTimestampWidth[i] = len(yieldsInTimerange) / (step[1] - step[0])

curr = yieldsInTimerange[0,0]
endIndex = 0

values, counts = np.unique(yieldsInTimerange[:,0]-yieldsInTimerange[0,0], return_counts=True)

plt.scatter(values, counts)

#plt.plot(yieldsTotalRange[:,0]-yieldsTotalRange[0,0])

plt.show()
