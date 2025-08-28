import pandas as pd
import numpy as np

def extract_res_percentiles(abbrev, res_name, record_type, realization):
	'''
	writes a csv file of monthly storage for a given realization
	
	:param abbrev:                      a string representing basin abbreviation
	:param res_name:					a string representing the name of the reservoir (ex BM for Blue Mesa)
    :param record_type:                 string, type of statemod run (historical, baseline or climate)
    :param realization:                 float, the realization number (put 10000 for hist)
	
	:returns monthly_means:				a  numpy array of mean reservoir levels across the 105 year record
	'''

	xre_data = pd.read_csv(abbrev + '/' + record_type + '/' + res_name + 'S' + str(realization) + '_xre_data.csv', index_col=False)

	account_0 = xre_data[xre_data['ACC']==0]

	account_0 = account_0[account_0['MO'] != 'TOT']

	monthly_array = account_0['Init. Storage'].to_numpy()



	res_percentiles = np.zeros(99)
	
	for i, p in enumerate(range(1,100,1)):
		res_percentiles[i] = np.percentile(monthly_array, p)



	return res_percentiles



realization_percentiles = np.zeros([99,1000])


abbrev = 'gm'
res_name = 'BM'
record_type = 'AdjustedClimate_05'


for r in range(1000):
	print(r)
	#if r not in [13, 17, 74, 110, 111, 116, 145, 162, 203, 208, 224, 225, 267, 288, 346, 459, 483, 492, 563, 588, 664, 713, 727, 843, 845, 917, 974]:
	realization_percentiles[:,r] = extract_res_percentiles(abbrev, res_name, record_type, r)

np.savetxt(res_name + '_realizationPercentiles_' + record_type + '_1_to_99.csv', realization_percentiles, delimiter=',')