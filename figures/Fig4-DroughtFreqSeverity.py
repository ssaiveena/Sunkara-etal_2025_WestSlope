import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import statistics
from random import random
from scipy import stats as ss

#
import os
os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/paper_code/ProcessResults')
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
        AnnualQ_s = pd.read_csv(file_name, sep=' ', header=None)
        AnnualQ_s.columns = ['cm', 'gm', 'ym', 'wm', 'sj']


    AnnualQ_s_hist = pd.read_csv(hist_file, sep=',')
    AnnualQ_s_hist['Year'] = list(range(1909, 2014))
    AnnualQ_s['Year'] = list(range(1909, 2014))


    #std = statistics.stdev(AnnualQ_s.iloc[:, b])
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

#%% Colored CDFs for Baseline ensemble
drought_def = 6 # size of moving window
basin_names = ['Upper Colorado',  'Gunnison', 'Yampa', 'White', 'Southwest']
basins = ['cm', 'gm', 'ym', 'wm', 'sj']
colors = ['tab:grey', 'tab:red', 'tab:cyan', 'tab:green', 'tab:olive']
fig1, axes1 = plt.subplots(1,5, figsize=(12,3))
for b in range(len(basins)):
    # synthetic baseline realizations
    num_droughts = np.zeros(1000)
    severity_curve = []
    max_severity = np.zeros(1000)

    for r in range(0,1000):
        file_name = '../../Synthetic_records/Baseline/AnnualQ_s' + str(r) + '.txt' # edit here
        hist_file_name = '../../historical_data/all_basins.csv'
        drought_instances, drought_years, drought_severity = drought_statistics(file_name, hist_file_name, b, False,
                                                                                drought_def)

        if drought_instances:
            num_droughts[r] = len(drought_years)
            severity_curve.append(drought_severity)
            max_severity[r] = max(drought_severity)
    print('finished drought stats for ' + str(b))
    # Historical (edit file name)
    #file_name = '../../historical_data/all_basins.csv'
    drought_instances_hist, drought_years_hist, drought_severity_hist = drought_statistics(hist_file_name,
                                                                                           hist_file_name, b, True,
                                                                                           drought_def)

    drought_ranks = np.zeros([len(severity_curve), 10])
    for i in range(len(severity_curve)):
        sorted_curve = np.sort(severity_curve[i])[::-1]
        for j in range(len(sorted_curve)):
            drought_ranks[i, j] = sorted_curve[j]


    drought_ranks_hist = np.zeros(10)
    sorted_ranks_hist = np.sort(drought_severity_hist)[::-1]
    for i in range(len(drought_severity_hist)):
            drought_ranks_hist[i] = sorted_ranks_hist[i]


    max_ranks = np.max(drought_ranks, axis=0)
    min_ranks = np.min(drought_ranks, axis=0)

    # pad ranks with zeros for realizations without droughts
    no_drought_traces = 999-len(severity_curve)
    for nr in range(no_drought_traces):
        drought_ranks = np.vstack((drought_ranks, np.zeros(10)))
    print(len(drought_ranks))

    print('getting percentiles and plotting')
    ps = np.arange(0, 1.01, 0.01) * 100
    for j in range(1, len(ps)):
        u = np.percentile(drought_ranks, ps[j], axis=0)
        axes1.flatten()[b].plot(u, np.arange(0,1, .1), color=cm.viridis(ps[j - 1] / 100.0))
        #l = np.percentile(drought_ranks, ps[j - 1], axis=0)
        #axes1.flatten()[b].fill_between(np.arange(0, 1.25, .25), l, u, color=cm.YlGnBu_r(ps[j - 1] / 100.0), alpha=0.75,
                        #edgecolor='none')

    print('plotting hist')
    #axes1.flatten()[b].plot( np.arange(0, 1.25, .25), max_ranks, linestyle='--', color='k', alpha=.5)
    for i in range(7):
        axes1.flatten()[b].plot(drought_ranks_hist, np.arange(0, 1, .1), color='k', zorder=3)
        if drought_ranks_hist[i] > 0:
            axes1.flatten()[b].scatter( drought_ranks_hist[i], np.arange(0, 1, .1)[i], color='k', s=50, zorder=3)
    axes1.flatten()[b].set_ylim([0, .7])
    axes1.flatten()[b].set_yticklabels([0,10,20,30,40], fontsize=12)
    axes1.flatten()[b].set_yticks(np.arange(0, .8, .1))
    axes1.flatten()[b].set_yticklabels([0, 1, 2, 3, 4, 5, 6, 7], fontsize=12)
    axes1.flatten()[b].set_xlim([0, 20])
    axes1.flatten()[b].set_title(basin_names[b], fontsize=16)
    axes1.flatten()[b].set_xlabel('DM', fontsize=14)
    if b ==0:
        axes1.flatten()[b].set_ylabel('# of Droughts Exceeding\n in 105-year Record', fontsize=14)
