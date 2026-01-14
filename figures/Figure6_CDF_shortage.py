import numpy as np
import matplotlib
from matplotlib import pyplot as plt
# plt.switch_backend('agg')
import matplotlib.patches
from scipy import stats
import itertools
import sys
import matplotlib.font_manager as font_manager
plt.ioff()

font = font_manager.FontProperties(style='normal', size=16)

all_IDs = ['cm', 'gm', 'wm', 'ym', 'sj']
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

def shortage_duration(sequence):
    cnt_shrt = [sequence[i]>0 for i in range(len(sequence))] # Returns a list of True values when there's a shortage
    shrt_dur = [ sum( 1 for _ in group ) for key, group in itertools.groupby( cnt_shrt ) if key ] # Counts groups of True values
    return shrt_dur
  
def plotSDC(ax1, synthetic, histData):
    #n = 12
    # #Reshape historic data to a [no. years x no. months] matrix
    # f_hist = np.reshape(histData, (int(np.size(histData)/n), n))
    # #Reshape to annual totals
    # f_hist_totals = np.sum(f_hist,1)  
    # #Calculate historical shortage duration curves
    F_hist = np.sort(histData) # for inverse sorting add this at the end [::-1]
    
    # #Reshape synthetic data
    # #Create matrix of [no. years x no. months x no. samples]
    # synthetic_global = np.zeros([int(np.size(histData)/n),n,samples*realizations]) 
    # # Loop through every SOW and reshape to [no. years x no. months]
    # for j in range(samples*realizations):
    #     synthetic_global[:,:,j]= np.reshape(synthetic[:,j], (int(np.size(synthetic[:,j])/n), n))
    # #Reshape to annual totals
    # synthetic_global_totals = np.sum(synthetic_global,1)
    # print(np.shape(synthetic_global_totals))
    
    p=np.arange(100,-10,-20)

    #Calculate synthetic shortage duration curves
    F_syn = np.empty([int(np.size(histData)),samples*realizations])
    F_syn[:] = np.NaN
    for j in range(samples*realizations):
        F_syn[:,j] = np.sort(synthetic[:,j])
    
    # For each percentile of magnitude, calculate the percentile among the experiments ran
    perc_scores = np.zeros_like(F_syn) 
    for m in range(int(np.size(histData))):
        perc_scores[m,:] = [stats.percentileofscore(F_syn[m,:], j, 'rank') for j in F_syn[m,:]]
                
    P = np.arange(1.,len(F_hist)+1)*100 / len(F_hist)
    
    ylimit = round(np.max(F_syn))
    # ax1
    handles = []
    labels=[]
    color = '#000292'
    for i in range(len(p)):
        ax1.fill_between(P, np.min(F_syn[:,:],1), np.percentile(F_syn[:,:], p[i], axis=1), color=color, alpha = 0.2)
        ax1.plot(P, np.percentile(F_syn[:,:], p[i], axis=1), linewidth=0.5, color=color, alpha = 0.5)
        if i ==3 or i==4:
            print(np.percentile(F_syn[:,:], p[i], axis=1))
        handle = matplotlib.patches.Rectangle((0,0),1,1, color=color, alpha=alpha(i, base=0.1))
        handles.append(handle)
        label = "{:.0f} %".format(100-p[i])
        labels.append(label)
    ax1.plot(P,F_hist, c='black', linewidth=2.5, label='Historical record')
    ax1.set_ylim(0,ylimit)
    ax1.set_xlim(0,100)
    #ax1.legend(handles=handles, labels=labels, framealpha=1, fontsize=8, loc='upper left', title='Frequency in experiment',ncol=2)
    ax1.set_xlabel('Shortage magnitude percentile',fontsize=16)
    ax1.set_ylabel('Annual shortage (Million $m^3$)',fontsize=16)
    handles1, labels1 = ax1.get_legend_handles_labels()
    return handles, labels
