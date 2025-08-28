import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from tqdm import tqdm
import os
os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/paper_code/final_data_analysis')
#%%
def calc_plot_percentile_shortage(record_type, percentile, ax, legend, hist):
    print('../../Results/Shortage/cu/updated_cm_' + record_type + '_no_export.csv')
    # read data
    cm_data = np.loadtxt('figureData/Shortage/cu/updated_cm_' + record_type + '_no_export.csv', delimiter=',') * 1233.48
    gm_data = np.loadtxt('figureData/Shortage/cu/updated_gm_' + record_type + '_no_export.csv', delimiter=',') * 1233.48
    ym_data = np.loadtxt('figureData/Shortage/cu/updated_ym_' + record_type + '_no_export.csv', delimiter=',') * 1233.48
    wm_data = np.loadtxt('figureData/Shortage/cu/updated_wm_' + record_type + '_no_export.csv', delimiter=',') * 1233.48
    sj_data = np.loadtxt('figureData/Shortage/cu/updated_sj_' + record_type + '_no_export.csv', delimiter=',') * 1233.48

    # get percentile of interest across all realizations
    cm_percentiles = np.zeros([1000])
    gm_percentiles = np.zeros([1000])
    ym_percentiles = np.zeros([1000])
    wm_percentiles = np.zeros([1000])
    sj_percentiles = np.zeros([len(sj_data[0,:])])

    for r in range(1000):
        cm_percentiles[r] = np.percentile(cm_data[:, r], percentile)
        gm_percentiles[r] = np.percentile(gm_data[:, r], percentile)
        ym_percentiles[r] = np.percentile(ym_data[:, r], percentile)
        wm_percentiles[r] = np.percentile(wm_data[:, r], percentile)

    for r in range(len(sj_data[0,:])):
        sj_percentiles[r] = np.percentile(sj_data[:, r], percentile)

    # now calculate the percentiles across the 1000 realizations to make plot
    cm_realizations = np.zeros(100)
    gm_realizations = np.zeros(100)
    ym_realizations = np.zeros(100)
    wm_realizations = np.zeros(100)
    sj_realizations = np.zeros(100)

    for p in range(1, 101):
        cm_realizations[p - 1] = np.percentile(cm_percentiles, p)
        gm_realizations[p - 1] = np.percentile(gm_percentiles, p)
        ym_realizations[p - 1] = np.percentile(ym_percentiles, p)
        wm_realizations[p - 1] = np.percentile(wm_percentiles, p)
        sj_realizations[p - 1] = np.percentile(sj_percentiles, p)

    # sum all and sort
    total = cm_realizations + gm_realizations + ym_realizations + wm_realizations + sj_realizations


    # create plot input
    base = sj_realizations/1000000
    second = base + wm_realizations/1000000
    third = second + ym_realizations/1000000
    fourth = third + gm_realizations/1000000
    fifth = fourth + cm_realizations/1000000

    print(max(fifth))

    ax.fill_between(np.arange(len(base)), np.zeros(100), base, alpha=.85, color='#335c67',edgecolor='none')
    ax.fill_between(np.arange(len(base)), base, second, alpha=.85, color='#fff3b0',edgecolor='none')
    ax.fill_between(np.arange(len(base)), second, third, alpha=.85, color='#e09f3e',edgecolor='none')
    ax.fill_between(np.arange(len(base)), third, fourth, alpha=.85, color='#9e2a2b',edgecolor='none')
    ax.fill_between(np.arange(len(base)), fourth, fifth, alpha=.85, color='#540b0e',edgecolor='none')


    ax.plot(np.arange(len(base)), np.ones(len(base))*hist, linestyle='--', color='lightblue')
    ax.set_ylabel('Annual Consumptive Use Shortage (Million $m^3$)')
    ax.set_xlabel('Realization Percentile')
    ax.set_ylim([0, 1000])
    ax.set_xlim(0,100)
    if record_type == 'base':
        ax.set_title('Baseline Ensemble\n'+str(percentile) + 'th percentile ')
    else:
        ax.set_title('Climate-Adjusted Ensemble\n' + str(percentile) + 'th percentile ')
    if legend:
        ax.legend(['Southwest', 'White', 'Yampa', 'Gunnison', 'Upper Colorado'])

#%%
fig, axes = plt.subplots(2,3, figsize=(12, 8))
calc_plot_percentile_shortage('base', 50, axes.flatten()[0], False, 116*1.233)
calc_plot_percentile_shortage('base', 90, axes.flatten()[1], False, 252.5*1.233)
calc_plot_percentile_shortage('base', 99, axes.flatten()[2], False, 457.8*1.233)
calc_plot_percentile_shortage('AdjustedClimate', 50, axes.flatten()[3], False,116.0*1.233)
calc_plot_percentile_shortage('AdjustedClimate', 90, axes.flatten()[4], False,252.5*1.233)
calc_plot_percentile_shortage('AdjustedClimate', 99, axes.flatten()[5], False, 457.8*1.233)

plt.tight_layout()
plt.show()
#plt.savefig('../../Figures/InitialSubmissionFigures/AdjustedClimate/Seminar/Shortage.png')
