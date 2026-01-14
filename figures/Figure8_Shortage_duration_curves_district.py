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

# plt.ioff()

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
  
def plotSDC(structure_name,ax1, region, label):    
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
    delta_values = pd.read_csv(sensitive_output+'_Sensitivity_analysis/'+ structure_name + '_DELTA_withdemand.csv')
    delta_conf = pd.read_csv(sensitive_output+'_Sensitivity_analysis/'+ structure_name + '_DELTA_conf_withdemand.csv')
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
                # if p<10:
                #     print(param,p)
    delta_values=delta_values.drop(['Controlvariable'])
    for p in percentiles:           
        total = np.sum(delta_values[str(p)])
        if total!=0:
            for param in param_names:
                    value = 100*delta_values.at[param,str(p)]/total
                    delta_values.at[param,str(p)] = value
                    # delta_values.set_value(param,str(p),value)
    delta_values_to_plot = delta_values.values.tolist()
    # print([[row[i] for i in range(10)] for row in delta_values_to_plot])
    color_list = ["#8C510A", "#DFC27D", "#01665E", "#80CDC1", "#FDE0EF", "#B2ABD2", "#9F9F9F", "#FD8D3C", "#3182BD", "#31A354"]  
                  
    values_to_plot = [delta_values_to_plot]
    titles = ["Delta","S1","R2"]
    yaxistitles = ["Relative distribution shift explained [%]","Variance explained","Variance explained"]
    k = 0
    
    smoothed_stack = np.array([savgol_filter(row, window_length=11, polyorder=2) for row in values_to_plot])
    ax1.stackplot(np.arange(0,100), *smoothed_stack, colors = color_list, labels=parameter_names_long)
    
    # ax1.stackplot(np.arange(0,100), *np.array(values_to_plot), colors = color_list, labels=parameter_names_long)
    
    ax1.set_ylim(0,100)
    ax1.set_xlim(0,100)

    # ax1.set_ylabel(yaxistitles[k], fontsize=16)
    # ax1.set_xlabel('Shortage magnitude percentile', fontsize=16)
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # ax1.legend(handles=handles1, labels= parameter_names_long, ncols=1,loc='right', fontsize=12,bbox_to_anchor=(1.55, 0.5))
    # ax1.set_title( label + 'District ' + structure_name + ' in ' + region, fontsize=15)

    #following for selected districts
    if district =='57' or district =='62' or district =='36' or district=='41' or district=='77':
        ax1.tick_params(axis='y', labelsize=12)
        ax1.set_ylabel(yaxistitles[k], fontsize=15)
    else:
        ax1.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    
    if district =='63' or district=='29' or district=='77':
        ax1.tick_params(axis='x', labelsize=12)
        ax1.set_xlabel('Shortage magnitude percentile', fontsize=15)
    else:
        ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    if region=='SanJuan':
        region = 'Southwest'
    ax1.set_title( label + 'District ' + structure_name + ' in ' + region, fontsize=15)
    plt.suptitle('Senior rights              Junior rights', fontsize=18)
    handles1, labels1 = ax1.get_legend_handles_labels()

    return handles1, labels1
# fig, ax = plt.subplots()
# plotSDC('56', ax, 'Yampa','a')
# plt.show()
# exit()
'''Plot all districts into a pdf'''
# ym_districts = ['55','44','56','57','58','54']
# gm_districts = ['42','40','41','59','62','68','28']
# sj_districts = ['73','63','61','60','69','71','32','33','34','30','31','78','46','29','77']
# cm_districts = ['72','70','39','45','38','53','37','36','51','50','52']
# wm_districts = ['43']
# all_IDs = ym_districts  + gm_districts+ sj_districts+cm_districts

# # Open a single multi-page PDF
# with PdfPages('all_districts_combined.pdf') as pdf:
#     for i in range(len(all_IDs)):
#         district = all_IDs[i]
#         if district in ym_districts:
#             region = 'Yampa'
#         elif district in gm_districts:
#             region = 'Gunnison'
#         elif district in sj_districts:
#             region = 'SanJuan'
#         elif district in wm_districts:
#             region = 'White'
#         elif district in cm_districts:
#             region = 'UpperColorado'
#         fig, ax = plt.subplots()   # create a new figure and axis for each plot
#         plotSDC(district, ax, region,'a')     # your custom plot function
        
#         pdf.savefig(fig, bbox_inches='tight')            # save the current figure into the PDF
#         plt.close(fig)              # close the figure to free up memory
# exit()
'''Plot for selected districts in a single figure'''
ym_districts = ['57','56']
gm_districts = ['41','42']
sj_districts = ['77','63']
cm_districts = ['36','72']
wm_districts = ['43']
all_IDs = cm_districts +  gm_districts+ ym_districts+sj_districts
fig, ax = plt.subplots(figsize=(8,12))   # create a new figure and axis for each plot
fig.delaxes(ax)                          # remove it immediately

gs  = fig.add_gridspec(5, 2)        # 5 rows × 2 columns
# or  fig.delaxes(a)
axs = []    
for r in range(4):           
    axs.append([fig.add_subplot(gs[r, 0]),
                fig.add_subplot(gs[r, 1])])

ax_last = fig.add_subplot(gs[4, :])  # row 4, “:”  ➜ span both columns
axs.append([ax_last])                # optional bookkeeping
# axes=axs.ravel()
from itertools import chain
axis = list(chain.from_iterable(axs))
label_names = ['a)','b)','c)','d)','e)','f)','g)','h)']
for i in range(len(all_IDs)):
    district = all_IDs[i]
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

    plotSDC(district, axis[i], region, label_names[i])     # your custom plot function
handles1, labels1 = axis[i].get_legend_handles_labels()
axis[8].axis('off')  # hide axes
axis[8].legend(handles=handles1, labels= parameter_names_long, ncols=2, fontsize=14)
plt.tight_layout(w_pad=0.04,h_pad=0.3)
# plt.show()
plt.savefig('district.pdf')            # save the current figure into the PDF
    