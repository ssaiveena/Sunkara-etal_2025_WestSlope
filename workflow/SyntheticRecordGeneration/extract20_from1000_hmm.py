import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import statistics
from tqdm import tqdm
from sys import exit
import matplotlib.cm as cm
import os
import random
import time
from multiprocessing import Pool
import json

def drought_statistics(file_name, hist_file, b, hist, drought_def):
    '''

    :param file_name: path to the annual Q file (string)
    :param hist_file: path to historical record
    :param b: basin index (float) cm=0, gm=1, ym=2, wm=3, sj=4
    :param hist: historical record toggle (bool)
    :param drought_def: size of moving window (float)
    :return: drought_instances (list) - all drought periods in the record
    :return: final_drought_range (list) ranges of years of decadal droughts in the recod
    :return: total_severity - sum of the difference between the mean & annual flows during a drought normalized by std
    '''
    if hist:
        AnnualQ_s = pd.read_csv(file_name, sep=',')
    else:
        with open(file_name, 'r') as file:
            AnnualQ_s = pd.read_csv(file, sep=' ', header=None) 
        # AnnualQ_s = pd.read_csv(file_name, sep=' ', header=None)
        AnnualQ_s.columns = ['cm', 'gm', 'ym', 'wm', 'sj']


    AnnualQ_s_hist = pd.read_csv(hist_file, sep=',')
    AnnualQ_s_hist['Year'] = list(range(1909, 2014))
    AnnualQ_s['Year'] = list(range(1909, 2014))


    std = statistics.stdev(AnnualQ_s_hist.iloc[:, b])
    threshold = np.mean(AnnualQ_s_hist.iloc[:, b]) - (0.5 * std)

    drought_instances = [i for i, v in enumerate(AnnualQ_s.iloc[:, b].rolling(drought_def).mean()) if v < threshold]
    drought_years = AnnualQ_s.iloc[:, 5].rolling(drought_def).mean()[drought_instances]

    drought_range = [range(0, 1)]
    j = 0
    for i in range(len(drought_years)):
        already_in = 0
        for j in range(len(drought_range)):
            if drought_years.iloc[i] in drought_range[j]:
                already_in = 1
        if already_in == 0:
            start_year = drought_years.iloc[i] - drought_def/2
            end_year = drought_years.iloc[i] + drought_def/2
            drought_range.append(range(int(start_year), int(end_year)))
        elif already_in == 1:
            if drought_years.iloc[i] - drought_def/2 < start_year:
                start_year = drought_years.iloc[i] - drought_def/2
            if drought_years.iloc[i] + drought_def/2 > end_year:
                end_year = drought_years.iloc[i] + drought_def/2
            drought_range.append(range(int(start_year), int(end_year)))

    # combine overlapping periods
    final_drought_range = []
    for i in range(1, len(drought_range)):
        if final_drought_range:
            if min(drought_range[i]) < max(final_drought_range[-1]):
                final_drought_range[-1] = range(min(final_drought_range[-1]), max(drought_range[i]) + 1)
            elif min(drought_range[i]) < min(drought_range[i - 1]):
                final_drought_range.append(range(min(drought_range[i - 1]), int(max(drought_range[i]) + 1)))
            else:
                final_drought_range.append(drought_range[i])
        else:
            if min(drought_range[i]) < min(drought_range[i - 1]):
                final_drought_range.append(range(min(drought_range[i - 1]), max(drought_range[i]) + 1))
            else:
                final_drought_range.append(drought_range[i])

    total_severity = []
    if drought_instances:
        for i in range(len(final_drought_range)):
            cur_severity = 0
            for j in range(105):
                if AnnualQ_s.iloc[j, 5] in final_drought_range[i]:
                    #cur_severity += (np.mean(AnnualQ_s_hist.iloc[:, b]) - AnnualQ_s.iloc[j,b])/std
                    cur_severity += (AnnualQ_s_hist.iloc[:, b].mean() - AnnualQ_s.iloc[j, b])/std
            total_severity.append(cur_severity)

    drought_severity = [(threshold - v) / np.mean(AnnualQ_s.iloc[:, b]) for i, v in enumerate(AnnualQ_s.iloc[:, b].rolling(drought_def).mean()) if
                       v < threshold]

    return drought_instances, final_drought_range, total_severity

