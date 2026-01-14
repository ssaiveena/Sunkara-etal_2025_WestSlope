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

# LHsamples = np.loadtxt('LHsamples_sj.txt')
# np.random.seed(42)  # Set seed for reproducibility
# # Add dummy control variable
# LHsamples = np.concatenate((LHsamples, np.random.rand(1000,1)), axis=1)
# param_bounds=np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_sj.txt', usecols=(1,2))
# # param_bounds=np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt', usecols=(1,2))
# # Add dummy control variable bounds
# param_bounds = np.concatenate((param_bounds, [[0,1]]))

# # SOW_values = np.array([1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) #Default parameter values for base SOW
# samples = len(LHsamples[:,0])

# realizations = 20
# params_no = len(LHsamples[0,:])

# rows_to_keep = list(np.arange(1000))
# LHsamples = LHsamples[rows_to_keep,:]

# param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_sj.txt').readlines()]+['Controlvariable']
# # param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt').readlines()]+['Controlvariable']

# print(param_names)
# problem = {
#     'num_vars': params_no,
#     'names': param_names,
#     'bounds': param_bounds.tolist()
# }
# print(problem)
# percentiles = np.arange(0,99)

# # deal with fact that calling result.summary() in statsmodels.api
# # calls scipy.stats.chisqprob, which no longer exists
# scipy.stats.chisqprob = lambda chisq, df: scipy.stats.chi2.sf(chisq, df)

# #==============================================================================
# # Function for water years
# #==============================================================================
# empty=[]
# n=12

# def sensitivity_analysis_reservoir(res_abbrev):
#     '''
#     Perform analysis for shortage magnitude
#     '''
#     DELTA = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
#     DELTA_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
#     S1 = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
#     S1_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
#     DELTA.index=DELTA_conf.index=S1.index=S1_conf.index  = param_names
#     SYN_short = np.zeros([1, samples * realizations])

#     # data= np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Results/SanJuan/updated_month_nodemand_2900718.csv', delimiter=',') 
#     data= np.loadtxt(res_abbrev + '_realizationPercentiles_1_to_99_withdemand.csv',delimiter=',')

#     # Shortage per water year
#     f_SYN_short_WY = copy.deepcopy(data)#change index based on duration of failures#first 20k with demand and last 20k without demand

#     # Delta Method analysis
#     # Delta Method analysis
#     for i in range(len(percentiles)):
#         if f_SYN_short_WY[i,:].any():
#             try:
#                 # output = np.mean(syn_magnitude[i,:].reshape(-1, 20), axis=1) #change reshape based on number of samples
#                 output = np.percentile(f_SYN_short_WY[i, :].reshape(-1, 20), 50, axis=1)
#                 output = output[rows_to_keep]
#                 result= delta.analyze(problem, LHsamples, output, print_to_console=False, num_resamples=10)
#                 DELTA[percentiles[i]]= result['delta']
#                 DELTA_conf[percentiles[i]] = result['delta_conf']
#                 S1[percentiles[i]]=result['S1']
#                 S1_conf[percentiles[i]]=result['S1_conf']
#             except:
#                 pass

#     S1.to_csv('Magnitude_Sensitivity_analysis/'+ res_abbrev + '_S1_withdemand_75.csv')
#     S1_conf.to_csv('Magnitude_Sensitivity_analysis/'+ res_abbrev + '_S1_conf_withdemand_75.csv')
#     DELTA.to_csv('Magnitude_Sensitivity_analysis/'+ res_abbrev + '_DELTA_withdemand_75.csv')
#     DELTA_conf.to_csv('Magnitude_Sensitivity_analysis/'+ res_abbrev + '_DELTA_conf_withdemand_75.csv')

# # sensitivity_analysis_reservoir('MR')

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Original data
# df = pd.read_csv('Magnitude_Sensitivity_analysis/GB_DELTA_withdemand_75.csv', index_col=0)

# # Determine the top 3 for each column
# top3_info = {}
# for col in df.columns:
#     # Sort descending and take top 3
#     top = df[col].nlargest(3)
#     # Store list of (variable, value) tuples in order: 1st,2nd,3rd
#     top3_info[col] = list(zip(top.index.tolist(), top.values.tolist()))

# # Prepare data for stacked bars
# ranks = ['1st dominant', '2nd dominant', '3rd dominant']
# columns = df.columns.tolist()

# # For each rank, collect values per column and corresponding variable
# stack_data = []
# stack_vars = []
# for r in range(3):
#     vals = [top3_info[col][r][1] for col in columns]
#     vars_ = [top3_info[col][r][0] for col in columns]
#     stack_data.append(vals)
#     stack_vars.append(vars_)

# # Setup colors for each variable (unique)
# unique_vars = sorted({var for row in stack_vars for var in row})
# cmap = plt.cm.get_cmap('tab20', len(unique_vars))
# color_dict = {var: cmap(i) for i, var in enumerate(unique_vars)}

