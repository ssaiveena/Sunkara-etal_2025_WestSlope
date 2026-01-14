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
cm_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/cm/baseline/cm_hist_outflow.csv', delimiter=',')
gm_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/gm/baseline/gm_hist_outflow.csv', delimiter=',')
ym_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/ym/baseline/ym_hist_outflow.csv', delimiter=',')
wm_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/wm/baseline/wm_hist_outflow.csv', delimiter=',')
sj_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/sj/baseline/sj_hist_outflow.csv', delimiter=',')

#%% correct cm
cm_gm = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Results/cm_gm_mod_hist_outflow.csv', delimiter=',')

cm_corrected = cm_hist - cm_gm
#%%
total_hist = cm_corrected + gm_hist + ym_hist + wm_hist + sj_hist
print(np.mean(total_hist))
exit()
# read in baseline data
cm_baseline = np.loadtxt('Results/cm_mod_climate_outflow_demand.csv', delimiter=',')
gm_baseline = np.loadtxt('Results/gm_mod_climate_outflow_demand.csv', delimiter=',')
ym_baseline = np.loadtxt('Results/ym_mod_climate_outflow_demand.csv', delimiter=',')
wm_baseline = np.loadtxt('Results/wm_mod_climate_outflow_demand.csv', delimiter=',')
sj_baseline = np.loadtxt('Results/sj_mod_climate_outflow_demand.csv', delimiter=',')

#%%
cm_gm_baseline = np.loadtxt('Results/cm_gm_mod_climate_outflow_demand.csv', delimiter=',')

cm_corrected_baseline = cm_baseline - cm_gm_baseline
#%%
total_baseline = cm_corrected_baseline.flatten() + gm_baseline.flatten() + ym_baseline.flatten() + wm_baseline.flatten() +\
                 sj_baseline.flatten()
pd.DataFrame(total_baseline).to_csv('Powell_outflows_demand.csv', header=False, index=False)

# read in the climate data
cm_climate = np.loadtxt('Results/cm_mod_climate_outflow_wodemand.csv', delimiter=',')
gm_climate = np.loadtxt('Results/gm_mod_climate_outflow_wodemand.csv', delimiter=',')
ym_climate = np.loadtxt('Results/ym_mod_climate_outflow_wodemand.csv', delimiter=',')
wm_climate = np.loadtxt('Results/wm_mod_climate_outflow_wodemand.csv', delimiter=',')
sj_climate = np.loadtxt('Results/sj_mod_climate_outflow_wodemand.csv', delimiter=',')
cm_gm_climate = np.loadtxt('Results/cm_gm_mod_climate_outflow_wodemand.csv', delimiter=',')

#%%
cm_mod_climate_corrected = cm_climate - cm_gm_climate
#%%
total_climate = cm_mod_climate_corrected.flatten() + gm_climate.flatten() + ym_climate.flatten() + wm_climate.flatten() +\
                 sj_climate.flatten()

pd.DataFrame(total_climate).to_csv('Powell_outflows_wodemand.csv', header=False, index=False)

# reshape to annual
baseline_annual = np.reshape(total_baseline, [105,20000])
climate_annual = np.reshape(total_climate, [105,20000])

#%% calculate 1st percentile flows
baseline_percentiles = np.zeros([31, 20000])
climate_percentiles = np.zeros([31, 20000])
hist_percentiles = np.zeros(31)

for i in range(1,32):
    baseline_percentiles[i-1,:] = calculate_moving_ave_percentile(baseline_annual, i, 1, False, 20000)
    climate_percentiles[i-1,:] = calculate_moving_ave_percentile(climate_annual, i, 1, False, 20000)
    hist_percentiles[i-1] = calculate_moving_ave_percentile(total_hist, i, 1, True, 20000)
print(np.mean(total_hist))
# Calculate the maximum and minimums across the moving averages
max_baseline = np.max(baseline_percentiles, axis=1)
min_baseline = np.min(baseline_percentiles, axis=1)

max_climate = np.max(climate_percentiles, axis=1)
min_climate = np.min(climate_percentiles, axis=1)

# Create boxplots
# 1. make a flat array of all percentile data
transposed_baseline_percentiles = np.transpose(baseline_percentiles)*1233.48/1000000
transposed_climate_percentiles = np.transpose(climate_percentiles)*1233.48/1000000

both_ensembles = np.zeros([7, 40000]) #1946])

for i, dur in enumerate([0, 5, 10, 15, 20, 25, 30]):
    both_ensembles[i,:] = np.hstack([transposed_baseline_percentiles[:,dur], transposed_climate_percentiles[:,dur]])

both_ensembles_flat = both_ensembles.flatten()

#save both ensembles with shape 7,40000 for sensitivity analysis of deliveries to Lake Powell
pd.DataFrame(both_ensembles).to_csv('Powell_outflows_duration.csv', header=False, index=False)

# 2. create an array of strings for noting which is which
climate_name = ['climate'] * 20000
baseline_name = ['baseline'] * 20000
both_names = np.hstack([baseline_name, climate_name, baseline_name, climate_name, baseline_name, climate_name,
                        baseline_name, climate_name, baseline_name, climate_name, baseline_name, climate_name,
                        baseline_name, climate_name])

# make an initial data frame with one column containing the flows
both_df = pd.DataFrame(both_ensembles_flat, columns=['Mean Flow (maf)'])

# 3. make a new array that specifies the rolling average of each flow
one_year = np.ones(40000)
five_years = np.ones(40000)*5
ten_years = np.ones(40000)*10
fifteen_years = np.ones(40000)*15
twenty_years = np.ones(40000)*20
twentyfive_years = np.ones(40000)*25
thirty_years = np.ones(40000)*30

all_years = np.hstack([one_year,five_years, ten_years, fifteen_years, twenty_years, twentyfive_years, thirty_years])

# 4. combine into a single array
both_df['Duration'] = all_years
both_df['Ensemble'] = both_names

# 5. extract hist data that corresponds to plot
years = [0, 5, 10, 15, 20, 25, 30]
plot_hist = np.zeros(7)
for i in range(7):
    plot_hist[i] = hist_percentiles[years[i]]
print(plot_hist)
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

#axes[0].plot(np.arange(105), total_hist*1233.48/1000000)
axes[0].fill_between([43,53], [30000,30000], [0,0], color='goldenrod', alpha=.4)
axes[0].fill_between([91,96], [30000,30000], [0,0], color='goldenrod', alpha=.4)
axes[0].set_xlim(0,104)
axes[0].set_xticks(np.arange(1, 121,20))
axes[0].set_xticklabels([1910, 1930, 1950, 1970, 1990, 2010])
#axes[0].set_ylim([0,25000])
axes[0].set_ylabel('Flow (Million $m^3$)')

sns.boxplot(data=both_df, x = 'Duration', y = 'Mean Flow (maf)' , hue='Ensemble',
            showfliers=False, palette=my_pal, whis=[5,95], ax = axes[1])
axes[1].scatter(np.arange(7), plot_hist*1233.48/1000000, s=100, color='darkblue',zorder=5, label='Historical')
#axes[1].set_ylim([3000,13000])
axes[1].set_xlim([.5,6.5])
axes[1].set_ylabel('Combined Outflow (Million $m^3$)')
axes[1].set_xlabel('Duration')
axes[1].legend(loc='lower right')
plt.legend([])
plt.tight_layout()
# plt.savefig('Powell_full.pdf')

plt.show()
