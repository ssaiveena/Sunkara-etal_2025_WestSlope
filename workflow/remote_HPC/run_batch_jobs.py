import os
import numpy as np
import sys

# read in run information
'''
BASIN_NAME:   the statemod code for the current basin. All names have "2015" in them. For example "sj2015" is san juan/dolores
RUN_TYPE:     either "baseline_run" or "climate_change"
START_REL:    the number of the realizatation to run first
NUM_RELS:     the total number of realizations to be run by this core 
SOW:          the SOW index for which ensemble this is (baseline is 1)
'''

BASIN_NAME = sys.argv[1]
RUN_TYPE = sys.argv[2]
START_REL = sys.argv[3]
NUM_RELS = sys.argv[4]
SOW = sys.argv[5]


projectdirectory = '/scratch/dfg42/statemod_training/cdss-app-statemod-fortran/src/main/fortran/' + BASIN_NAME + '_StateMod_modified/' + BASIN_NAME + '_StateMod_modified/StateMod/' + RUN_TYPE + '/'

realizations = np.arange(int(START_REL), int(START_REL)+ int(NUM_RELS))

for j in realizations:
	scenario = 'S' + str(j) + '_' + SOW
	os.chdir(projectdirectory + 'scenarios/' + scenario)
	os.system('./statemod-17.0.3-gfortran-lin-64bit-o3 {}B_{} -simulate'.format(BASIN_NAME, scenario))