# # Plot
# fig, ax = plt.subplots(figsize=(8, 5))
# y_pos = np.arange(len(ranks))

# # Bottom offsets
# bottom = np.zeros(len(ranks))

# # For each column, plot a segment for each rank
# for col_idx, col in enumerate(columns):
#     # For each rank, get variable and value from that column
#     vals = [stack_data[r][col_idx] for r in range(3)]
#     vars_ = [stack_vars[r][col_idx] for r in range(3)]
#     # Plot segments for this column across ranks
#     for r in range(3):
#         vals[r] = 0.1#this is to have fixed width
#         ax.barh(r, vals[r], left=bottom[r], color=color_dict[vars_[r]], edgecolor='white', height=0.5)
#         bottom[r] += vals[r]

# # Legend
# handles = [plt.Rectangle((0,0),1,1, color=color_dict[var]) for var in unique_vars]
# ax.legend(handles, unique_vars, bbox_to_anchor=(1.05, 1), loc='upper left', title='Variable')

# # Labels
# ax.set_yticks(y_pos)
# ax.set_yticklabels(ranks, fontsize=12)
# ax.set_xticks([0,5,9.9])
# ax.set_xticklabels(['1st', '50th', '99th'], fontsize=12)
# ax.set_xlabel('Ensemble Percentile', fontsize=12)
# # ax.set_title('Stacked Bars of Top-3 Values per Column\nSegments colored by variable')
# plt.tight_layout()
# plt.show()

'''For relative values saved from reservoir_percentile_plot_time code for monthly values; finding important factors at everymotnh
and plotting as stacked plot'''

def sensitivity_analysis_reservoir(res_abbrev,basin):
    '''
    Perform analysis for shortage magnitude
    '''
    LHsamples = np.loadtxt('LHsamples_' + basin + '.txt')
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
    LHsamples = LHsamples[rows_to_keep,:]

    param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param_demand_' + basin + '.txt').readlines()]+['Controlvariable']
    # param_names=[x.split(' ')[0] for x in open('/home/fs02/pmr82_0001/ss4285/West_Slope_Training/Gold-etal_2023_EarthsFuture/workflow/SyntheticRecordGeneration/uncertain_param.txt').readlines()]+['Controlvariable']

    print(param_names)
    problem = {
        'num_vars': params_no,
        'names': param_names,
        'bounds': param_bounds.tolist()
    }
    print(problem)
    percentiles = np.arange(0,12)#number of months

    # deal with fact that calling result.summary() in statsmodels.api
    # calls scipy.stats.chisqprob, which no longer exists
    scipy.stats.chisqprob = lambda chisq, df: scipy.stats.chi2.sf(chisq, df)

    #==============================================================================
    # Function for water years
    #==============================================================================
    empty=[]
    n=12

    DELTA = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    DELTA_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    S1 = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    S1_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
    DELTA.index=DELTA_conf.index=S1.index=S1_conf.index  = param_names
    SYN_short = np.zeros([1, samples * realizations])

    # data= np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Results/SanJuan/updated_month_nodemand_2900718.csv', delimiter=',') 
    data= np.loadtxt(res_abbrev + '_reservoir_data_relative_month.csv',delimiter=',')

    # Shortage per water year
    f_SYN_short_WY = copy.deepcopy(data)#change index based on duration of failures#first 20k with demand and last 20k without demand

    # Delta Method analysis
    # Delta Method analysis
    for i in range(len(percentiles)):
        if f_SYN_short_WY[i,:].any():
            try:
                # output = np.mean(syn_magnitude[i,:].reshape(-1, 20), axis=1) #change reshape based on number of samples
                output = f_SYN_short_WY[:, i]
                output = output[rows_to_keep]
                result= delta.analyze(problem, LHsamples, output, print_to_console=False, num_resamples=10)
                DELTA[percentiles[i]]= result['delta']
                DELTA_conf[percentiles[i]] = result['delta_conf']
                S1[percentiles[i]]=result['S1']
                S1_conf[percentiles[i]]=result['S1_conf']
            except:
                pass

    S1.to_csv('Reservoir_Sensitivity_analysis/'+ res_abbrev + '_S1.csv')
    S1_conf.to_csv('Reservoir_Sensitivity_analysis/'+ res_abbrev + '_S1_conf.csv')
    DELTA.to_csv('Reservoir_Sensitivity_analysis/'+ res_abbrev + '_DELTA.csv')
    DELTA_conf.to_csv('Reservoir_Sensitivity_analysis/'+ res_abbrev + '_DELTA_conf.csv')

# sensitivity_analysis_reservoir('BM','gm')
# sensitivity_analysis_reservoir('GB','cm')
# sensitivity_analysis_reservoir('MR','sj')

