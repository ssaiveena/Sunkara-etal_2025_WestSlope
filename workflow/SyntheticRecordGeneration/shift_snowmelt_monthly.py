import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def readFiles(filename, firstLine, numSites):
    # read in all monthly flows and re-organize into nyears x 12 x nsites matrix
    with open(filename, 'r') as f:
        all_split_data = [x.split('.') for x in f.readlines()]

    f.close()

    numYears = int((len(all_split_data) - firstLine) / numSites)
    MonthlyQ = np.zeros([12 * numYears, numSites])
    sites = []
    for i in range(numYears):
        for j in range(numSites):
            index = firstLine + i * numSites + j
            sites.append(all_split_data[index][0].split()[1])
            all_split_data[index][0] = all_split_data[index][0].split()[2]
            MonthlyQ[i * 12:(i + 1) * 12, j] = np.asfarray(all_split_data[index][0:12], float)

    MonthlyQ = np.reshape(MonthlyQ, [int(np.shape(MonthlyQ)[0] / 12), 12, numSites])

    return MonthlyQ


def shift_snowmelt(xbmPath, numNodes, Basin, lastNode):
    '''
    creates and saves a .npy file containing an ensemble of shifted time-series with fractions of total annual flow
    and returns values for plotting

    :param xbmPath:             str, path to the xbm file
    :param numNodes:            float, the number of nodes in the statemod basin
    :param Basin:               str, name of basin (cm, gm, sj, ym, wm)
    :param lastNode             float, the last node of the xbm file (ie -1 for last node)

    :returns:
        - LastNodeFractions     numpy array, shifted fractions of annual flow (per month) for each year
        - HistNodeFractions     numpy array, historical fractions of annual flow per month for each year
    '''

    # read in monthly flows at all sites
    MonthlyQ_hist = readFiles(xbmPath, 16, numNodes)

    flattenedHistLastNode = MonthlyQ_hist[:, :, lastNode].flatten()

    LastNodeShifted = np.zeros(len(flattenedHistLastNode))
    LastNodeShifted[:-1] = flattenedHistLastNode[1:]
    LastNodeShifted[-1] = np.median(MonthlyQ_hist[:,0, lastNode]) # we lose one year of data, add the median for Oct

    LastNodeShifted_annual = np.reshape(LastNodeShifted, [105,12])

    # calculate the fraction of flow from every month at the last node
    HistLastNodeFractions = np.zeros([105, 12])
    LastNodeFractions = np.zeros([105,12])
    for i in range(105):
        HistLastNodeFractions[i, :] = MonthlyQ_hist[i, :, lastNode] / np.sum(MonthlyQ_hist[i, :, lastNode])
        LastNodeFractions[i,:] = LastNodeShifted_annual[i, :] / np.sum(LastNodeShifted_annual[i,:])

    np.savetxt('ClimateRealizations/FlowShifts/' + Basin + '_shiftedflows.csv', LastNodeFractions, delimiter=',')

    return HistLastNodeFractions, LastNodeFractions

#%%
def plot_shits(hist, shifted, name):
    fig = plt.figure()
    plt.plot(np.arange(12), hist[0,:], c = 'cornflowerblue')
    plt.plot(np.arange(12), shifted[0, :], c='goldenrod')
    plt.legend(['Historical', 'Shifted'])
    for i in range(105):
        plt.plot(np.arange(12), hist[i,:], c = 'cornflowerblue')
        plt.plot(np.arange(12), shifted[i, :], c='goldenrod')
        plt.xlabel('Month')
        plt.ylabel('Fraction of annual flow')
    plt.title(name + ' Fractional Flows')
    plt.savefig('Figures/ClimateRealizations/'+ name + '/shiftedFractions.png')


#%%
cm_hist_fractions, cm_fractions = shift_snowmelt('historical_data/cm2015_Statemod/StateMod/cm2015x.xbm', 208, 'cm', -1)
plot_shits(cm_hist_fractions, cm_fractions, 'cm')

gm_hist_fractions, gm_fractions = shift_snowmelt('historical_data/gm2015_Statemod/StateMod/gm2015x.xbm', 139, 'gm', -1)
plot_shits(gm_hist_fractions, gm_fractions, 'gm')
#%%
ym_hist_fractions, ym_fractions = shift_snowmelt('historical_data/ym2015_Statemod/StateMod/ym2015x.xbm', 94, 'ym', -3)
plot_shits(ym_hist_fractions, ym_fractions, 'ym')

wm_hist_fractions, wm_fractions = shift_snowmelt('historical_data/wm2015_Statemod/StateMod/wm2015x.xbm', 43, 'wm', -2)
plot_shits(wm_hist_fractions, wm_fractions, 'wm')
#%%
sj_hist_fractions, sj_fractions = shift_snowmelt('historical_data/sj2015_Statemod/StateMod/sj2015x.xbm', 165, 'sj', -1)
plot_shits(sj_hist_fractions, sj_fractions, 'sj')