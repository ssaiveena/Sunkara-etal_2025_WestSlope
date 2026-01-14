import pandas as pd
import numpy as np
import os
import csv
from matplotlib import pyplot as plt

def are_first_two_rows_same(csv_file):
    """
    Checks if the first two rows of a CSV file are the same.

    Args:
        csv_file: Path to the CSV file.

    Returns:
        True if the first two rows are the same, False otherwise.
    """
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            try:
                row1 = next(reader)
                row2 = next(reader)
            except StopIteration:
                return False  # Not enough rows in the file
        return row1 == row2
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
        return False
def extract_res_percentiles(abbrev, res_name, record_type, hmm, realization):
	'''
	writes a csv file of monthly storage for a given realization
	
	:param abbrev:                      a string representing basin abbreviation
	:param res_name:					a string representing the name of the reservoir (ex BM for Blue Mesa)
    :param record_type:                 string, type of statemod run (historical, baseline or climate)
    :param realization:                 float, the realization number (put 10000 for hist)
	
	:returns monthly_means:				a  numpy array of mean reservoir levels across the 105 year record
	'''
	#print(abbrev + '/' + res_name + '_S' + str(hmm) + '_' + str(realization) + '_xre_data.csv')
	if os.path.getsize('ReservoirResults/' + abbrev + '/' + res_name + '_S' + str(hmm) + '_' + str(realization) + '_xre_data_withdemand.csv')>2000:
		if are_first_two_rows_same('ReservoirResults/' + abbrev + '/' + res_name + '_S' + str(hmm) + '_' + str(realization) + '_xre_data_withdemand.csv'):
			xre_data = pd.read_csv('ReservoirResults/' + abbrev + '/' + res_name + '_S' + str(hmm) + '_' + str(realization) + '_xre_data_withdemand.csv', index_col=False, skiprows=1)
		else:
			xre_data = pd.read_csv('ReservoirResults/' + abbrev + '/' + res_name + '_S' + str(hmm) + '_' + str(realization) + '_xre_data_withdemand.csv', index_col=False)
		account_0 = xre_data[(xre_data['ACC']=='0') | (xre_data['ACC']==0)]
		account_0 = account_0[account_0['MO'] != 'TOT']

		monthly_array = account_0['Init. Storage'].to_numpy()

		monthly_array1 = [int(j) for j in monthly_array]
		plt.plot(monthly_array1)
		res_percentiles = np.zeros(99)
		
		for i, p in enumerate(range(1,100,1)):
			res_percentiles[i] = np.percentile(monthly_array1, p)

		return res_percentiles
	else:
		return np.zeros(99)

realization_percentiles = np.zeros([99,20000])#500 realizations

#'5104055'for granby (UC) #BM blue mesa 6203532 (gunnison), Mcphee MR 7103614 (sanjuan)
abbrev = 'gm'
res_name = 'BM'
record_type = 'AdjustedClimate_05'
ind=0
for hmm in range(100):#1000
	print(hmm)
	for r in range(1):#20
	#if r not in [13, 17, 74, 110, 111, 116, 145, 162, 203, 208, 224, 225, 267, 288, 346, 459, 483, 492, 563, 588, 664, 713, 727, 843, 845, 917, 974]:
		realization_percentiles[:,ind] = extract_res_percentiles(abbrev, res_name, record_type, hmm, r)
		ind = ind+1
plt.show()
# np.savetxt(res_name + '_realizationPercentiles_1_to_99_withdemand.csv', realization_percentiles, delimiter=',')