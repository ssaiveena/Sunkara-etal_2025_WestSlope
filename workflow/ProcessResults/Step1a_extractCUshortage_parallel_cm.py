import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from mpi4py import MPI
import math
#os.chdir('C:/Users/dgold/Dropbox/Postdoc/IM3/Colorado/InternalVariabilityPaper/code/final_data_analysis')
#%%
def extract_shortage_info_new(abbrev, hmm, realization, record_type, exports, exportNodes):
    """
    Optimized function to extract shortage information from Parquet files.
    """

    # Construct Parquet file path
    if record_type != 'historical':
        pq_path = f'../{abbrev}2015B_S{hmm}_{realization}.parquet'
        if not os.path.exists(pq_path):
            return np.zeros(105)  # Avoid unnecessary computation
    else:
        pq_path = f'Results/{abbrev}/{record_type}/parquet/{abbrev}2015B.parquet'

    # Read Parquet file using PyArrow for speed
    pq_file = pd.read_parquet(pq_path, engine='pyarrow')

    # Keep export structures using vectorized filtering
    if exports and exportNodes:
        pq_file = pq_file[pq_file['structure_id'].isin(exportNodes)]

    # Extract only the annual totals
    pq_tot = pq_file.query("month == 'TOT'")

    # Pivot table to get yearly shortage per structure
    pq_tot.loc[:,'year'] = pq_tot['year'].astype(str)  # Ensure year is string
    pq_tot.loc[:, 'shortage_cu'] = pd.to_numeric(pq_tot['shortage_cu'], errors='coerce')

    # shortage_data = pq_tot.pivot(index='year', columns='structure_id', values='shortage_cu').fillna(0)
    shortage_data = pq_tot.pivot_table(
    index='year',
    columns='structure_id',
    values='shortage_cu',
    aggfunc='sum',  # or 'mean', 'first', etc. depending on your needs
    )

    # shortage_data = pq_tot.pivot(index='year', columns='structure_id', values='shortage_cu').fillna(0)
    # Compute total basin shortage across all structures
    total_basin_shortage = shortage_data.sum(axis=1).values

    return total_basin_shortage

all_struct = np.genfromtxt('All_cm.txt',dtype='str').tolist()
'''parallel code'''
nSamples = len(all_struct)
# Begin parallel simulation
comm = MPI.COMM_WORLD

# Get the number of processors and the rank of processors
rank = comm.rank
nprocs = comm.size

# Determine the chunk which each processor will neeed to do
count = int(math.floor(nSamples/nprocs))
remainder = nSamples % nprocs

# Use the processor rank to determine the chunk of work each processor will do
if rank < remainder:
    start = rank*(count+1)
    stop = start + count + 1
else:
    start = remainder*(count+1) + (rank-remainder)*count
    stop = start + count

# =============================================================================
# Loop though all SOWs
# # =============================================================================
for k in range(start, stop):
    ind = 0
    uc_baseline = np.zeros([105,20000])
    for hmm in range(1000):#realizations
        for r in range(20):
            uc_baseline[:,ind] = extract_shortage_info_new('cm',hmm,  r, 'baseline', True, [all_struct[k]])
            ind=ind+1
    np.savetxt('UpperColorado/updated_demand_%s.csv' %all_struct[k], uc_baseline, delimiter=',')

