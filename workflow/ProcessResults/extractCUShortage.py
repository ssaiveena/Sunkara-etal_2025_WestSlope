import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from tqdm import tqdm
import os
#os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/code/final_data_analysis')
#%%
def extract_shortage_info(abbrev, realization, record_type, exports, exportNodes):
    """
    pandas df of shortage information
    :param abbrev:                      a string representing basin abbreviation
    :param realization:                 float, the realization number (put 10000 for hist)
    :param record_type:                 string, type of statemod run (historical, baseline or climate)
    :param exports:                     bool, specifies if basin has exports across divide or to NM
    :param exportNodes:                 list, the structure IDs of export nodes in the basin

    :return median_shortage:            float, the median total basin shortage across all years
    :return ninetieth_shortage:         float, the 90th percentile of total shortage
    :return ninetyninth_shortage:       float, the 99th percentile of total shortage
    """
    #if realization not in [708, 397, 309, 220, 556, 477, 242, 118, 508, 287, 786, 310, 375, 445, 734, 540, 728, 208,
    #                       493, 59, 9, 293, 113, 567, 930, 985, 915, 960]:
    if record_type != 'historical':
        pq_file = pd.read_parquet(
           'Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B_S' + str(
           realization) + '_1.parquet',
                engine='pyarrow')
    else:
        pq_file = pd.read_parquet(
            'Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B.parquet',
            engine='pyarrow')

    # remove the exports
    if exports:
        for export in range(len(exportNodes)):
            pq_file = pq_file[pq_file['structure_id'].str.contains(exportNodes[export]) == False]

    # Extract only the annual totals
    pq_tot = pq_file[pq_file['month'] == 'TOT']

    # get unique structure IDs
    pq_structures = pq_tot['structure_id'].unique()

    # intialize arrays to store yearly shortage and shortage ratios
    yearly_shortage_total = np.zeros([105, len(pq_structures)])

    # loop through all years
    for y in range(1909, 2014):
        year_temp = pq_tot[pq_tot['year'] == str(y)] # a dataframe with data from a single year

        #loop through structures
        for i, id in enumerate(pq_structures):
            struct_temp = year_temp[year_temp['structure_id'] == id] # a dataframe with structures from a single year
            # if there is shortage, add to total and calc shortage ratio
            if float(struct_temp['shortage_cu'].iloc[0]) > 0:
                yearly_shortage_total[y - 1909, i] = float(struct_temp['shortage_cu'].iloc[0])

            else:
                yearly_shortage_total[y - 1909, i] = 0

        #users_in_shortage = np.count_nonzero(yearly_shortage_total, axis=1) / len(pq_structures)
    total_basin_shortage = np.sum(yearly_shortage_total, axis=1)

    return total_basin_shortage
#%% Southwest Baseline
sj_baseline = np.zeros([1000,105])

for r in tqdm(range(1000)):
    sj_baseline[r, :] = extract_shortage_info('sj', r, 'baseline', True, ['7799999'])

np.savetxt('Results/Shortage/cu/updated_sj_climate_no_export.csv', sj_baseline, delimiter=',')
#%% Southwest Climate
sj_climate = np.zeros([1000,105])
sj_error = [13, 17, 74,110,111,116,145,162,203,208,224,225,267,288,346,459,483,492,563,588,664,713,727,843,845,917,974]
for r in tqdm(range(1000)):
    if r not in sj_error:
        sj_climate[r, :] = extract_shortage_info('sj', r, 'AdjustedClimate', True, ['7799999'])

np.savetxt('Results/Shortage/cu/sj_AdjustedClimate_no_export.csv', sj_climate, delimiter=',')

#%% Upper Colorado Baseline
uc_baseline = np.zeros([105,1000])

for r in tqdm(range(1000)):
    uc_baseline[:, r] = extract_shortage_info('cm', r, 'baseline', True, ['380941', '5100958', '5104634', '5104655','5100639',
                                                              '5101309_D', '5101310', '5101269', '3804625', '3604683SU',
                                                              '5104655', '3804625SU', '3704614', '3704643', '3604684'])

np.savetxt('Results/Shortage/cu/updated_cm_baseline_no_export.csv', uc_baseline, delimiter=',')

#%% Upper Colorado Climate
uc_climate = np.zeros([105,1000])

for r in tqdm(range(1000)):
    uc_climate[:, r] = extract_shortage_info('cm', r, 'AdjustedClimate', True, ['380941', '5100958', '5104634', '5104655','5100639',
                                                              '5101309_D', '5101310', '5101269', '3804625', '3604683SU',
                                                              '5104655', '3804625SU', '3704614', '3704643', '3604684'])

np.savetxt('Results/Shortage/cu/cm_Adjustedclimate_no_export.csv', uc_climate, delimiter=',')
#%%
# Gunnison Baseline
gm_baseline = np.zeros([105,1000])
for r in tqdm(range(1000)):
    gm_baseline[:,r] = extract_shortage_info('gm', r, 'baseline', False, [])
np.savetxt('Results/Shortage/cu/updated_gm_baseline.csv', gm_baseline, delimiter=',')
#%%
# Gunnison Climate
gm_climate = np.zeros([105,1000])
for r in tqdm(range(1000)):
    gm_climate[:,r] = extract_shortage_info('gm', r, 'AdjustedClimate', False, [])
np.savetxt('Results/Shortage/cu/gm_Adjustedclimate.csv', gm_climate, delimiter=',')
#%% Yampa Climate
ym_climate = np.zeros([105,1000])

for r in tqdm(range(1000)):
    ym_climate[:, r] = extract_shortage_info('ym', r, 'AdjustedClimate', False, [])

np.savetxt('Results/Shortage/cu/ym_AdjustedClimate_no_export.csv', ym_climate, delimiter=',')

#%% White Climate
wm_climate = np.zeros([105,1000])

for r in tqdm(range(1000)):
    wm_climate[:, r] = extract_shortage_info('wm', r, 'AdjustedClimate', False, [])

np.savetxt('Results/Shortage/cu/wm_AdjustedClimate_no_export.csv', wm_climate, delimiter=',')