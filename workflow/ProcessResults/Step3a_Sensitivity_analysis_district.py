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

def sensitivity_analysis_per_structure(ID, basin):
    #change the basin name at the beginning and the end
    if basin == 'UpperColorado':
        basin1 = 'cm'
    elif basin =='Yampa':
        basin1 = 'ym'
    elif basin=='White':
        basin1 = 'wm'
    elif basin == 'SanJuan':
        basin1 = 'sj'
    else:
        basin1 = 'gm'
    LHsamples = np.loadtxt('LHsamples_' + basin1 + '.txt')
    # LHsamples = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/LHS_samples/LHsamples_100_Trial.txt') 
    param_bounds=np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_' + basin1 + '.txt', usecols=(1,2))
    # param_bounds=np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt', usecols=(1,2))
    param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_' + basin1 + '.txt').readlines()]+['Controlvariable']
    # param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt').readlines()]+['Controlvariable']
    # Add dummy control variable
    LHsamples = np.concatenate((LHsamples, np.random.rand(1000,1)), axis=1)
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
    '''
    Perform analysis for shortage magnitude
    '''
    DELTA = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    DELTA_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    S1 = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    S1_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    R2_scores = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    DELTA.index=DELTA_conf.index=S1.index=S1_conf.index = R2_scores.index = param_names
    SYN_short = np.zeros([len(HIS_short), samples * realizations])

    # data= np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Results/SanJuan/updated_month_nodemand_2900718.csv', delimiter=',') 
    data= np.loadtxt(basin + '/district' + ID + '_withdemand.csv', delimiter=',') 
    #Gunnison, Yampa, White, Colorado, SanJuan
    # try:
    #     SYN_short = copy.deepcopy(data)
    # except IndexError:
    #     print('error')
    # # Reshape into water years
    # # Create matrix of [no. years x no. months x no. experiments]
    # f_SYN_short = np.zeros([int(np.size(HIS_short)/n),n, samples*realizations])
    # for i in range(samples*realizations):
    #     f_SYN_short[:,:,i]= np.reshape(SYN_short[:,i], (int(np.size(SYN_short[:,i])/n), n))

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
                output = np.mean(syn_magnitude[i,:].reshape(-1, 20),axis=1) #change reshape based on number of samples
                # output = np.percentile(syn_magnitude[i, :].reshape(-1, 20), 75, axis=1)
                
                #changes np.mean to np.max for worst shortage
                output = output[rows_to_keep]
                result= delta.analyze(problem, LHsamples, output, print_to_console=False, num_resamples=10)
                DELTA[percentiles[i]]= result['delta']
                DELTA_conf[percentiles[i]] = result['delta_conf']
                S1[percentiles[i]]=result['S1']
                S1_conf[percentiles[i]]=result['S1_conf']
            except:
                pass

    S1.to_csv('Magnitude_Sensitivity_analysis/'+ ID + '_S1_withdemand.csv')
    S1_conf.to_csv('Magnitude_Sensitivity_analysis/'+ ID + '_S1_conf_withdemand.csv')
    DELTA.to_csv('Magnitude_Sensitivity_analysis/'+ ID + '_DELTA_withdemand.csv')
    DELTA_conf.to_csv('Magnitude_Sensitivity_analysis/'+ ID + '_DELTA_conf_withdemand.csv')

# =============================================================================
# Start parallelization (running each structure in parallel)
# =============================================================================
# for i in range(len(all_IDs)):
ym_districts = ['55','44','56','57','58','54']
gm_districts = ['42','40','41','59','62','68','28']
sj_districts = ['73','63','61','60','69','71','32','33','34','30','31','78','46','29','77']
cm_districts = ['72','70','39','45','38','53','37','36','51','50','52']
wm_districts = ['43']
# for ind in sj_districts:
#     print(ind)
#     sensitivity_analysis_per_structure(ind, 'SanJuan')
# for ind in ym_districts:
#     print(ind)
#     sensitivity_analysis_per_structure(ind, 'Yampa')
# for ind in gm_districts:
#     print(ind)
#     sensitivity_analysis_per_structure(ind, 'Gunnison')
# for ind in cm_districts:
#     print(ind)
#     sensitivity_analysis_per_structure(ind, 'UpperColorado')
# for ind in wm_districts:
#     print(ind)
#     sensitivity_analysis_per_structure(ind, 'White')
nStructures = 39
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

all_IDs = ym_districts +  gm_districts+ sj_districts+cm_districts
# Run simulation
for k in range(start, stop):
    district = all_IDs[k]
    if district in ym_districts:
        region = 'Yampa'
    elif district in gm_districts:
        region = 'Gunnison'
    elif district in sj_districts:
        region = 'SanJuan'
    elif district in wm_districts:
        region = 'White'
    elif district in cm_districts:
        region = 'UpperColorado'
    sensitivity_analysis_per_structure(district, region)