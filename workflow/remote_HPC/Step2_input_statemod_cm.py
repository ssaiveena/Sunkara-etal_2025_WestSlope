from mpi4py import MPI
import math
import numpy as np
from string import Template
import os
import pandas as pd
import sys
import shutil

#download all statemod files from https://cdss.colorado.gov/modeling-data/surface-water-statemod
#this code is for preparing input files for statemod simulation

file_name_suffix = range(10)    
file = "Statemod_files/cm2015B.iwr"
destination_prefix = "Experiment_files/"
# for i in file_name_suffix:
#    file_destination = destination_prefix + 'gm2015B_S' + str(i+1) + "_1.iwr"
#    shutil.copyfile(file, file_destination)

# =============================================================================
# Experiment set up
# =============================================================================
# Read in SOW parameters
LHsamples = np.loadtxt('../SyntheticRecordGeneration/' + 'LHsamples_1000.txt') 
nSamples = len(LHsamples[:,0])
realizations = 1

# Read/define relevant structures for each uncertainty
irrigation = np.genfromtxt('irrigation_cm.txt',dtype='str').tolist()
mun_ind = np.genfromtxt('MI_cm.txt',dtype='str').tolist()
transbasin = np.genfromtxt('TBD_cm.txt',dtype='str').tolist()

# =============================================================================
# Load global information (applicable to all SOW)
# =============================================================================
# For RSP
T = open('Statemod_files/cm2015B_template.rsp', 'r')
template_RSP = Template(T.read())

# For DDM
# split data on periods (splitting on spaces/tabs doesn't work because some columns are next to each other)
with open('Statemod_files/cm2015B.ddm','r') as f:
    all_split_data_DDM = [x.split('.') for x in f.readlines()]       
f.close()        
# get unsplit data to rewrite firstLine # of rows
with open('Statemod_files/cm2015B.ddm','r') as f:
    all_data_DDM = [x for x in f.readlines()]       
f.close() 
# Get historical irrigation rata 
with open('Statemod_files/cm2015B.iwr','r') as f:
    hist_IWR = [x.split() for x in f.readlines()[463:]]       #change this    #463 for cm, 377 for sj, 202 for wm, 620 for gm, 370 for ym 
f.close() 

max_values = pd.read_csv('Statemod_files/max_val_cm.csv', index_col=0)#change
max_values.index = max_values.index.map(str)

# =============================================================================
# Define functions that generate each type of input file 
# =============================================================================

