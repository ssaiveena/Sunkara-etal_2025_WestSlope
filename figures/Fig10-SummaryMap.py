import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from tqdm import tqdm
import os
#os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/paper_code/FigureGeneration')

#%%
def moving_average(a, n=11) :
    '''
    Calculates the moving average over n periods

    :param a:           numpy array, sequence to take the moving average over
    :param n:           float, the number of years used in the moving average
    :return:            the moving average of a over n periods
    '''

    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

#%%

def shortage_diff_plot(abbrev):

    # start by comparing baseline to climate (will need to include historical for final)
    # 12.3348 conversion is to convert acre feet to million m^3
    if abbrev == 'cm':
        base = np.loadtxt('Results/Shortage/cu/cm_base_no_export', delimiter=',') * 12.3348
        climate = np.loadtxt('Results/Shortage/cu/updated_cm_AdjustedClimate_no_export.csv', delimiter=',')* 12.3348
        hist = np.loadtxt('Results/Shortage/cu/cm_hist.csv', delimiter=',')* 12.3348
    elif abbrev == 'gm':
        base = np.loadtxt('Results/Shortage/cu/gm_base.csv', delimiter=',')* 12.3348
        climate = np.loadtxt('Results/Shortage/cu/updated_gm_AdjustedClimate_no_export.csv', delimiter=',')* 12.3348
        hist = np.loadtxt('Results/Shortage/cu/gm_hist.csv', delimiter=',')* 12.3348
    elif abbrev == 'sj':
        base = np.loadtxt('Results/Shortage/cu/sj_base_no_export.csv', delimiter=',')* 12.3348
        climate = np.loadtxt('Results/Shortage/cu/updated_sj_AdjustedClimate_no_export.csv', delimiter=',')* 12.3348
        hist = np.loadtxt('Results/Shortage/cu/sj_hist.csv', delimiter=',')* 12.3348
    else:
        base = np.zeros(100)
        climate = np.zeros(100)
        hist = np.zeros(100)
        print('Error, must specify cm, gm or sj as basin')

    # calculate the medians of both ensembles
    base_median = np.mean(np.percentile(base, 50, axis=0))
    climate_median = np.mean(np.percentile(climate, 50, axis=0))
    hist_median = np.percentile(hist, 50)

    # calculate the 90th percentile of the baseline ensemble
    base_90 = np.mean(np.percentile(base, 90, axis=0))
    climate_90 = np.mean(np.percentile(climate, 90, axis=0))
    hist_90 = np.percentile(hist, 90)


    # calculate the 99th perecentile of the baseline ensemble
    base_99 = np.mean(np.percentile(base, 99, axis=0))
    climate_99 = np.mean(np.percentile(climate, 99, axis=0))
    hist_99 = np.percentile(hist, 99)


    # plot the 50th, 90th and 99th percentiles
    fig = plt.figure()
    ax = fig.gca()

    # plot between hist and each ensemble
    ax.plot([hist_median, base_median], [5,5], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([hist_median, climate_median], [7, 7], color='darkgrey',linewidth=3, zorder=-3)
    ax.plot([hist_90, base_90], [15, 15], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([hist_90, climate_90], [17, 17], color='darkgrey',linewidth=3, zorder=-3)
    ax.plot([hist_99, base_99], [25, 25], color='darkgrey',linewidth=3, zorder=-3)
    ax.plot([hist_99, climate_99], [27, 27], color='darkgrey', linewidth=3, zorder=-3)

    ax.scatter([hist_median, hist_90, hist_99], [5,15,25], s=150, color='w', edgecolor='k')
    ax.scatter([hist_median, hist_90, hist_99], [7, 17, 27], s=150, color='w', edgecolor='k')
    ax.scatter([base_median, base_90, base_99],[5,15,25], s=150, color='cornflowerblue')
    ax.scatter([climate_median, climate_90, climate_99], [7, 17, 27], s=150, color='indianred')
    ax.set_ylim([0,30])
    ax.set_yticks([6, 16,26])
    plt.savefig('Figures/'+ abbrev + '_shortage.pdf')

#%%
shortage_diff_plot('cm')
shortage_diff_plot('gm')
shortage_diff_plot('sj')
#%%
def deliveries_diff_plot():
    # start by comparing baseline to climate (will need to include historical for final)
    # 12.3348 conversion is to convert acre feet to million m^3

    cm_hist = np.loadtxt('Results/cm/baseline/cm_hist_outflow.csv', delimiter=',') *12.3348
    gm_hist = np.loadtxt('Results/gm/baseline/gm_hist_outflow.csv', delimiter=',')*12.3348
    ym_hist = np.loadtxt('Results/ym/baseline/ym_hist_outflow.csv', delimiter=',')*12.3348
    wm_hist = np.loadtxt('Results/wm/baseline/wm_hist_outflow.csv', delimiter=',')*12.3348
    sj_hist = np.loadtxt('Results/sj/baseline/sj_hist_outflow.csv', delimiter=',')*12.3348

    total_hist = cm_hist + gm_hist + ym_hist + wm_hist + sj_hist

    cm_baseline = np.loadtxt('Results/cm/baseline/cm_baseline_outflow.csv', delimiter=',') *12.3348
    gm_baseline = np.loadtxt('Results/gm/baseline/gm_baseline_outflow_filled.csv', delimiter=',')*12.3348
    ym_baseline = np.loadtxt('Results/ym/baseline/ym_baseline_outflow_filled.csv', delimiter=',')*12.3348
    wm_baseline = np.loadtxt('Results/wm/baseline/wm_baseline_outflow_filled.csv', delimiter=',')*12.3348
    sj_baseline = np.loadtxt('Results/sj/baseline/sj_baseline_outflow.csv', delimiter=',')*12.3348

    # read in the climate data

    cm_climate = np.loadtxt('Results/cm/AdjustedClimate/cm_AdjustedClimate_outflow.csv', delimiter=',')*12.3348
    gm_climate = np.loadtxt('Results/gm/AdjustedClimate/gm_AdjustedClimate_outflow.csv', delimiter=',')*12.3348
    ym_climate = np.loadtxt('Results/ym/AdjustedClimate/ym_AdjustedClimate_outflow.csv', delimiter=',')*12.3348
    wm_climate = np.loadtxt('Results/wm/AdjustedClimate/wm_AdjustedClimate_outflow.csv', delimiter=',')*12.3348
    sj_climate = np.loadtxt('Results/sj/AdjustedClimate/sj_AdjustedClimate_outflow.csv', delimiter=',')*12.3348

    total_baseline = np.zeros((105, 1000))
    total_climate = np.zeros((105, 1000))

    # sum the total outflow to powell for each record in the baseline and climate adjusted ensembles
    for i in range(1000):
        total_baseline[:,i] = cm_baseline[:,i] + gm_baseline[:,i] + ym_baseline[:,i] + wm_baseline[:,i] + sj_baseline[:,i]
        total_climate[:, i] = cm_climate[:, i] + gm_climate[:, i] + ym_climate[:, i] + wm_climate[:,
                                                                                           i] + sj_climate[:, i]
    baseline_mov_ave = np.zeros((95,1000))
    climate_mov_ave = np.zeros((95,1000))
    for i in range(1000):
        baseline_mov_ave[:,i] = moving_average(total_baseline[:,i])
        climate_mov_ave[:,i] = moving_average(total_climate[:,i])

    hist_moving_ave = moving_average(total_hist)


    # calculate the medians of both ensembles
    base_median = np.mean(np.percentile(baseline_mov_ave, 50, axis=0))
    climate_median = np.mean(np.percentile(climate_mov_ave, 50, axis=0))
    hist_median = np.percentile(hist_moving_ave, 50)

    # calculate the 90th percentile of the baseline ensemble
    base_90 = np.mean(np.percentile(baseline_mov_ave, 10, axis=0))
    climate_90 = np.mean(np.percentile(climate_mov_ave, 10, axis=0))
    hist_90 = np.percentile(hist_moving_ave, 10)

    # calculate the 1st perecentile of the baseline ensemble
    base_99 = np.mean(np.percentile(baseline_mov_ave, 1, axis=0))
    climate_99 = np.mean(np.percentile(climate_mov_ave, 1, axis=0))
    hist_99 = np.percentile(hist_moving_ave, 1)

    # plot the 50th, 90th and 99th percentiles
    fig = plt.figure(figsize=(4.8,6.4))
    ax = fig.gca()

    marker_size=200
    # plot between hist and each ensemble
    ax.plot([25, 25], [hist_median, base_median], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([27, 27], [hist_median, climate_median], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([15, 15], [hist_90, base_90], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([17, 17], [hist_90, climate_90], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([5, 5], [hist_99, base_99], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([7, 7], [hist_99, climate_99], color='darkgrey', linewidth=3, zorder=-3)

    ax.scatter([25, 15, 5], [hist_median, hist_90, hist_99], s=marker_size, color='w', edgecolor='k', marker='s')
    ax.scatter([27, 17, 7], [hist_median, hist_90, hist_99], s=marker_size, color='w', edgecolor='k', marker='s')
    ax.scatter([25, 15, 5], [base_median, base_90, base_99], s=marker_size, color='cornflowerblue', marker='s')
    ax.scatter([27, 17, 7], [climate_median, climate_90, climate_99], s=150, color='indianred', marker='s')
    ax.set_xlim([0, 30])
    ax.set_xticks([6, 16, 26])
    #plt.show()
    plt.savefig('Figures/total_deliveries.pdf')

#%%
deliveries_diff_plot()

#%% Reservoir Storage

def res_diff_plot(res_abbrev, min_max):
    baseline_rels = np.loadtxt('Results/reservoir/' + res_abbrev + '_realizationPercentiles_baseline_run_1_to_99.csv',
                               delimiter=',') *12.2248

    climate_rels = np.loadtxt('Results/reservoir/' + res_abbrev + '_realizationPercentiles_AdjustedClimate_05_1_to_99.csv',
                              delimiter=',') *12.3348

    hist = np.loadtxt('Results/reservoir/' + res_abbrev + '_realizationPercentiles_hist_1_to_99.csv') *12.33

    # plot the 50th, 90th and 99th percentiles
    fig = plt.figure(figsize=(4.8,6.4))
    ax = fig.gca()

    marker_size = 300
    # plot between hist and each ensemble
    ax.plot([25, 25], [hist[50], np.mean(baseline_rels[50,:])], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([27, 27], [hist[50], np.mean(climate_rels[50,:])], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([15, 15], [hist[11], np.mean(baseline_rels[11,:])], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([17, 17], [hist[11], np.mean(climate_rels[11,:])], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([5, 5], [hist[1], np.mean(baseline_rels[1,:])], color='darkgrey', linewidth=3, zorder=-3)
    ax.plot([7, 7], [hist[1], np.mean(climate_rels[1,:])], color='darkgrey', linewidth=3, zorder=-3)

    ax.scatter([25, 15, 5], [hist[50], hist[11], hist[1]], s=marker_size, color='w', edgecolor='k', marker= 'v')
    ax.scatter([27, 17, 7], [hist[50], hist[11], hist[1]], s=marker_size, color='w', edgecolor='k', marker= 'v')
    ax.scatter([25, 15, 5], [np.mean(baseline_rels[50,:]), np.mean(baseline_rels[11,:]), np.mean(baseline_rels[1,:])],
               s=marker_size, color='cornflowerblue', marker= 'v')
    ax.scatter([27, 17, 7], [np.mean(climate_rels[50,:]), np.mean(climate_rels[11,:]), np.mean(climate_rels[1,:])],
               s=marker_size, color='indianred', marker= 'v')
    ax.set_xlim([0, 30])
    ax.set_xticks([6, 16, 26])
    ax.set_ylim(min_max)
    #plt.show()
    plt.savefig('Figures/' + res_abbrev + 'storage_diff.pdf')
#%%
res_diff_plot('LG', [0, 6000000])
res_diff_plot('BM', [0, 9000000])
res_diff_plot('MR', [0, 4000000])

#%% Environmental Flow Diff
record_type = 'baseline'
# first, extract shortage at the 15 mile reach
baseline_shortage = np.zeros([105,1000])

for r in tqdm(range(1000)):
    pq_file = pd.read_parquet('../../Results/cm/' + record_type + '/parquet/cm2015B_S' + str(r) + '_1.parquet',
                engine='pyarrow')

    fifteen_mile = pq_file[pq_file['structure_id']=='7202003']

    fifteen_mile = fifteen_mile[fifteen_mile['month']=='TOT']

    baseline_shortage[:,r] = fifteen_mile['shortage_total'].astype('float')

#%%
record_type = 'climate'
# first, extract shortage at the 15 mile reach
climate_shortage = np.zeros([105,1000])

for r in tqdm(range(1000)):
    pq_file = pd.read_parquet('../../Results/cm/' + record_type + '/parquet/cm2015B_S' + str(r) + '_1.parquet',
                engine='pyarrow')

    fifteen_mile = pq_file[pq_file['structure_id']=='7202003']

    fifteen_mile = fifteen_mile[fifteen_mile['month']=='TOT']

    climate_shortage[:,r] = fifteen_mile['shortage_total'].astype('float')

#%% Historical
record_type = 'historical'
pq_file_hist = pd.read_parquet('../../Results/cm/' + record_type + '/parquet/cm2015B.parquet',
                engine='pyarrow')

fifteen_mile_hist = pq_file_hist[pq_file_hist['structure_id']=='7202003']

fifteen_mile_hist = fifteen_mile_hist[fifteen_mile_hist['month']=='TOT']
hist_shortage = fifteen_mile_hist['shortage_total'].astype('float')
#%%
# calculate the medians of both ensembles
base_env_median = np.mean(np.percentile(baseline_shortage, 50, axis=0)) *12.3348
climate_env_median = np.mean(np.percentile(climate_shortage, 50, axis=0))*12.3348
hist_env_median = np.percentile(hist_shortage, 50)*12.3348

# calculate the 90th percentile of the baseline ensemble
base_env_90 = np.mean(np.percentile(baseline_shortage, 90, axis=0))*12.3348
climate_env_90 = np.mean(np.percentile(climate_shortage, 90, axis=0))*12.3348
hist_env_90 = np.percentile(hist_shortage, 90)*12.3348


# calculate the 99th perecentile of the baseline ensemble
base_env_99 = np.mean(np.percentile(baseline_shortage, 99, axis=0))*12.3348
climate_env_99 = np.mean(np.percentile(climate_shortage, 99, axis=0))*12.3348
hist_env_99 = np.percentile(hist_shortage, 99)*12.3348

#%%
# plot the 50th, 90th and 99th percentiles
fig = plt.figure()
ax = fig.gca()
marker_size = 300
# plot between hist and each ensemble
ax.plot([hist_env_median, base_env_median], [5,5], color='darkgrey', linewidth=3, zorder=-3)
ax.plot([hist_env_median, climate_env_median], [7, 7], color='darkgrey',linewidth=3, zorder=-3)
ax.plot([hist_env_90, base_env_90], [15, 15], color='darkgrey', linewidth=3, zorder=-3)
ax.plot([hist_env_90, climate_env_90], [17, 17], color='darkgrey',linewidth=3, zorder=-3)
ax.plot([hist_env_99, base_env_99], [25, 25], color='darkgrey',linewidth=3, zorder=-3)
ax.plot([hist_env_99, climate_env_99], [27, 27], color='darkgrey', linewidth=3, zorder=-3)

ax.scatter([hist_env_median, hist_env_90, hist_env_99], [5,15,25], s=marker_size, color='w', edgecolor='k', marker = 'p')
ax.scatter([hist_env_median, hist_env_90, hist_env_99], [7, 17, 27], s=marker_size, color='w', edgecolor='k', marker = 'p')
ax.scatter([base_env_median, base_env_90, base_env_99],[5,15,25], s=marker_size, color='cornflowerblue', marker = 'p')
ax.scatter([climate_env_median, climate_env_90, climate_env_99], [7, 17, 27], s=marker_size, color='indianred', marker = 'p')
ax.set_ylim([0,30])
ax.set_yticks([6, 16,26])
plt.savefig('../../Figures/InitialSubmissionFigures/map_figures/ENV_diff.pdf')