def count_spatial_droughts(cm_drought_years, gm_drought_years, sj_drought_years, wm_drought_years, ym_drought_years):
    '''
    Insanely naive code that counts the number of years of co-occuring droughts across basins
    :param cm_drought_years:
    :param gm_drought_years:
    :param sj_drought_years:
    :param wm_drought_years:
    :param ym_drought_years:
    :return:
        one_basin: the number of drought years that happen in at least one basin
        two_basin: the number of drought years that happen in at least two basins etc.
    '''

    one_basin = 0
    two_basin = 0
    three_basin = 0
    four_basin = 0
    five_basin = 0

    # TERRIBLY INEFFICIENT CODE BUT WILL WORK

    # Loop through each year, and check how many basins are in drought
    for year in range(1909, 2014):
        # start with upper colorado river
        if cm_drought_years:
            for c in range(len(cm_drought_years)):
                if year in cm_drought_years[c]:
                    one_basin += 1
                    if gm_drought_years:
                        for g in range(len(gm_drought_years)):
                            if year in gm_drought_years[g]:
                                two_basin += 1
                                if sj_drought_years:
                                    for s in range(len(sj_drought_years)):
                                        if year in sj_drought_years[s]:
                                            three_basin += 1
                                            if wm_drought_years:
                                                for w in range(len(wm_drought_years)):
                                                    if year in wm_drought_years[w]:
                                                        four_basin += 1
                                                        if ym_drought_years:
                                                            for y in range(len(ym_drought_years)):
                                                                if year in ym_drought_years[y]:
                                                                    five_basin += 1
                    elif sj_drought_years:
                        for s in range(len(sj_drought_years)):
                            if year in sj_drought_years[s]:
                                two_basin += 1
                                if wm_drought_years:
                                    for w in range(len(wm_drought_years)):
                                        if year in wm_drought_years[w]:
                                            three_basin += 1
                                            if ym_drought_years:
                                                for y in range(len(ym_drought_years)):
                                                    if year in ym_drought_years[y]:
                                                        four_basin += 1

                    elif wm_drought_years:
                        for w in range(len(wm_drought_years)):
                            if year in wm_drought_years[w]:
                                two_basin += 1
                                if ym_drought_years:
                                    for y in range(len(ym_drought_years)):
                                        if year in ym_drought_years[y]:
                                            three_basin += 1

                    elif ym_drought_years:
                        for y in range(len(ym_drought_years)):
                            if year in ym_drought_years[y]:
                                two_basin += 1

        elif gm_drought_years:
            for g in range(len(gm_drought_years)):
                if year in gm_drought_years[g]:
                    one_basin += 1
                    if sj_drought_years:
                        for s in range(len(sj_drought_years)):
                            if year in sj_drought_years[s]:
                                two_basin += 1
                                if wm_drought_years:
                                    for w in range(len(wm_drought_years)):
                                        if year in wm_drought_years[w]:
                                            three_basin += 1
                                            if ym_drought_years:
                                                for y in range(len(ym_drought_years)):
                                                    if year in ym_drought_years[y]:
                                                        four_basin += 1
                    elif wm_drought_years:
                        for w in range(len(wm_drought_years)):
                            if year in wm_drought_years[w]:
                                two_basin += 1
                                if ym_drought_years:
                                    for y in range(len(ym_drought_years)):
                                        if year in ym_drought_years[y]:
                                            three_basin += 1

                    elif ym_drought_years:
                        for y in range(len(ym_drought_years)):
                            if year in ym_drought_years[y]:
                                two_basin += 1

        elif sj_drought_years:
            for s in range(len(sj_drought_years)):
                if year in sj_drought_years[s]:
                    one_basin += 1
                    if wm_drought_years:
                        for w in range(len(wm_drought_years)):
                            if year in wm_drought_years[w]:
                                two_basin += 1
                                if ym_drought_years:
                                    for y in range(len(ym_drought_years)):
                                        if year in ym_drought_years[y]:
                                            three_basin += 1
                    elif ym_drought_years:
                        for y in range(len(ym_drought_years)):
                            if year in ym_drought_years[y]:
                                two_basin += 1
        elif wm_drought_years:
            for w in range(len(wm_drought_years)):
                if year in wm_drought_years[w]:
                    one_basin += 1
                    if ym_drought_years:
                        for y in range(len(ym_drought_years)):
                            if year in ym_drought_years[y]:
                                two_basin += 1

        elif ym_drought_years:
            for y in range(len(ym_drought_years)):
                if year in ym_drought_years[y]:
                    two_basin += 1

    return one_basin, two_basin, three_basin, four_basin, five_basin



