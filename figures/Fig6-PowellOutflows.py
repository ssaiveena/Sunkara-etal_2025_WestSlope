import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os

def moving_average(a, n=3) :
    '''
    Calculates the moving average over n periods

    :param a:           numpy array, sequence to take the moving average over
    :param n:           float, the number of years used in the moving average
    :return:            the moving average of a over n periods
    '''

    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def calculate_moving_ave_percentile(ensemble, duration, p, hist, length):
    '''
    calculates the pth percentile of a moving average of a given duration

    :param ensemble:                    numpy array, the time-series being evaluated
    :param duration:                    float, the period used to take the moving average
    :param p:                           int, the percentile of interest
    :param hist:                        bool, indicates whether the ensemble is the historical record
    :param length:                      int, the length of the array being processed
    :return:                            the pth percentile of the moving average of the ensemble
    '''

    moving_av = np.zeros([105-duration+1, length])
    if not hist:
        for i in range(length):
            moving_av[:, i] = moving_average(ensemble[:,i], duration)
        percentile_mov = np.percentile(moving_av, p, axis=0)
    else:
        moving_av = moving_average(ensemble, duration)
        percentile_mov = np.percentile(moving_av, p)

    return percentile_mov


# read in historical data
cm_hist = np.loadtxt('figureData/cm/baseline/cm_hist_outflow.csv', delimiter=',')
gm_hist = np.loadtxt('figureData/gm/baseline/gm_hist_outflow.csv', delimiter=',')
ym_hist = np.loadtxt('figureData/ym/baseline/ym_hist_outflow.csv', delimiter=',')
wm_hist = np.loadtxt('figureData/wm/baseline/wm_hist_outflow.csv', delimiter=',')
sj_hist = np.loadtxt('figureData/sj/baseline/sj_hist_outflow.csv', delimiter=',')

total_hist = cm_hist + gm_hist + ym_hist + wm_hist + sj_hist

# read in baseline data
cm_baseline = np.loadtxt('figureData/cm/baseline/cm_baseline_outflow.csv', delimiter=',')
gm_baseline = np.loadtxt('figureData/gm/baseline/gm_baseline_outflow_filled.csv', delimiter=',')
ym_baseline = np.loadtxt('figureData/ym/baseline/ym_baseline_outflow_filled.csv', delimiter=',')
wm_baseline = np.loadtxt('figureData/wm/baseline/wm_baseline_outflow_filled.csv', delimiter=',')
sj_baseline = np.loadtxt('figureData/sj/baseline/sj_baseline_outflow.csv', delimiter=',')

total_baseline = cm_baseline.flatten() + gm_baseline.flatten() + ym_baseline.flatten() + wm_baseline.flatten() +\
                 sj_baseline.flatten()

# read in the climate data
cm_climate = np.loadtxt('figureData/cm/AdjustedClimate/cm_AdjustedClimate_outflow.csv', delimiter=',')
gm_climate = np.loadtxt('figureData/gm/AdjustedClimate/gm_AdjustedClimate_outflow.csv', delimiter=',')
ym_climate = np.loadtxt('figureData/ym/AdjustedClimate/ym_AdjustedClimate_outflow.csv', delimiter=',')
wm_climate = np.loadtxt('figureData/wm/AdjustedClimate/wm_AdjustedClimate_outflow.csv', delimiter=',')
sj_climate = np.loadtxt('figureData/sj/AdjustedClimate/sj_AdjustedClimate_outflow.csv', delimiter=',')

# A small number of Southwest realizations crashed due to Statemod problems, remove them from the ensemble
sj_error = [13, 17, 74, 110, 111, 116, 145, 162, 203, 208, 224, 225, 267, 288, 346, 459, 483, 492, 563, 588, 664, 713,
            727, 843, 845, 917, 974]

cm_mod_climate = np.delete(cm_climate, sj_error, axis=1)
gm_mod_climate = np.delete(gm_climate, sj_error, axis=1)
ym_mod_climate = np.delete(ym_climate, sj_error, axis=1)
wm_mod_climate = np.delete(wm_climate, sj_error, axis=1)
sj_mod_climate = np.delete(sj_climate, sj_error, axis=1)
#%%
# TEMPORARY: Not all runs were processed, leaving ~96 blank columns, remove them here

#cm_mod_climate = cm_mod_climate[:,0:878]
#gm_mod_climate = gm_mod_climate[:,0:878]
#ym_mod_climate = ym_mod_climate[:,0:878]
#wm_mod_climate = wm_mod_climate[:,0:878]
#sj_mod_climate = sj_mod_climate[:,0:878]


