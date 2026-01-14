from mpi4py import MPI
import math
import numpy as np
from string import Template
import os
import pandas as pd
import sys

# function to get unique values
def unique(list1):
    unique_list = pd.Series(list1).drop_duplicates().tolist()
    for x in unique_list:
        print(x)

'''Extract irrigation structures'''
structure_id = []
# split data on periods (splitting on spaces/tabs doesn't work because some columns are next to each other)
with open('Statemod_files/cm2015B.iwr','r') as f: #downlaod statemod files from website
    for line in f:
    # Process the line (e.g., split and extract values)
        parts = line.split()
        structure_id.append(parts[1] if len(parts) > 1 else None)
    #all_split_data_DDM = [x.split(' ') for x in f.readlines()]       
f.close() 
structure_id = pd.Series(structure_id).drop_duplicates().tolist()

# Path to the file
file_path = 'irrigation_cm.txt'

# Open the file for writing
with open(file_path, 'w') as file:
    # Write each element of the list to the file
    for item in structure_id:
        file.write("%s\n" % item)
#delete manually first few lines

'''Extract Mun and Ind structures'''
#extracted manually from ddm files under M_I demands section for cm
#for gm based on , constant=0.00, max(400)
# no details under step10 for M_I deamnds