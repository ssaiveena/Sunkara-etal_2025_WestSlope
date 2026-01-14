import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
#os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/paper_code/final_data_analysis')
#%%
def extract_total_annual_flow(abbrev, hmm,realization, record_type):
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
    elif abbrev == "cm_gm":
        abbrev = 'cm'
        basin_name = 'Upper_Colorado'
        last_node_name = '09152500'
    else:
        print('Must use one of the following basin abbrevs: cm, gm, ym, wm, sj')

    if record_type != 'historical':
        pq_path = f'../withdemand/{abbrev}2015B_S{hmm}_{realization}.parquet'
        
        if not os.path.exists(pq_path):
            return np.zeros(105)  # Avoid unnecessary computation
        pq_file = pd.read_parquet(pq_path, engine='pyarrow')
    else:
        pq_file = pd.read_parquet('../../Results/'  + abbrev + '2015B.parquet',
                                  engine='pyarrow')

    final_node = pq_file[pq_file['river_id'] == last_node_name]
    annual_flow = final_node[final_node['month'] == 'TOT']
    annual_flow1 = annual_flow.copy(deep=True)
    annual_flow1.loc[annual_flow1['station_balance_river_outflow']=='********'] = 10000000
    # annual_flow.loc[annual_flow['station_balance_river_outflow'] == '********', 'station_balance_river_outflow'] = 10000000
    annual_flow1 = annual_flow1['station_balance_river_outflow'].astype(float)

    return np.array(annual_flow1)

#%% Baseline ensemble
abbrevs = ['cm', 'gm', 'ym', 'wm', 'sj']
# cm_baseline = np.zeros([105, 20000])
# gm_baseline = np.zeros([105, 20000])
# ym_baseline = np.zeros([105, 20000])
# wm_baseline = np.zeros([105, 20000])
# sj_baseline = np.zeros([105, 20000])
# baseline    = np.zeros([105, 20000])
# ind=0
# for hmm in range(1000):#1000
#     for r in range(20):#2
#         # cm_baseline[:, ind] = extract_total_annual_flow('cm', hmm, r, 'baseline')
#         # gm_baseline[:, ind] = extract_total_annual_flow('gm',hmm, r, 'baseline')
#         ym_baseline[:, ind] = extract_total_annual_flow('ym', hmm,r, 'baseline')
#         wm_baseline[:, ind] = extract_total_annual_flow('wm',hmm, r, 'baseline')
#         # sj_baseline[:, ind] = extract_total_annual_flow('sj', hmm,r, 'baseline')
#         # baseline[:, ind] = extract_total_annual_flow('cm_gm', hmm,r, 'baseline')
#         ind=ind+1
# np.savetxt('Results/cm_mod_climate_outflow_demand.csv', cm_baseline, delimiter=',')
# np.savetxt('Results/gm_mod_climate_outflow_demand.csv', gm_baseline, delimiter=',')
# np.savetxt('Results/ym_mod_climate_outflow_demand.csv', ym_baseline, delimiter=',')
# np.savetxt('Results/wm_mod_climate_outflow_demand.csv', wm_baseline, delimiter=',')
# np.savetxt('Results/sj_mod_climate_outflow_demand.csv', sj_baseline, delimiter=',')
# np.savetxt('Results/cm_gm_mod_climate_outflow_demand.csv', baseline, delimiter=',')

def extract_total_month_flow(abbrev, hmm,realization, record_type):
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
    elif abbrev == "cm_gm":
        abbrev = 'cm'
        basin_name = 'Upper_Colorado'
        last_node_name = '09152500'
    else:
        print('Must use one of the following basin abbrevs: cm, gm, ym, wm, sj')

    if record_type != 'historical':
        pq_path = f'../withdemand/{abbrev}2015B_S{hmm}_{realization}.parquet'
        
        if not os.path.exists(pq_path):
            return np.zeros(105*12)  # Avoid unnecessary computation
        pq_file = pd.read_parquet(pq_path, engine='pyarrow')
    else:
        pq_file = pd.read_parquet('../../Results/'  + abbrev + '2015B.parquet',
                                  engine='pyarrow')

    final_node = pq_file[pq_file['river_id'] == last_node_name]
    annual_flow = final_node[final_node['month'] != 'TOT']
    annual_flow1 = annual_flow.copy(deep=True)
    annual_flow1.loc[annual_flow1['station_balance_river_outflow']=='********'] = 10000000
    # annual_flow.loc[annual_flow['station_balance_river_outflow'] == '********', 'station_balance_river_outflow'] = 10000000
    annual_flow1 = annual_flow1['station_balance_river_outflow'].astype(float)

    return np.array(annual_flow1)

