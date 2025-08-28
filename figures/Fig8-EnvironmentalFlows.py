import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import seaborn as sns

# Calculate historical frequency of environmental flows

# upper Colorado
pq_file = pd.read_parquet('../../Results/cm/historical/parquet/cm2015B.parquet', engine='pyarrow')
fifteen_mile = pq_file[pq_file['structure_id'] == '7202003']
hist_tots = fifteen_mile[fifteen_mile['month']=='TOT']
hist_shortage = hist_tots['shortage_total'].astype(float)
hist_shortage= hist_shortage.to_numpy()
cm_hist = np.count_nonzero(hist_shortage)

# White
pq_file = pd.read_parquet('../../Results/wm/historical/parquet/wm2015B.parquet', engine='pyarrow')

watson_utah = pq_file[pq_file['river_id'] == '09306500']

august_flows = watson_utah[watson_utah['month'] == 'AUG']
august_flows = august_flows['station_balance_river_outflow'].astype(float)
august_flows = august_flows.to_numpy()

september_flows = watson_utah[watson_utah['month'] == 'SEP']
september_flows = september_flows['station_balance_river_outflow'].astype(float)
september_flows = september_flows.to_numpy()

october_flows = watson_utah[watson_utah['month'] == 'OCT']
october_flows = october_flows['station_balance_river_outflow'].astype(float)
october_flows = october_flows.to_numpy()

ASO = np.vstack([august_flows , september_flows, october_flows])

fails = 0
for i in range(105):
    if ASO[0, i] < 12348 or ASO[1, i] < 16618 or ASO[2, i] < 18447:
        fails += 1

wm_hist = fails

#%% Yampa
pq_file = pd.read_parquet('../../Results/ym/historical/parquet/ym2015B.parquet', engine='pyarrow')

deerlodge = pq_file[pq_file['river_id'] == '09260050']

august_flows = deerlodge[deerlodge['month'] == 'AUG']
august_flows = august_flows['station_balance_river_outflow'].astype(float)
august_flows = august_flows.to_numpy()

september_flows = deerlodge[deerlodge['month'] == 'SEP']
september_flows = september_flows['station_balance_river_outflow'].astype(float)
september_flows = september_flows.to_numpy()

october_flows = deerlodge[deerlodge['month'] == 'OCT']
october_flows = october_flows['station_balance_river_outflow'].astype(float)
october_flows = october_flows.to_numpy()

ASO = np.vstack([august_flows , september_flows, october_flows])

fails = 0
for i in range(105):
    if ASO[0, i] < 7379 or ASO[1, i] < 7141 or ASO[2, i] < 11900:
        fails += 1

ym_hist = fails

#%% Gunnison
pq_file = pd.read_parquet('../../Results/gm/historical/parquet/gm2015B.parquet', engine='pyarrow')

gunn = pq_file[pq_file['river_id'] == '09152500']

august_flows = gunn[gunn['month'] == 'AUG']
august_flows = august_flows['station_balance_river_outflow'].astype(float)
august_flows = august_flows.to_numpy()

september_flows = gunn[gunn['month'] == 'SEP']
september_flows = september_flows['station_balance_river_outflow'].astype(float)
september_flows = september_flows.to_numpy()

october_flows = gunn[gunn['month'] == 'OCT']
october_flows = october_flows['station_balance_river_outflow'].astype(float)
october_flows = october_flows.to_numpy()

ASO = np.vstack([august_flows , september_flows, october_flows])

fails = 0
for i in range(105):
    if ASO[0, i] < 63347.27 or ASO[1, i] < 63347.27 or ASO[2, i] < 63347.27:
        fails += 1

gm_hist = fails


#%%
########################################################################################################################
# load the HMM ensembles, calculate the average and the 95th percentiles

# colorado
cm_baseline = np.loadtxt('figureData/cm/baseline_env_shortage_freq.csv', delimiter=',')
cm_baseline_mean = np.mean(cm_baseline)
cm_baseline_ninetyfifth = np.percentile(cm_baseline, 95)

cm_climate = np.loadtxt('figureData/cm/AdjustedClimate_env_shortage_freq.csv', delimiter=',')
cm_climate_mean = np.mean(cm_climate)
cm_climate_ninetyfifth = np.percentile(cm_climate, 95)