# Function for DDM files
def writenewDDM(structures, firstLine, k, l):    
    allstructures = []
    for m in range(len(structures)):
        allstructures.extend(structures[m])
    with open('Experiment_files/cm2015B_S'+ str(k+1) + '_' + str(l+1) + '.iwr') as f:
        sample_IWR = [x.split() for x in f.readlines()[463:]]  #change this    #463 for cm, 377 for sj, 202 for wm, 620 for gm, 370 for ym 
    f.close() 
    new_data = []
    irrigation_encounters = np.zeros(len(structures[0]))
    for i in range(len(all_split_data_DDM)-firstLine):
        row_data = []
        # To store the change between historical and sample irrigation demand (12 months + Total)
        change = np.zeros(13) 
        # Split first 3 columns of row on space
        # This is because the first month is lumped together with the year and the ID when spliting on periods
        row_data.extend(all_split_data_DDM[i+firstLine][0].split())
        # If the structure is not in the ones we care about then do nothing
        if row_data[1] in structures[0]: #If the structure is irrigation            
            line_in_iwr = int(irrigation_encounters[structures[0].index(row_data[1])]*len(structures[0]) + structures[0].index(row_data[1]))
            irrigation_encounters[structures[0].index(row_data[1])]=+1
            for m in range(len(change)):
                change[m]= float(sample_IWR[line_in_iwr][2+m])-float(hist_IWR[line_in_iwr][2+m]) 
            # apply change to 1st month
            row_data[2] = str(max(0, int(float(row_data[2])+change[0])))
            # apply multipliers to rest of the columns
            for j in range(len(all_split_data_DDM[i+firstLine])-2):
                row_data.append(str(max(0, int(float(all_split_data_DDM[i+firstLine][j+1])+change[j+1]))))
            #print(row_data)
        elif row_data[1] in structures[1]: #If the structure is transbasin (to uncurtail)   
            # apply multiplier to 1st month
            row_data[2] = str(int(max_values.loc[row_data[1]][0]*LHsamples[k,1]))
            # apply multipliers to rest of the columns
            for j in range(1,13):
                row_data.append(str(int(max_values.loc[row_data[1]][j]*LHsamples[k,1]))) 
        elif row_data[1] in structures[2]: #If the structure is mun_ind 
            # apply multiplier to 1st month
            row_data[2] = str(int(float(row_data[2])*LHsamples[k,2]))
            # apply multipliers to rest of the columns
            for j in range(len(all_split_data_DDM[i+firstLine])-2):
                row_data.append(str(int(float(all_split_data_DDM[i+firstLine][j+1])*LHsamples[k,2])))  
        elif row_data[1] not in allstructures:
            for j in range(len(all_split_data_DDM[i+firstLine])-2):
                row_data.append(str(int(float(all_split_data_DDM[i+firstLine][j+1]))))                      
        # append row of adjusted data
        new_data.append(row_data)                
    # write new data to file
    f = open('Experiment_files/'+ 'cm2015B.ddm'[0:-4] + '_S' + str(k+1) + '_' + str(l+1) + 'cm2015B.ddm'[-4::],'w')
    # write firstLine # of rows as in initial file
    for i in range(firstLine):
        f.write(all_data_DDM[i])            
    for i in range(len(new_data)):
        # write year, ID and first month of adjusted data
        f.write(new_data[i][0] + ' ' + new_data[i][1] + (19-len(new_data[i][1])-len(new_data[i][2]))*' ' + new_data[i][2] + '.')
        # write all but last month of adjusted data
        for j in range(len(new_data[i])-4):
            f.write((7-len(new_data[i][j+3]))*' ' + new_data[i][j+3] + '.')                
        # write last month of adjusted data
        f.write((9-len(new_data[i][-1]))*' ' + new_data[i][-1] + '.' + '\n')            
    f.close()
    
    return None

# =============================================================================
# Start parallelization
# =============================================================================
    
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
   for j in range(realizations): 
       d = {}
       d['IWR'] = 'cm2015B_S' + str(k+1) + '_' + str(j+1) + '.iwr'
       d['DDM'] = 'cm2015B_S' + str(k+1) + '_' + str(j+1) + '.ddm'
       S1 = template_RSP.safe_substitute(d)
       f1 = open('Experiment_files/cm2015B_S' + str(k+1) + '_' + str(j+1) + '.rsp', 'w')
       f1.write(S1)    
       f1.close()
       writenewDDM([irrigation, transbasin, mun_ind], 779, k, j) #558 for sj, 494 for ym, 264 for wm, 684 for gm, 779 for cm

# LHS_number = 10


# name='San_Juan'
# abbrev='ym'
# nSites=165
# nIWRSites=296
# startXBM=16
# startIWR=377
# xbm_file='../../historical_data/'+abbrev+'2015_StateMod/StateMod/ym2015x.xbm'
# xbm_out='../../Adjusted_stateMod_input_files/.xbm/baseline/SanJuan_Dolores/'
# abbrev_file_xbm='ym2015x.xbm'
# last_node = -1
# historical_column=4

# for r in tqdm(range(0, LHS_number)):
#     writenewDDM(abbrev, nSites, startXBM, xbm_file, xbm_out, abbrev_file_xbm, last_node, historical_column, r)


# os.chdir("../"+design+"/Experiment_files")
# for k in range(6, stop): #start
#     for j in range(realizations): 
#         if os.path.getsize("cm2015B_S{}_{}.xdd".format(k+1,j+1))>>20 <500:
#             os.system("./statemod cm2015B_S{}_{} -simulate".format(k+1,j+1))
