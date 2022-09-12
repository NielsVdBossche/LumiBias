# first run on joscha's results
import RunVDMSim as vdm
import numpy as np

import matplotlib.pyplot as plt

if __name__ == "__main__":
    models = [["SingleGauss", "SG"], ["DoubleGauss", "DG"], ["TripleGauss", "TG"], ["SuperGauss", "SupG"], ["SuperDoubleGauss", "SupDG"]]
    bcids = ["41", "281", "872", "1783", "2063"]
    plainResults = np.zeros((len(models), len(bcids), 2), dtype=np.float64)
    
    filepath = "/home/njovdnbo/Documents/EPR/LumiBias/Data/Results_Joscha/"
    """
    avgs = np.zeros(len(models), dtype=np.float64)
    for i, model in enumerate(models):
        modelResults = []
        for id in bcids:
            path = filepath + model[0] + "/" + "Fill6016_" + model[1] + "_bcid" + id + ".json"

            modelResults.append(vdm.runVDMSimOnJSON(path))

        avgs[i] = np.average(modelResults)
        plainResults[i] = np.array(modelResults)
        print(model[0] + ":")
        print(modelResults)

    print(avgs)
    print(plainResults)

    np.savez("vdmSimResultsFitsJoscha.npz", SG=plainResults[0], DG=plainResults[1], TG=plainResults[2], SupG=plainResults[3], SupDG=plainResults[4])
    """
    
    px = 1/plt.rcParams['figure.dpi']
    fig, ((ax1, ax3)) = plt.subplots(1, 2, sharex='col', sharey='row', figsize=(1000*px, 400*px))
    
    npzfile = np.load("vdmSimResultsFitsAngela.npz")
    plainResults[0] = npzfile["SG"]
    plainResults[1] = npzfile["DG"]
    plainResults[2] = npzfile["TG"]
    plainResults[3] = npzfile["SupG"]
    plainResults[4] = npzfile["SupDG"]
    x = np.linspace(1, len(bcids), len(bcids))
    colors = ['b', 'r', 'g', 'y', 'm']
    for i, model in enumerate(models):
        ax1.scatter(x, plainResults[i, :, 0], label=model[0], s=8., c=colors[i])
        ax3.scatter(x, plainResults[i, :, 1], label=model[0], s=8., c=colors[i])

    ax1.title.set_text("Single gauss fits")
    ax3.title.set_text("Double gauss fits")
    """
    npzfile = np.load("vdmSimResultsFitsJoscha.npz")
    plainResults[0] = npzfile["SG"]
    plainResults[1] = npzfile["DG"]
    plainResults[2] = npzfile["TG"]
    plainResults[3] = npzfile["SupG"]
    plainResults[4] = npzfile["SupDG"]
    for i, model in enumerate(models):
        ax2.scatter(x, plainResults[i, :, 0], label=model[0], s=8., c=colors[i])
        ax4.scatter(x, plainResults[i, :, 1], label=model[0], s=8., c=colors[i])

    ax2.title.set_text("Single gauss fits Joscha")
    ax4.title.set_text("Double gauss fits Joscha")
    """
    ax1.set_xticks(x, bcids)
    #ax2.set_xticks(x, bcids)
    ax3.set_xticks(x, bcids)
    #ax4.set_xticks(x, bcids)

    ax3.set_xlabel("bcid")
    ax1.set_xlabel("bcid")
    ax1.legend()


    plt.savefig("Output/FitResultsAngela.png", bbox_inches='tight')
    #plt.show()

    ## plot each of these results




    



# compare results to angela's fits
# systematic effect of BI vs VDM
# other stuff