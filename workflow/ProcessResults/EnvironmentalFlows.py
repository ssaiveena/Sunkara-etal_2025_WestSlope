import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

# Modify file path
os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/paper_code/ProcessResults')

# upper Colorado - uses shortage output from StateMod
pq_file = pd.read_parquet('../../Results/cm/historical/parquet/cm2015B.parquet', engine='pyarrow')
fifteen_mile = pq_file[pq_file['structure_id'] == '7202003']
hist_tots = fifteen_mile[fifteen_mile['month']=='TOT']
hist_shortage = hist_tots['shortage_total'].astype(float)
hist_shortage= hist_shortage.to_numpy()
cm_hist = np.count_nonzero(hist_shortage)

abbrev = 'cm'
record_type = 'AdjustedClimate' # change this to 'baseline' for baseline run
num_shortages = np.zeros(1000)

for r in tqdm(range(1000)):
    pq_file = pd.read_parquet(
                '../../Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B_S' + str(
                    r) + '_1.parquet',
                engine='pyarrow')
    fifteen_mile = pq_file[pq_file['structure_id'] == '7202003']
    tots = fifteen_mile[fifteen_mile['month'] == 'TOT']
    shortage = tots['shortage_total'].astype(float)
    shortage = shortage.to_numpy()
    num_shortages[r] = np.count_nonzero(shortage)

np.savetxt('../../Results/cm/AdjustedClimate_env_shortage_freq.csv', num_shortages, delimiter=',')



# Gunnison - calculated after run using flow at gage 09152500
abbrev = 'gm'
record_type = 'AdjustedClimate' # change this to 'baseline' for baseline run
num_shortages = np.zeros(1000)

for r in tqdm(range(0, 1000)):
    pq_file = pd.read_parquet(
        '../../Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B_S' + str(
            r) + '_1.parquet',
        engine='pyarrow')

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

    num_shortages[r] = fails

np.savetxt('../../Results/gm/AdjustedClimate_env_shortage_freq_flow.csv', num_shortages, delimiter=',')


# Yampa - calculated after run using flow at gage 09260050
abbrev = 'ym' 
record_type = 'AdjustedClimate' # change this to 'baseline' for baseline run
num_shortages = np.zeros(1000)

for r in tqdm(range(0, 1000)):
    pq_file = pd.read_parquet(
        '../../Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B_S' +
        str(r) + '_1.parquet', engine='pyarrow')

    watson_utah = pq_file[pq_file['river_id'] == '09260050']

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
        if ASO[0, i] < 7379 or ASO[1, i] < 7141 or ASO[2, i] < 11900:
            fails += 1

    num_shortages[r] = fails

np.savetxt('../../Results/ym/AdjustedClimate_env_shortage_freq.csv', num_shortages, delimiter=',')



# White - calculated after run using flow at gage 09306500
abbrev = 'wm'
record_type = 'AdjustedClimate' # change this to 'baseline' for baseline run
num_shortages = np.zeros(1000)

for r in tqdm(range(0, 1000)):
    pq_file = pd.read_parquet(
        '../../Results/' + abbrev + '/' + record_type + '/parquet/' + abbrev + '2015B_S' + str(
            r) + '_1.parquet',
        engine='pyarrow')

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

    num_shortages[r] = fails

np.savetxt('../../Results/wm/AdjustedClimate_env_shortage_freq.csv', num_shortages, delimiter=',')


# Southwest - calculated using reservoir release data
def extract_ASO_releases(abbrev, res_name, record_type, realization):
    '''
    writes a csv file of monthly storage for a given realization
    
    :param abbrev:                      a string representing basin abbreviation
    :param res_name:                    a string representing the name of the reservoir (ex BM for Blue Mesa)
    :param record_type:                 string, type of statemod run (historical, baseline or climate)
    :param realization:                 float, the realization number (put 10000 for hist)
    
    :returns monthly_means:             a  numpy array of mean reservoir levels across the 105 year record
    '''

    fails = 0
    if realization not in [13, 17, 74,110,111,116,145,162,203,208,224,225,267,288,346,459,483,492,563,588,664,713,727,843,845,917,974]:
        xre_data = pd.read_csv(abbrev + '/' + record_type + '/' + res_name + 'S' + str(realization) + '_xre_data.csv', index_col=False)

        account_0 = xre_data[xre_data['ACC']==0]

        august_releases = account_0[account_0['MO']=='AUG']
        august_releases = august_releases['River Outflow'].to_numpy()

        september_releases = account_0[account_0['MO']=='SEP']
        september_releases = september_releases['River Outflow'].to_numpy()

        october_releases = account_0[account_0['MO']=='OCT']
        october_releases = october_releases['River Outflow'].to_numpy()

        ASO = np.vstack([august_releases, september_releases, october_releases])


        fails = 0
        for i in range(105):
            if ASO[0, i] < 3612 or ASO[1, i] < 2112 or ASO[2, i] < 2112:
                fails += 1

    return fails


num_fails = np.zeros(1000)
abbrev = 'sj'
res_name = 'MR'
record_type = 'AdjustedClimate' # change this for baseline


for r in range(1000):
    num_fails[r] = extract_ASO_releases(abbrev, res_name, record_type, r)

np.savetxt(res_name + '_' + record_type + '_environmental_flows.csv', num_fails, delimiter=',')