parameter_names_long = ['Changes in expected dry flow', 
                        'Dry flow variability', 'Changes in expected wet flow', 
                        'Wet flow variability', 'Annual dry year persistence', 
                        'Annual wet year persistence','Snowmelt shift','Irrigation','Industrial','Municipal','Interaction']#,
percentiles = np.arange(0,12)

def alpha(i, base=0.2):
    l = lambda x: x+base-x*base
    ar = [l(0)]
    for j in range(i):
        ar.append(l(ar[-1]))
    return ar[-1]
  
def plotSDC(structure_name, ax1):    
    '''
    Sensitivity analysis plots normalized to 0-100
    '''
    if structure_name =='GB':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Colorado','Industrial_Colorado','Municipal_Colorado']
    elif structure_name =='BM':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Gunnison','Industrial_Gunnison','Municipal_Gunnison']
    elif structure_name =='wm':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_White','Industrial_White','Municipal_White']
    elif structure_name =='ym':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Yampa','Industrial_Yampa','Municipal_Yampa']
    elif structure_name =='MR':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Southwest','Industrial_Southwest','Municipal_Southwest']

    sensitive_output = 'Reservoir'
    delta_values = pd.read_csv(sensitive_output+'_Sensitivity_analysis/'+ structure_name + '_DELTA.csv')
    delta_conf = pd.read_csv(sensitive_output+'_Sensitivity_analysis/'+ structure_name + '_DELTA_conf.csv')
    delta_values.set_index(list(delta_values)[0],inplace=True)
    delta_conf.set_index(list(delta_conf)[0],inplace=True)
    delta_values = delta_values.clip(lower=0)
    for p in percentiles:
        # Check if their CI overlaps zero or if are lower than the dummy
        for param in param_names:
            if delta_values.at[param,str(p)]<delta_conf.at[param,str(p)] or \
            delta_values.at[param,str(p)]<=delta_values.at['Controlvariable',str(p)]:
                # If yes, set the index value to zero
                delta_values.at[param,str(p)] = 0
    delta_values=delta_values.drop(['Controlvariable'])
    for p in percentiles:           
        total = np.sum(delta_values[str(p)])
        if total!=0:
            for param in param_names:
                    value = 100*delta_values.at[param,str(p)]/total
                    delta_values.at[param,str(p)] = value
                    # delta_values.set_value(param,str(p),value)
    delta_values_to_plot = delta_values.values.tolist()
    
    color_list = ["#8C510A", "#DFC27D", "#01665E", "#80CDC1", "#FDE0EF", "#B2ABD2", "#9F9F9F", "#FD8D3C", "#3182BD", "#31A354"]
    values_to_plot = [delta_values_to_plot]
    titles = ["Delta","S1","R2"]
    yaxistitles = ["Change explained","Variance explained","Variance explained"]
    from scipy.signal import savgol_filter

# Example: smooth each row (each category) in your stack data
# Assume `stack_data` is a 2D NumPy array with shape (n_categories, n_points)
    smoothed_stack = np.array([savgol_filter(row, window_length=11, polyorder=2) for row in values_to_plot])
    for k in range(1):
        ax1.stackplot(np.arange(0,12), *smoothed_stack, colors = color_list)#values_to_plot[k]
        # ax1.set_title(structure_name)
        # ax1.set_ylim(0,100)
        # ax1.set_xlim(0,100)
        handles, labels = ax1.get_legend_handles_labels()
        ax1.tick_params(axis='x', labelsize=12)
        ax1.tick_params(axis='y', labelsize=12)
        if structure_name == 'GB':
            ax1.set_ylabel('Relative distribution shift explained [%]', fontsize=14)
        # else:
        #     ax1.tick_params(axis="y", label1On=False)   # or labelleft=False before Matplotlib 3.8
        ax1.set_xticks(np.arange(0,12,3))
        ax1.set_xticklabels(['Jan',  'Apr', 
                        'Jul',  'Oct'], fontsize=12)
        ax1.set_xlabel('Month', fontsize=14)
    return handles, labels

# plotSDC('cm')
# all_IDs = ['cm','gm','wm','ym','sj']
# for i in range(len(all_IDs)):
fig, axes = plt.subplots(3,1, figsize=(4,8))
ax= axes.flatten()
plotSDC('BM',ax[0])
plotSDC('GB',ax[1])
handles, labels =plotSDC('MR',ax[2])
fig.legend(handles, labels = parameter_names_long, fontsize=9, loc='lower center',bbox_to_anchor=(0.5, -0.01), ncols=2)

fig.tight_layout()
fig.subplots_adjust(bottom=0.2)  # make room for the legend
plt.show()
# fig.savefig(sensitive_output+'_Sensitivity_analysis/' + structure_name + '_'+titles[k]+'_wodemand.svg')
# fig.savefig('Reservoir_Sensitivity_analysis/Res.png')