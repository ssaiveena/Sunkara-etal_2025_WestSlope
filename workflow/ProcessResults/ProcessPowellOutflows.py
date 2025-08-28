import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/paper_code/final_data_analysis')
#%%
def extract_total_annual_flow(abbrev, realization, record_type):
    """
    extracts total annual outflows from a parquet file of statemod output (originally from xdd data)

    returns an array of total annual flow for a realization
    :param abbrev:              a string representing basin abbreviation
    :param realization:         float, the realization number
    :param record_type:         string, type of statemod run (historical, baseline or climate)

    :returns an array of annual flows from the last node of the basin
    """

    if abbrev == 'cm':
        basin_name = 'Upper_Colorado'
        last_node_name = 'coloup_end'
    elif abbrev == 'gm':
        basin_name = 'Gunnison'
        last_node_name = 'gunn_end'
    elif abbrev == 'ym':
        basin_name = 'Yampa'
        last_node_name = '09260050'
    elif abbrev == 'wm':
        basin_name = 'White'
        last_node_name = '09306395'
    elif abbrev == 'sj':
        basin_name = 'SanJuan_Dolores'
        last_node_name = 'Sanjdol_end'
    else:
        print('Must use one of the following basin abbrevs: cm, gm, ym, wm, sj')

    if record_type != 'historical':
        pq_file = pd.read_parquet('../../Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B_S' + str(realization) + '_1.parquet',
                                  engine='pyarrow')
    else:
        pq_file = pd.read_parquet('../../Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B.parquet',
                                  engine='pyarrow')

    final_node = pq_file[pq_file['river_id'] == last_node_name]
    annual_flow = final_node[final_node['month'] == 'TOT']
    annual_flow.loc[annual_flow['station_balance_river_outflow']=='********'] = 10000000

    annual_flow = annual_flow['station_balance_river_outflow'].astype(float)

    return np.array(annual_flow)

#%% Baseline ensemble
abbrevs = ['cm', 'gm', 'ym', 'wm', 'sj']
cm_baseline = np.zeros([105, 1000])
gm_baseline = np.zeros([105, 1000])
ym_baseline = np.zeros([105, 1000])
wm_baseline = np.zeros([105, 1000])
sj_baseline = np.zeros([105, 1000])

for r in tqdm(range(1000)):
    cm_baseline[:, r] = extract_total_annual_flow('cm', r, 'baseline')
    gm_baseline[:, r] = extract_total_annual_flow('gm', r, 'baseline')
    ym_baseline[:, r] = extract_total_annual_flow('ym', r, 'baseline')
    wm_baseline[:, r] = extract_total_annual_flow('wm', r, 'baseline')
    sj_baseline[:, r] = extract_total_annual_flow('sj', r, 'baseline')

#%% Climate ensemble
cm_climate = np.zeros([105, 1000])
gm_climate = np.zeros([105, 1000])
ym_climate = np.zeros([105, 1000])
wm_climate = np.zeros([105, 1000])
sj_climate = np.zeros([105, 1000])

sj_error = [23, 29, 40, 47, 96, 116, 150, 205, 264, 275, 284, 303, 354, 420,
            568, 579, 593, 597, 648, 664, 670, 720, 817, 820, 874, 883, 901, 970]

for r in tqdm(range(1000)):
    cm_climate[:, r] = extract_total_annual_flow('cm', r, 'mod_climate')
    gm_climate[:, r] = extract_total_annual_flow('gm', r, 'mod_climate')
    ym_climate[:, r] = extract_total_annual_flow('ym', r, 'mod_climate')
    wm_climate[:, r] = extract_total_annual_flow('wm', r, 'mod_climate')
    if r not in sj_error:
        sj_climate[:, r] = extract_total_annual_flow('sj', r, 'mod_climate')

#%%
np.savetxt('../../Results/cm/mod_climate/cm_mod_climate_outflow.csv', cm_climate, delimiter=',')
np.savetxt('../../Results/gm/mod_climate/gm_mod_climate_outflow.csv', gm_climate, delimiter=',')
np.savetxt('../../Results/ym/mod_climate/ym_mod_climate_outflow.csv', ym_climate, delimiter=',')
np.savetxt('../../Results/wm/mod_climate/wm_mod_climate_outflow.csv', wm_climate, delimiter=',')
np.savetxt('../../Results/sj/mod_climate/sj_mod_climate_outflow.csv', sj_climate, delimiter=',')