import numpy as np
import matplotlib
from matplotlib import pyplot as plt
plt.switch_backend('TKagg')
import matplotlib.patches
from scipy import stats
import pandas as pd
import math
#import os
from mpi4py import MPI
import sys
from scipy.signal import savgol_filter
from matplotlib.backends.backend_pdf import PdfPages

plt.ioff()

# Longform parameter names to use in figure legend
parameter_names_long = ['Changes in expected dry flow', 
                        'Dry flow variability', 'Changes in expected wet flow', 
                        'Wet flow variability', 'Annual dry year persistence', 
                        'Annual wet year persistence','Snowmelt shift','Irrigation demand','Industrial demand','Municipal demand','Interaction']#,

percentiles = np.arange(0,100)
samples = 1000
realizations = 20
idx = np.arange(2,22,2)

def alpha(i, base=0.2):
    l = lambda x: x+base-x*base
    ar = [l(0)]
    for j in range(i):
        ar.append(l(ar[-1]))
    return ar[-1]
  
def plotSDC(structure_name,ax1, region, basin_code):    
    p=np.arange(100,-10,-10)
    '''
    Sensitivity analysis plots normalized to 0-100
    '''
    if region =='UpperColorado':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Colorado','Industrial_Colorado','Municipal_Colorado']
    elif region =='Gunnison':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Gunnison','Industrial_Gunnison','Municipal_Gunnison']
    elif region =='White':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_White','Industrial_White','Municipal_White']
    elif region =='Yampa':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Yampa','Industrial_Yampa','Municipal_Yampa']
    elif region =='SanJuan':
        param_names=['XBM_mu0','XBM_sigma0', 'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11','snowmelt_shift','Irrigation_Southwest','Industrial_Southwest','Municipal_Southwest']

    sensitive_output = 'Magnitude'
    delta_values = pd.read_csv(sensitive_output+'_Sensitivity_analysis/'+ structure_name + '_' + basin_code + '_DELTA_withdemand.csv')
    delta_conf = pd.read_csv(sensitive_output+'_Sensitivity_analysis/'+ structure_name + '_' + basin_code +'_DELTA_conf_withdemand.csv')
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
    yaxistitles = ["Relative distribution shift explained [%]","Variance explained","Variance explained"]
    k = 0
    smoothed_stack = np.array([savgol_filter(row, window_length=11, polyorder=2) for row in values_to_plot])
    ax1.stackplot(np.arange(0,100), *smoothed_stack, colors = color_list, labels=parameter_names_long)
    ax1.set_ylim(0,100)
    ax1.set_xlim(0,100)
    ax1.tick_params(axis='x', labelsize=12)
    ax1.tick_params(axis='y', labelsize=12)
    ax1.set_ylabel(yaxistitles[k], fontsize=16)

    if region =='SanJuan':
        region='Southwest'
    ax1.set_xlabel('Shortage magnitude percentile', fontsize=16)
    if structure_name =='mun':
        ax1.set_title('a) Municipal' + ' in ' + region, fontsize=16)
    elif structure_name =='ind':
        ax1.set_title('b) Industrial' + ' in ' + region, fontsize=16)
    else:
        ax1.set_title('c) Irrigation' + ' in ' + region, fontsize=16)

    handles1, labels1 = ax1.get_legend_handles_labels()
    # ax1.legend(handles=handles1, labels= parameter_names_long, ncols=1,loc='right', fontsize=12,bbox_to_anchor=(1.55, 0.5))
    return handles1, labels1

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

'''Plotting all sectors into pdf'''
# Open a single multi-page PDF
# with PdfPages('all_sectors_combined.pdf') as pdf:
#     for i in range(15):
#         sector, basin_code, basin_name = combos[i]
#         fig, ax = plt.subplots()   # create a new figure and axis for each plot
#         plotSDC(sector, ax, basin_name, basin_code)     # your custom plot function
        
#         pdf.savefig(fig, bbox_inches='tight')            # save the current figure into the PDF
#         plt.close(fig)              # close the figure to free up memory

'''Plottong selected sectors'''
fig, axes = plt.subplots(2,2, figsize=(10,8))
axis= axes.flatten()

sector, basin_code, basin_name = combos[12]
plotSDC(sector, axis[0], basin_name, basin_code)     # your custom plot function
sector, basin_code, basin_name = combos[13]
plotSDC(sector, axis[1], basin_name, basin_code)     # your custom plot function
sector, basin_code, basin_name = combos[14]
plotSDC(sector, axis[2], basin_name, basin_code)     # your custom plot function

handles1, labels1 = axis[2].get_legend_handles_labels()
axis[3].axis('off')  # hide axes
axis[3].legend(handles=handles1, labels= parameter_names_long, ncols=1, fontsize=12)
plt.tight_layout(w_pad=0.25,h_pad=0.35)

plt.savefig('sector.pdf')            # save the current figure into the PDF
