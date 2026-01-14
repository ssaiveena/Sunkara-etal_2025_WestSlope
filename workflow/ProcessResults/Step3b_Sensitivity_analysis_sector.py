import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats
import matplotlib.pyplot as plt
import math
import sys
from mpi4py import MPI
import copy
sys.path.append('../')
from SALib.analyze import delta
plt.ioff()


def fitOLS(dta, predictors):
    # concatenate intercept column of 1s
    dta['Intercept'] = np.ones(np.shape(dta)[0])
    # get columns of predictors
    cols = dta.columns.tolist()[-1:] + predictors
    #fit OLS regression
    ols = sm.OLS(dta['Shortage'], dta[cols])
    result = ols.fit()
    return result

def sensitivity_analysis_per_structure(ID, basin, basin_name):
    '''
    Perform analysis for shortage magnitude
    '''

    #change the basin name at the beginning and the end for wo demand

    LHsamples = np.loadtxt('LHsamples_' + basin + '.txt')
    # LHsamples = np.loadtxt('LHsamples_wodemand.txt')
    np.random.seed(42)  # Set seed for reproducibility
    # Add dummy control variable
    LHsamples = np.concatenate((LHsamples, np.random.rand(1000,1)), axis=1)
    param_bounds=np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_' + basin + '.txt', usecols=(1,2))
    # param_bounds=np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt', usecols=(1,2))
    # Add dummy control variable bounds
    param_bounds = np.concatenate((param_bounds, [[0,1]]))

    # SOW_values = np.array([1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) #Default parameter values for base SOW
    samples = len(LHsamples[:,0])

    realizations = 20
    params_no = len(LHsamples[0,:])

    rows_to_keep = list(np.arange(1000))
    # for i in range(params_no):
    #     within_rows = np.intersect1d(np.where(LHsamples[:,i] > param_bounds[i][0])[0], np.where(LHsamples[:,i] < param_bounds[i][1])[0])
    #     rows_to_keep = np.intersect1d(rows_to_keep,within_rows)
    LHsamples = LHsamples[rows_to_keep,:]

    param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_' + basin + '.txt').readlines()]+['Controlvariable']
    # param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt').readlines()]+['Controlvariable']

    print(param_names)
    problem = {
        'num_vars': params_no,
        'names': param_names,
        'bounds': param_bounds.tolist()
    }
    percentiles = np.arange(0,100)
    # deal with fact that calling result.summary() in statsmodels.api
    # calls scipy.stats.chisqprob, which no longer exists
    scipy.stats.chisqprob = lambda chisq, df: scipy.stats.chi2.sf(chisq, df)

    #==============================================================================
    # Function for water years
    #==============================================================================
    empty=[]
    n=12
    HIS_short = np.loadtxt('7202003_info_0.txt')[:,2]

    DELTA = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    DELTA_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    S1 = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    S1_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    R2_scores = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    DELTA.index=DELTA_conf.index=S1.index=S1_conf.index = R2_scores.index = param_names
    SYN_short = np.zeros([len(HIS_short), samples * realizations])

    # data= np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Results/SanJuan/updated_month_nodemand_2900718.csv', delimiter=',') 
    data= np.loadtxt(basin_name + '/' + ID + '_withdemand.csv', delimiter=',') 
    

    # Shortage per water year
    f_SYN_short_WY = copy.deepcopy(data)#np.sum(f_SYN_short,axis=1)

    # Identify droughts at percentiles
    syn_magnitude = np.zeros([len(percentiles),samples*realizations])
    for j in range(samples*realizations):
        syn_magnitude[:,j]=[np.percentile(f_SYN_short_WY[:,j], i) for i in percentiles]

    # Delta Method analysis
    for i in range(len(percentiles)):
        if syn_magnitude[i,:].any():
            try:
                output = np.mean(syn_magnitude[i,:].reshape(-1, 20), axis=1) #change reshape based on number of samples
                # output = np.percentile(syn_magnitude[i, :].reshape(-1, 20), 95, axis=1)
                output = output[rows_to_keep]
                result= delta.analyze(problem, LHsamples, output, print_to_console=False, num_resamples=10)
                DELTA[percentiles[i]]= result['delta']
                DELTA_conf[percentiles[i]] = result['delta_conf']
                S1[percentiles[i]]=result['S1']
                S1_conf[percentiles[i]]=result['S1_conf']
            except:
                pass

    S1.to_csv('Magnitude_Sensitivity_analysis/'+ ID + '_'+ basin+ '_S1_withdemand.csv')
    S1_conf.to_csv('Magnitude_Sensitivity_analysis/'+ ID +'_'+ basin+  '_S1_conf_withdemand.csv')
    DELTA.to_csv('Magnitude_Sensitivity_analysis/'+ ID +'_'+ basin+  '_DELTA_withdemand.csv')
    DELTA_conf.to_csv('Magnitude_Sensitivity_analysis/'+ ID +'_'+ basin+  '_DELTA_conf_withdemand.csv')

# =============================================================================
# Start parallelization (running each structure in parallel)
# =============================================================================
nStructures = 15
# Begin parallel simulation
comm = MPI.COMM_WORLD

# Get the number of processors and the rank of processors
rank = comm.rank
nprocs = comm.size

# Determine the chunk which each processor will neeed to do
count = int(math.floor(nStructures/nprocs))
remainder = nStructures % nprocs

# Use the processor rank to determine the chunk of work each processor will do
if rank < remainder:
    start = rank*(count+1)
    stop = start + count + 1
else:
    start = remainder*(count+1) + (rank-remainder)*count
    stop = start + count

combos = [
    ('mun', 'cm', 'UpperColorado'),
    ('ind', 'cm', 'UpperColorado'),
    ('irrigation', 'cm', 'UpperColorado'),
    
    ('mun', 'gm', 'Gunnison'),
    ('ind', 'gm', 'Gunnison'),
    ('irrigation', 'gm', 'Gunnison'),
    
    ('mun', 'wm', 'White'),
    ('ind', 'wm', 'White'),
    ('irrigation', 'wm', 'White'),
    
    ('mun', 'ym', 'Yampa'),
    ('ind', 'ym', 'Yampa'),
    ('irrigation', 'ym', 'Yampa'),
    
    ('mun', 'sj', 'SanJuan'),
    ('ind', 'sj', 'SanJuan'),
    ('irrigation', 'sj', 'SanJuan'),
]
for k in range(start, stop):
    sector, basin_code, basin_name = combos[k]
    sensitivity_analysis_per_structure(sector, basin_code, basin_name)