def make_plotting_input(hist, type, r):
    if hist==False:
        file_name = '../../Synthetic_records/' + type + '/AnnualQ_s' + str(r) + '.txt'
    else:
        file_name = '../../historical_data/all_basins.csv'
    hist_file_name = '../../historical_data/all_basins.csv'

    num_droughts = np.zeros([5, 5])

    drought_defs = [6, 11, 16, 21, 26]
    for i in range(5):

        cm_instances, cm_drought_years, cm_severity = drought_statistics(file_name, hist_file_name, 0, hist,
                                                                         drought_defs[i])
        gm_instances, gm_drought_years, gm_severity = drought_statistics(file_name, hist_file_name, 1, hist,
                                                                         drought_defs[i])
        ym_instances, ym_drought_years, ym_severity = drought_statistics(file_name, hist_file_name, 2, hist,
                                                                         drought_defs[i])
        wm_instances, wm_drought_years, wm_severity = drought_statistics(file_name, hist_file_name, 3, hist,
                                                                         drought_defs[i])
        sj_instances, sj_drought_years, sj_severity = drought_statistics(file_name, hist_file_name, 4, hist,
                                                                                   drought_defs[i])

        num_droughts[i, :] = count_spatial_droughts(cm_drought_years, gm_drought_years, sj_drought_years,
                                                        wm_drought_years, ym_drought_years)

        return num_droughts

#%% Historical
hist_file_name = 'historical_data/all_basins.csv'
file_name = 'historical_data/all_basins.csv'

hist_droughts = np.zeros([5,5])
hist=True
drought_defs = [6, 11, 16, 21, 26]
for i in range(5):
    cm_instances, cm_drought_years, cm_severity = drought_statistics(file_name, hist_file_name, 0, hist,
                                                                     drought_defs[i])
    gm_instances, gm_drought_years, gm_severity = drought_statistics(file_name, hist_file_name, 1, hist,
                                                                     drought_defs[i])
    ym_instances, ym_drought_years, ym_severity = drought_statistics(file_name, hist_file_name, 2, hist,
                                                                     drought_defs[i])
    wm_instances, wm_drought_years, wm_severity = drought_statistics(file_name, hist_file_name, 3, hist,
                                                                     drought_defs[i])
    sj_instances, sj_drought_years, sj_severity = drought_statistics(file_name, hist_file_name, 4, hist,
                                                                               drought_defs[i])

    hist_droughts[i,:] = count_spatial_droughts(cm_drought_years, gm_drought_years, sj_drought_years,
                                                    wm_drought_years, ym_drought_years)

##################################################
i_20 = []

baseline_realization_severity = np.zeros(1000)
hist_file_name = 'historical_data/all_basins.csv'
num_rel = 1000
num_HMM = 1000
def calc_rel(r, hmm): #simulate across realizations
#for r in range(num_rel):
    num_droughts = np.zeros((5,5))
    total_severity = 0
    file_name = 'Synthetic_records/HMM_1000_r_1000/S_' + str(hmm) + '/AnnualQ_s' + str(r) + '.txt'
    drought_defs = [6, 11, 16, 21, 26]
    for i in range(5):

        cm_instances_hist, cm_drought_years, cm_severity_hist = drought_statistics(file_name, hist_file_name, 0, False, drought_defs[i])    
        gm_instances_hist, gm_drought_years, gm_severity_hist = drought_statistics(file_name, hist_file_name, 1, False, drought_defs[i])
        ym_instances_hist, ym_drought_years, ym_severity_hist = drought_statistics(file_name, hist_file_name, 2, False, drought_defs[i])
        wm_instances_hist, wm_drought_years, wm_severity_hist = drought_statistics(file_name, hist_file_name, 3, False, drought_defs[i])
        sj_instances_hist, sj_drought_years, sj_severity_hist = drought_statistics(file_name, hist_file_name, 4, False, drought_defs[i])
        start_time=time.time()
        num_droughts[i][:] = count_spatial_droughts(cm_drought_years, gm_drought_years, sj_drought_years,
                                                     wm_drought_years, ym_drought_years)

    total_severity += (np.sum(cm_severity_hist) + np.sum(gm_severity_hist) + np.sum(ym_severity_hist) +
                              np.sum(wm_severity_hist)) + np.sum(sj_severity_hist)
    return total_severity, num_droughts

#for hmm in range(num_HMM):
def calc_severity(hmm):
    print(hmm)
    # total_severity = np.zeros(num_rel) 
    with Pool(400) as p:
        result = p.starmap(calc_rel, [(r, hmm) for r in range(1000)])
    result_drought = [i[1].tolist() for i in result]
    result_severity = [i[0] for i in result]
    return result_drought, result_severity

         
num_droughts_20=np.zeros((num_HMM,20))


for hmm in range(num_HMM):#num_HMM
    i_20 = []

    for p in np.arange(0.5,100.5,5).tolist():
        pcen=np.percentile(results[hmm],p,interpolation='nearest')
        # i_200.append(abs(results[hmm]-pcen).argmin())
        sorted_indices = np.argsort(np.abs(results[hmm] - pcen))  # Sort indices by closeness to pcen
        for idx in sorted_indices:
            if idx not in i_20:  # Append if it's not already in i_200
                i_20.append(idx)
                break  # Stop after finding the next closest unique value

    num_droughts_20[hmm][:] = i_20

with open("num_droughts_20_hmm","w") as fp:
    json.dump(num_droughts_20.tolist(), fp)