# Gunnison
gm_baseline = np.loadtxt(figureData/gm/baseline_env_shortage_freq.csv', delimiter=',')
gm_baseline_mean = np.mean(gm_baseline)
gm_baseline_ninetyfifth = np.percentile(gm_baseline, 95)

gm_climate = np.loadtxt('figureData/gm/AdjustedClimate_env_shortage_freq_flow.csv', delimiter=',')
gm_climate_mean = np.mean(gm_climate)
gm_climate_ninetyfifth = np.percentile(gm_climate, 95)

# Yampa
ym_baseline = np.loadtxt('figureData/ym/baseline_env_shortage_freq.csv', delimiter=',')
ym_baseline_mean = np.mean(ym_baseline)
ym_baseline_ninetyfifth = np.percentile(ym_baseline, 95)

ym_climate = np.loadtxt('figureData/ym/AdjustedClimate_env_shortage_freq.csv', delimiter=',')
ym_climate_mean = np.mean(ym_climate)
ym_climate_ninetyfifth = np.percentile(ym_climate, 95)

# White
wm_baseline = np.loadtxt('figureData/wm/baseline_env_shortage_freq.csv', delimiter=',')
wm_baseline_mean = np.mean(wm_baseline)
wm_baseline_ninetyfifth = np.percentile(wm_baseline, 95)

wm_climate = np.loadtxt('figureData/wm/AdjustedClimate_env_shortage_freq.csv', delimiter=',')
wm_climate_mean = np.mean(wm_climate)
wm_climate_ninetyfifth = np.percentile(wm_climate, 95)

# San Juan / Dolores (just dolores in this case)
sj_baseline = np.loadtxt('figureData/sj/baseline_env_shortage_freq.csv', delimiter=',')
sj_baseline_mean = np.mean(sj_baseline)
sj_baseline_ninetyfifth = np.percentile(sj_baseline, 95)

sj_climate = np.loadtxt('figureData/sj/AdjustedClimate_env_shortage_freq.csv', delimiter=',')
sj_climate_mean = np.mean(sj_climate)
sj_climate_ninetyfifth = np.percentile(sj_climate, 95)

sj_hist = 7 # calcuated on the cube
#%% create dataframes for each

cm_df = pd.DataFrame({'mean': [cm_hist, cm_baseline_mean, cm_climate_mean],
                      '95th percentile': [cm_hist, cm_baseline_ninetyfifth, cm_climate_ninetyfifth],
                     'Record type': ['Historical', 'Baseline', 'Climate']})
gm_df = pd.DataFrame({'mean': [gm_hist, gm_baseline_mean, gm_climate_mean],
                      '95th percentile': [gm_hist, gm_baseline_ninetyfifth, gm_climate_ninetyfifth],
                     'Record type': ['Historical', 'Baseline', 'Climate']})
ym_df = pd.DataFrame({'mean': [ym_hist, ym_baseline_mean, ym_climate_mean],
                      '95th percentile': [ym_hist, ym_baseline_ninetyfifth, ym_climate_ninetyfifth],
                     'Record type': ['Historical', 'Baseline', 'Climate']})
wm_df = pd.DataFrame({'mean': [wm_hist, wm_baseline_mean, wm_climate_mean],
                      '95th percentile': [wm_hist, wm_baseline_ninetyfifth, wm_climate_ninetyfifth],
                     'Record type': ['Historical', 'Baseline', 'Climate']})
sj_df = pd.DataFrame({'mean': [sj_hist, sj_baseline_mean, sj_climate_mean],
                      '95th percentile': [sj_hist, sj_baseline_ninetyfifth, sj_climate_ninetyfifth],
                     'Record type': ['Historical', 'Baseline', 'Climate']})

#%%

fig, axes = plt.subplots(2,3, figsize=(8,5))
cm_top = sns.barplot(x='Record type', y='95th percentile', data=cm_df, color='#540b0e', alpha=.5, ax=axes.flatten()[0])
cm_bot = sns.barplot(x='Record type', y='mean', data=cm_df, color='#540b0e', ax=axes.flatten()[0])

gm_top = sns.barplot(x='Record type', y='95th percentile', data=gm_df, color='#9e2a2b', alpha =.5, ax=axes.flatten()[1])
gm_bot = sns.barplot(x='Record type', y='mean', data=gm_df, color='#9e2a2b', ax=axes.flatten()[1])

ym_top = sns.barplot(x='Record type', y='95th percentile', data=ym_df, color='#e09f3e', alpha=.5, ax=axes.flatten()[2])
ym_bot = sns.barplot(x='Record type', y='mean', data=ym_df, color='#e09f3e', ax=axes.flatten()[2])

wm_top = sns.barplot(x='Record type', y='95th percentile', data=wm_df, color='#d9c86a', alpha=.5, ax=axes.flatten()[3])
wm_bot = sns.barplot(x='Record type', y='mean', data=wm_df, color='#d9c86a', ax=axes.flatten()[3])

sj_top = sns.barplot(x='Record type', y='95th percentile', data=sj_df, color='#335c67', alpha=.5, ax=axes.flatten()[4])
sj_bot = sns.barplot(x='Record type', y='mean', data=sj_df, color='#335c67', ax=axes.flatten()[4])

for i in range(5):
    axes.flatten()[i].set_ylim([0,100])
    axes.flatten()[i].set_ylabel('')
axes.flatten()[5].set_visible(False)
plt.tight_layout()
#plt.show()
plt.savefig('EnvironmentalFlow.pdf')

