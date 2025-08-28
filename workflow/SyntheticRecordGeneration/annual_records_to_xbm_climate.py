#%%
import numpy as np
import pandas as pd
from random import random
import xbm_iwr_utils
from tqdm import tqdm

def HMM_to_xbm(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column, r):
    '''
    Disaggregates annual synthetic records across space and time and writes new xbm files for input to StateMod

    :param abbrev:            string, abbreviation for current basin
    :param nSites:            float, number of nodes in current basin
    :param startXBM:          float, line number where comments in xbm file end
    :param xbm_file:          string, xbm file from historical record for input to organize monthly function in xbm_iwr_utils
    :param abbrev_file_xbm:   string, base name of xbm file to be written
    :param last node:         float, node in the StateMod network that data is fit to (usually -1, sometimes -2 or -3)
    :param historical_column: float, column of historical data with basin data
    :param r:                 float, realization number
    '''
    nYears = 105
    AnnualQ_s = np.array(pd.read_csv('../../Synthetic_records/ClimateAdjusted_zero_zero_five/AnnualQ_s' + str(r) + '.txt', sep=' ',
                                     header=None))

    # load annual and monthly flow files
    MonthlyQ_h = np.array(pd.read_csv('../../historical_data/' + abbrev + '2015_StateMod/MonthlyQ.csv', header=None))
    AnnualQ_h = np.array(pd.read_csv('../../historical_data/' + abbrev + '2015_Statemod/AnnualQ.csv', header=None))

    # Read in monthly flows at all sites
    MonthlyQ_all = organizeMonthly(xbm_file, startXBM, nSites)
    MonthlyQ_all_ratios = np.zeros(np.shape(MonthlyQ_all))

    # if zeros are in the data, make them temporarily ones to prevent true divide
    zero_value_indices = np.where(MonthlyQ_all == 0)
    MonthlyQ_all[zero_value_indices] = 1

    # Divide monthly flows at each site by the monthly flow at the last node
    for i in range(np.shape(MonthlyQ_all_ratios)[2]):
        MonthlyQ_all_ratios[:, :, i] = MonthlyQ_all[:, :, i] / MonthlyQ_all[:, :, last_node]

    # revert back to zero
    MonthlyQ_all[zero_value_indices] = 0

    # Get historical flow ratios
    AnnualQ_h_ratios = np.zeros(np.shape(AnnualQ_h))
    for i in range(np.shape(AnnualQ_h_ratios)[0]):
        AnnualQ_h_ratios[i, :] = AnnualQ_h[i, :] / np.sum(AnnualQ_h[i, last_node])

    # Get historical flow ratios for last node monthly
    last_node_breakdown = np.zeros([105, 12])
    for i in range(np.shape(last_node_breakdown)[0]):
        last_node_breakdown[i, :] = MonthlyQ_all[i, :, last_node] / AnnualQ_h[i, last_node]

    MonthlyQ_s = np.zeros([nYears, nSites, 12])
    # disaggregate annual flows and demands at all sites using randomly selected neighbor from k nearest based on flow
    dists = np.zeros([nYears, np.shape(AnnualQ_h)[0]])
    for j in range(nYears):
        for m in range(np.shape(AnnualQ_h)[0]):
            dists[j, m] = dists[j, m] + (AnnualQ_s[j, historical_column] - AnnualQ_h[m, last_node]) ** 2

    # Create probabilities for assigning a nearest neighbor for the simulated years
    probs = np.zeros([int(np.sqrt(np.shape(AnnualQ_h)[0]))])
    for j in range(len(probs)):
        probs[j] = 1 / (j + 1)
        probs = probs / np.sum(probs)
        for j in range(len(probs) - 1):
            probs[j + 1] = probs[j] + probs[j + 1]
    probs = np.insert(probs, 0, 0)

    LastNodeFractions = np.loadtxt('../../ClimateRealizations/FlowShifts/' + abbrev + '_shiftedflows.csv', delimiter=',')

    for j in range(nYears):
        # select one of k nearest neighbors for each simulated year
        neighbors = np.sort(dists[j, :])[0:int(np.sqrt(np.shape(AnnualQ_h)[0]))]
        indices = np.argsort(dists[j, :])[0:int(np.sqrt(np.shape(AnnualQ_h)[0]))]
        randnum = random()
        for k in range(1, len(probs)):
            if randnum > probs[k - 1] and randnum <= probs[k]:
                neighbor_index = indices[k - 1]


        # Use selected neighbors to downscale flows and apply snowmelt shift each year at last node
        proportions = LastNodeFractions[neighbor_index, :]
        MonthlyQ_s[j, last_node, :] = AnnualQ_s[j, historical_column] * proportions


        # Find monthly flows at all other sites each year
        for k in range(12):
            MonthlyQ_s[j, :, k] = MonthlyQ_all_ratios[neighbor_index, k, :] * MonthlyQ_s[j, last_node, k]

    # write new flows to file for LHsample i (inputs: filename, firstLine, sampleNo,realization, allMonthlyFlows,output folder)
    writeNewStatemodFiles(abbrev_file_xbm, abbrev, startXBM, r, 1, MonthlyQ_s, xbm_out)