#%%
total_climate = cm_mod_climate.flatten() + gm_mod_climate.flatten() + ym_mod_climate.flatten() + wm_mod_climate.flatten() +\
                 sj_mod_climate.flatten()

# reshape to annual
baseline_annual = np.reshape(total_baseline, [105,1000])
climate_annual = np.reshape(total_climate, [105,973])

#%% calculate 1st percentile flows
baseline_percentiles = np.zeros([31, 973])
climate_percentiles = np.zeros([31, 973])
hist_percentiles = np.zeros(31)

for i in range(1,32):
    baseline_percentiles[i-1,:] = calculate_moving_ave_percentile(baseline_annual, i, 1, False, 973)
    climate_percentiles[i-1,:] = calculate_moving_ave_percentile(climate_annual, i, 1, False, 973)
    hist_percentiles[i-1] = calculate_moving_ave_percentile(total_hist, i, 1, True, 1000)

# Calculate the maximum and minimums across the moving averages
max_baseline = np.max(baseline_percentiles, axis=1)
min_baseline = np.min(baseline_percentiles, axis=1)

max_climate = np.max(climate_percentiles, axis=1)
min_climate = np.min(climate_percentiles, axis=1)

# Create boxplots
# 1. make a flat array of all percentile data
transposed_baseline_percentiles = np.transpose(baseline_percentiles)*1233.48/1000000
transposed_climate_percentiles = np.transpose(climate_percentiles)*1233.48/1000000

both_ensembles = np.zeros([7, 1946])

for i, dur in enumerate([0, 5, 10, 15, 20, 25, 30]):
    both_ensembles[i,:] = np.hstack([transposed_baseline_percentiles[:,dur], transposed_climate_percentiles[:,dur]])

both_ensembles_flat = both_ensembles.flatten()

# 2. create an array of strings for noting which is which
climate_name = ['climate'] * 973
baseline_name = ['baseline'] * 973
both_names = np.hstack([baseline_name, climate_name, baseline_name, climate_name, baseline_name, climate_name,
                        baseline_name, climate_name, baseline_name, climate_name, baseline_name, climate_name,
                        baseline_name, climate_name])

# make an initial data frame with one column containing the flows
both_df = pd.DataFrame(both_ensembles_flat, columns=['Mean Flow (maf)'])

# 3. make a new array that specifies the rolling average of each flow
one_year = np.ones(1946)
five_years = np.ones(1946)*5
ten_years = np.ones(1946)*10
fifteen_years = np.ones(1946)*15
twenty_years = np.ones(1946)*20
twentyfive_years = np.ones(1946)*25
thirty_years = np.ones(1946)*30

all_years = np.hstack([one_year,five_years, ten_years, fifteen_years, twenty_years, twentyfive_years, thirty_years])

# 4. combine into a single array
both_df['Duration'] = all_years
both_df['Ensemble'] = both_names

# 5. extract hist data that corresponds to plot
years = [0, 5, 10, 15, 20, 25, 30]
plot_hist = np.zeros(7)
for i in range(7):
    plot_hist[i] = hist_percentiles[years[i]]

# 6. set up boxplot parameters
my_pal = {'baseline': 'cornflowerblue', 'climate': 'indianred'}

PROPS = {
    'boxprops':{'facecolor':'none', 'edgecolor':'none'},
    'medianprops':{'color':'none'},
    'whiskerprops':{'color':'none'},
    'capprops':{'color':'none'}
}

# 7. plot boxplots
fig, axes = plt.subplots(2,1, figsize=(10,7))

axes[0].plot(np.arange(105), total_hist*1233.48/1000000)
axes[0].fill_between([43,53], [30000,30000], [0,0], color='goldenrod', alpha=.4)
axes[0].fill_between([91,96], [30000,30000], [0,0], color='goldenrod', alpha=.4)
axes[0].set_xlim(0,104)
axes[0].set_xticks(np.arange(1, 121,20))
axes[0].set_xticklabels([1910, 1930, 1950, 1970, 1990, 2010])
axes[0].set_ylim([0,25000])
axes[0].set_ylabel('Flow (Million $m^3$)')

sns.boxplot(data=both_df, x = 'Duration', y = 'Mean Flow (maf)' , hue='Ensemble',
            showfliers=False, palette=my_pal, whis=[5,95], ax = axes[1])
axes[1].scatter(np.arange(7), plot_hist*1233.48/1000000, s=100, color='darkblue',zorder=5)
axes[1].set_ylim([3000,13000])
axes[1].set_xlim([.5,6.5])
axes[1].set_ylabel('Combined Outflow (Million $m^3$)')
axes[1].set_xlabel('Duration')
axes[1].legend(loc='lower right')
plt.tight_layout()
plt.savefig('Powell_full.pdf')

#plt.show()