#%% Full ensemble
abbrevs = ['cm', 'gm', 'ym', 'wm', 'sj']
cm_baseline = np.zeros([105*12, 20000])
gm_baseline = np.zeros([105*12, 20000])
ym_baseline = np.zeros([105*12, 20000])
wm_baseline = np.zeros([105*12, 20000])
sj_baseline = np.zeros([105*12, 20000])
baseline    = np.zeros([105*12, 20000])
ind=0
for hmm in range(1000):#1000
    for r in range(20):#2
        cm_baseline[:, ind] = extract_total_month_flow('cm', hmm, r, 'baseline')
        gm_baseline[:, ind] = extract_total_month_flow('gm',hmm, r, 'baseline')
        ym_baseline[:, ind] = extract_total_month_flow('ym', hmm,r, 'baseline')
        wm_baseline[:, ind] = extract_total_month_flow('wm',hmm, r, 'baseline')
        sj_baseline[:, ind] = extract_total_month_flow('sj', hmm,r, 'baseline')
        baseline[:, ind] = extract_total_month_flow('cm_gm', hmm,r, 'baseline')
        ind=ind+1
np.savetxt('Results/cm_month_outflow_demand.csv', cm_baseline, delimiter=',')
np.savetxt('Results/gm_month_outflow_demand.csv', gm_baseline, delimiter=',')
np.savetxt('Results/ym_month_outflow_demand.csv', ym_baseline, delimiter=',')
np.savetxt('Results/wm_month_outflow_demand.csv', wm_baseline, delimiter=',')
np.savetxt('Results/sj_month_outflow_demand.csv', sj_baseline, delimiter=',')
np.savetxt('Results/cm_gm_month_outflow_demand.csv', baseline, delimiter=',')

def extract_total_month_flow_hist(abbrev, hmm,realization, record_type):
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
    elif abbrev == "cm_gm":
        abbrev = 'cm'
        basin_name = 'Upper_Colorado'
        last_node_name = '09152500'
    else:
        print('Must use one of the following basin abbrevs: cm, gm, ym, wm, sj')

    if record_type != 'historical':
        pq_path = f'../withdemand/{abbrev}2015B_S{hmm}_{realization}.parquet'
        
        if not os.path.exists(pq_path):
            return np.zeros(105*12)  # Avoid unnecessary computation
        pq_file = pd.read_parquet(pq_path, engine='pyarrow')
    else:
        pq_file = pd.read_parquet('../../Results/'  + abbrev + '2015B.parquet',
                                  engine='pyarrow')

    final_node = pq_file[pq_file['river_id'] == last_node_name]
    annual_flow = final_node[final_node['month'] != 'TOT']
    annual_flow1 = annual_flow.copy(deep=True)
    annual_flow1.loc[annual_flow1['station_balance_river_outflow']=='********'] = 10000000
    # annual_flow.loc[annual_flow['station_balance_river_outflow'] == '********', 'station_balance_river_outflow'] = 10000000
    annual_flow1 = annual_flow1['station_balance_river_outflow'].astype(float)

    return np.array(annual_flow1)

#%% Baseline ensemble
abbrevs = ['cm', 'gm', 'ym', 'wm', 'sj']
cm_baseline = np.zeros([105*12, 1])
gm_baseline = np.zeros([105*12, 1])
ym_baseline = np.zeros([105*12, 1])
wm_baseline = np.zeros([105*12, 1])
sj_baseline = np.zeros([105*12, 1])
baseline    = np.zeros([105*12, 1])
ind=0
for hmm in range(1):#1000
    for r in range(1):#2
        cm_baseline[:, ind] = extract_total_month_flow_hist('cm', hmm, r, 'historical')
        gm_baseline[:, ind] = extract_total_month_flow_hist('gm',hmm, r, 'historical')
        ym_baseline[:, ind] = extract_total_month_flow_hist('ym', hmm,r, 'historical')
        wm_baseline[:, ind] = extract_total_month_flow_hist('wm',hmm, r, 'historical')
        sj_baseline[:, ind] = extract_total_month_flow_hist('sj', hmm,r, 'historical')
        baseline[:, ind] = extract_total_month_flow_hist('cm_gm', hmm,r, 'historical')
        ind=ind+1
np.savetxt('Results/cm_month_outflow_demand_hist.csv', cm_baseline, delimiter=',')
np.savetxt('Results/gm_month_outflow_demand_hist.csv', gm_baseline, delimiter=',')
np.savetxt('Results/ym_month_outflow_demand_hist.csv', ym_baseline, delimiter=',')
np.savetxt('Results/wm_month_outflow_demand_hist.csv', wm_baseline, delimiter=',')
np.savetxt('Results/sj_month_outflow_demand_hist.csv', sj_baseline, delimiter=',')
np.savetxt('Results/cm_gm_month_outflow_demand_hist.csv', baseline, delimiter=',')