plt.tight_layout()
#axes1.flatten()[5].axis('off')
plt.show()
#plt.savefig('../../Figures/InitialSubmissionFigures/SeverityCurves_5years_vertical.pdf')

#%% Colored CDFs for Climate ensemble
drought_def = 6 # size of moving window
basin_names = ['Upper Colorado',  'Gunnison', 'Yampa', 'White', 'Southwest']
basins = ['cm', 'gm', 'ym', 'wm', 'sj']
colors = ['tab:grey', 'tab:red', 'tab:cyan', 'tab:green', 'tab:olive']
fig1, axes1 = plt.subplots(1,5, figsize=(12,3))
for b in range(len(basins)):
    # synthetic climate realizations
    num_droughts = np.zeros(1000)
    severity_curve = []
    max_severity = np.zeros(1000)

    for r in range(0,1000):
        file_name = '../../Synthetic_records/ClimateAdjusted_zero_zero_five/AnnualQ_s' + str(r) + '.txt' # edit here
        hist_file_name = '../../historical_data/all_basins.csv'
        drought_instances, drought_years, drought_severity = drought_statistics(file_name, hist_file_name, b, False,
                                                                                drought_def)

        if drought_instances:
            num_droughts[r] = len(drought_years)
            severity_curve.append(drought_severity)
            max_severity[r] = max(drought_severity)
    print('finished drought stats for ' + str(b))
    # Historical (edit file name)
    #file_name = '../../historical_data/all_basins.csv'
    drought_instances_hist, drought_years_hist, drought_severity_hist = drought_statistics(hist_file_name,
                                                                                           hist_file_name, b, True,
                                                                                           drought_def)

    drought_ranks = np.zeros([len(severity_curve), 10])
    for i in range(len(severity_curve)):
        sorted_curve = np.sort(severity_curve[i])[::-1]
        for j in range(len(sorted_curve)):
            drought_ranks[i, j] = sorted_curve[j]


    drought_ranks_hist = np.zeros(10)
    sorted_ranks_hist = np.sort(drought_severity_hist)[::-1]
    for i in range(len(drought_severity_hist)):
            drought_ranks_hist[i] = sorted_ranks_hist[i]


    max_ranks = np.max(drought_ranks, axis=0)
    min_ranks = np.min(drought_ranks, axis=0)

    # pad ranks with zeros for realizations without droughts
    no_drought_traces = 999-len(severity_curve)
    for nr in range(no_drought_traces):
        drought_ranks = np.vstack((drought_ranks, np.zeros(10)))
    print(len(drought_ranks))

    print('getting percentiles and plotting')
    ps = np.arange(0, 1.01, 0.01) * 100
    for j in range(1, len(ps)):
        u = np.percentile(drought_ranks, ps[j], axis=0)
        axes1.flatten()[b].plot(u, np.arange(0,1, .1), color=cm.plasma(ps[j - 1] / 100.0))
        #l = np.percentile(drought_ranks, ps[j - 1], axis=0)
        #axes1.flatten()[b].fill_between(np.arange(0, 1.25, .25), l, u, color=cm.YlGnBu_r(ps[j - 1] / 100.0), alpha=0.75,
                        #edgecolor='none')

    print('plotting hist')
    #axes1.flatten()[b].plot( np.arange(0, 1.25, .25), max_ranks, linestyle='--', color='k', alpha=.5)
    for i in range(7):
        axes1.flatten()[b].plot(drought_ranks_hist, np.arange(0, 1, .1), color='k', zorder=3)
        if drought_ranks_hist[i] > 0:
            axes1.flatten()[b].scatter( drought_ranks_hist[i], np.arange(0, 1, .1)[i], color='k', s=50, zorder=3)
    axes1.flatten()[b].set_ylim([0, .7])
    #axes1.flatten()[b].set_yticklabels([0,10,20,30,40], fontsize=12)
    axes1.flatten()[b].set_yticks(np.arange(0, .8, .1))
    axes1.flatten()[b].set_yticklabels([0, 1, 2, 3, 4, 5, 6, 7], fontsize=12)
    axes1.flatten()[b].set_xlim([0, 50])
    axes1.flatten()[b].set_title(basin_names[b], fontsize=16, color='w')
    axes1.flatten()[b].set_xlabel('DM', fontsize=14)
    if b ==0:
        axes1.flatten()[b].set_ylabel('# of Droughts Exceeding\n in 105-year Record', fontsize=14)