#Figure in metric units
'''Basinwide shortage'''
fig, axes = plt.subplots(2,3)
for s in range(2):#5
    ax = axes.flat[s]
    histData = np.loadtxt('Shortage/' +  all_IDs[s] + '_shortage_hist.csv', delimiter=',')*1233.4818/1000000
    synthetic = np.zeros([len(histData), samples*realizations])
    synthetic = np.loadtxt('Shortage/' +  all_IDs[s] + '_shortage_withdemand.csv', delimiter=',')*1233.4818/1000000
    # print(np.sort(histData))
    handles1, labels1 = plotSDC(ax, synthetic, histData)

axes.flat[5].axis('off')  # hide axes
axes.flat[5].legend(handles=handles1, labels= labels1, ncols=1, fontsize=16)

fig.set_size_inches([20,10])
fig.savefig('cdf_shortage.svg')
fig.savefig('cdf_shortage.png')
exit()

'''explanation plots June 20'''
synthetic = np.loadtxt('Shortage/' +  all_IDs[4] + '_shortage_withdemand.csv', delimiter=',') *1233.4818/1000000
# plt.plot(synthetic[:,2220], color='grey')
# plt.plot(synthetic[:,13160], color='grey')
plt.plot(synthetic[:,1000], color='grey')
plt.plot(synthetic[:,5000], color='grey')
plt.plot(synthetic[:,8500], color='grey')

plt.show()
F_syn = np.empty([int(105),1000*20])

for j in range(1000*20):
    F_syn[:,j] = np.sort(synthetic[:,j])
print(np.percentile(F_syn[:,:], 100, axis=1))
row_max = np.max(F_syn, axis=1)  # same as np.percentile(F_syn, 100, axis=1)

# Step 2: Get column index (j) for each row where max occurs
# If multiple max values exist in a row, this gets the *first* one
j_indices = np.argmax(F_syn, axis=1)

# Optional: show result
for i in range(len(row_max)):
    print(f"Row {i}: max = {row_max[i]}, found at column j = {j_indices[i]}")

'''district wise CDF plots'''
exit()
ym_districts = ['57','56']
gm_districts = ['41','42']
sj_districts = ['77','63']
cm_districts = ['36','72']
wm_districts = ['43']
all_IDs = cm_districts +  gm_districts+ ym_districts+sj_districts

fig, axes = plt.subplots(4,2)
for s in range(len(all_IDs)):
    district = all_IDs[s]
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
    ax = axes.flat[s]
    histData = np.loadtxt(region + '/district' + all_IDs[s] + '_hist.csv', delimiter=',')#[:,2]#*1233.4818/1000000
    synthetic = np.zeros([len(histData), samples*realizations])
    synthetic = np.loadtxt(region + '/district' + all_IDs[s] + '_withdemand.csv', delimiter=',') 
    handles1, labels1 = plotSDC(ax, synthetic, histData[0,:])

# axes.flat[5].axis('off')  # hide axes
# axes.flat[5].legend(handles=handles1, labels= labels1, ncols=1, fontsize=12)
plt.show()
# fig.set_size_inches([20,10])
# fig.savefig('cdf_shortage.svg')
# fig.savefig('cdf_shortage.png')
exit()
'''Identifying Hist to plot veritcal lines'''
years=np.arange(100)#[27,40] #median and 2002
colors = ["#E5E059","#EF767A"]
n=12
import scipy.stats

yr_per = lambda x, array: int(np.round(scipy.stats.percentileofscore(array, array[x], kind='mean'), decimals=0)) 

def percentiles(ID):
    HIS_short = np.loadtxt('Shortage/' +  all_IDs[s] + '_shortage_hist.csv', delimiter=',')*1233.4818/1000000    
    # Identify percentile for 2002 annual shortage
    markers=[yr_per(x,HIS_short) for x in years]
    print(markers[50])
    print(np.median(HIS_short))
    return markers

fig, axes = plt.subplots(2,3)
for s in range(len(axes.flat)-1):
    ax = axes.flat[s]
    markers = percentiles(all_IDs[s])
    # print(markers.index(50))
    # print(markers.index(100))
    for m in range(2):#len(markers)
        ax.axvline(x=markers[m], linewidth=3, linestyle='--', color=colors[m])
    ax.set_xlim(0,100)
plt.show()