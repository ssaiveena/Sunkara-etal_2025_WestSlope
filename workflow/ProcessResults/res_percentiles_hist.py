import pandas as pd
import numpy as np

def extract_res_percentiles(abbrev, res_name):
	'''
	writes a csv file of monthly storage for a given realization
	
	:param abbrev:                      a string representing basin abbreviation
	:param res_name:					a string representing the name of the reservoir (ex BM for Blue Mesa)
	
	:returns monthly_means:				a  numpy array of mean reservoir levels across the 105 year record
	'''

	xre_data = pd.read_csv(abbrev + '/'  + res_name + '_hist_xre_data.csv', index_col=False)

	account_0 = xre_data[xre_data['ACC']==0]

	account_0 = account_0[account_0['MO'] != 'TOT']

	monthly_array = account_0['Init. Storage'].to_numpy()



	res_percentiles = np.zeros(99)
	
	for i, p in enumerate(range(1,100,1)):
		res_percentiles[i] = np.percentile(monthly_array, p)

	return res_percentiles



realization_percentiles = np.zeros(99)


abbrev = 'sj'
res_name = 'MR'

realization_percentiles = extract_res_percentiles(abbrev, res_name)

np.savetxt(res_name + '_realizationPercentiles_hist_1_to_99.csv', realization_percentiles, delimiter=',')