name = 'Upper_Colorado'
abbrev = 'cm'
nSites = 208
startXBM = 16
xbm_file = '../../historical_data/' + abbrev + '2015_Statemod/StateMod/cm2015x.xbm'
xbm_out = '../../Adjusted_stateMod_input_files/.xbm/ClimateAdjusted_zero_zero_five/Upper_Colorado/'
abbrev_file_xbm = 'cm2015x.xbm'
historical_column = 0
last_node = -1
r = 0

for r in range(1000):
    HMM_to_xbm(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column, r)
print('Done')

name='Gunnison'
abbrev='gm'
nSites=139
startXBM=16
xbm_file='../../historical_data/'+abbrev+'2015_Statemod/StateMod/gm2015x.xbm'
xbm_out='../../Adjusted_stateMod_input_files/.xbm/ClimateAdjusted_zero_zero_five/Gunnison/'
abbrev_file_xbm='gm2015x.xbm'
abbrev_file_iwr='gm2015B.iwr'
historical_column=1
last_node = -1

for r in range(0,1000):
    HMM_to_xbm(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column,r)
print('Done')

name='San_Juan'
abbrev='sj'
nSites=165
nIWRSites=296
startXBM=16
startIWR=377
xbm_file='../../historical_data/'+abbrev+'2015_Statemod/StateMod/sj2015x.xbm'
xbm_out='../../Adjusted_stateMod_input_files/.xbm/ClimateAdjusted_zero_zero_five/SanJuan_Dolores/'
abbrev_file_xbm='sj2015x.xbm'
last_node = -1
historical_column=4

for r in range(0, 1000):
    HMM_to_xbm(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column, r)
print('Done')

name='Yampa'
abbrev='ym'
nSites=94
nIWRSites=298
startXBM=16
xbm_file='../../historical_data/'+abbrev+'2015_Statemod/StateMod/ym2015x.xbm'
xbm_out='../../Adjusted_stateMod_input_files/.xbm/ClimateAdjusted_zero_zero_five/Yampa/'
abbrev_file_xbm='ym2015x.xbm'
historical_column=2
last_node = -3
for r in range(0, 1000):
    HMM_to_xbm(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column, r)
print('Done')


name='White'
abbrev='wm'
nSites=43
startXBM=16
xbm_file='../../historical_data/'+abbrev+'2015_Statemod/StateMod/wm2015x.xbm'
xbm_out='../../Adjusted_stateMod_input_files/.xbm/ClimateAdjusted_zero_zero_five/White/'
abbrev_file_xbm='wm2015x.xbm'
historical_column=3
abbrev_file_iwr='wm2015B.iwr'
last_node = -2
for r in range(0,1000):
    HMM_to_xbm(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column,r)
print('Done')