plt.tight_layout()

plt.savefig('../../Figures/InitialSubmissionFigures/AdjustedClimate/SeverityCurves_5years_vertical_AdjustedClimate.pdf')

#%%PLOT historical droughts
drought_def = 6
AnnualQ_s=pd.read_csv('../../historical_data/all_basins.csv', sep = ',')
#AnnualQ_s.columns = ['cm', 'gm', 'ym', 'wm', 'sj']
AnnualQ_s['Year'] = list(range(1909,2014))

basin_names = ['Upper Colorado',  'Gunnison', 'Yampa', 'White', 'San Juan  / Dolores']
for b in range(1):
    std = statistics.stdev(AnnualQ_s.iloc[:,b])
    threshold = np.mean(AnnualQ_s.iloc[:,b] - (0.5*std))

    drought_instances = [i for i, v in enumerate(AnnualQ_s.iloc[:,b].rolling(drought_def).mean()) if v < threshold]
    drought_years = AnnualQ_s.iloc[:, 5].rolling(drought_def).mean()[drought_instances]

    #drought_severity = [(threshold - v)/threshold for i, v in enumerate(AnnualQ_s.iloc[:,b].rolling(11).mean()) if v < threshold]

    #fig, ax = plt.subplots()
    #ax.plot(sorted(drought_severity)[::-1], np.arange(0,len(drought_severity)))
    #plt.show()


    # Add labels and title
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(AnnualQ_s.iloc[:,5],
            AnnualQ_s.iloc[:,b],
            color='#005F73',
            label='Annual Flow')

    #ax.plot(AnnualQ_s.iloc[:,5].rolling(drought_def,center=True).mean(),
    #        AnnualQ_s.iloc[:,b].rolling(drought_def,center=True).mean(),
    #        color='#183A2E',
    #        label= str(drought_def) + '-Year Rolling Mean')

    ax.axhline(y=AnnualQ_s.iloc[:,b].mean(),
               color='black',
               linestyle='--',
               label='Historical Mean')


    # Visualize the drought periods as yellow rectangles
    for i in drought_years:
     #   # Plot a box centered around those values and with 5 years on either side.
        rect = patches.Rectangle((i-drought_def/2,0), drought_def,2e7, linewidth=1, edgecolor='#EFE2BE', facecolor='#EFE2BE')

        # Add the patch to the Axes
        ax.add_patch(rect)
    # fix here
    ax.fill_between(np.arange(1958,1970), np.ones(12)*np.mean(AnnualQ_s.iloc[:,b]), AnnualQ_s.iloc[49:61,b], color='indianred')
    ax.fill_between(np.arange(1999,2011), np.ones(12)*np.mean(AnnualQ_s.iloc[:,b]), AnnualQ_s.iloc[90:102,b], color='indianred')


    ax.set_ylim([0.2*10**7, 1.2*10**7])
    plt.title(basin_names[b] + " Annual Flow")
    ax.set_xlabel("Year", fontsize=16)
    ax.set_ylabel("Annual Flow (cubic feet per year)", fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    mpl.rc('legend', fontsize=16)
    legend = plt.legend(loc='upper left')
    #plt.savefig('statemodify_XBM_IWR/Figures/HistoricalTS/Decadal/' + basin_names[b] + '_historicalTS_' + str(drought_def) + '.png')
    plt.savefig('../../Figures/InitialSubmissionFigures/SeverityCurves_5years_vertical_climate.pdf')

    plt.show()