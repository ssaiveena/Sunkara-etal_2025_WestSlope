import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
'''reading data'''
# read in historical data
cm_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/cm/baseline/cm_hist_outflow.csv', delimiter=',')*1233.48/1000000
gm_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/gm/baseline/gm_hist_outflow.csv', delimiter=',')*1233.48/1000000
ym_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/ym/baseline/ym_hist_outflow.csv', delimiter=',')*1233.48/1000000
wm_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/wm/baseline/wm_hist_outflow.csv', delimiter=',')*1233.48/1000000
sj_hist = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Figures/figureData/sj/baseline/sj_hist_outflow.csv', delimiter=',')*1233.48/1000000

# print(np.tile(cm_hist, (20, 1)).flatten())

#%% correct cm
cm_gm = np.loadtxt('/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/Results/cm_gm_mod_hist_outflow.csv', delimiter=',')*1233.48/1000000

cm_corrected = cm_hist - cm_gm
#%%
total_hist = cm_corrected + gm_hist + ym_hist + wm_hist + sj_hist

# read in baseline data
cm_baseline = np.loadtxt('Results/cm_mod_climate_outflow_demand.csv', delimiter=',')*1233.48/1000000
gm_baseline = np.loadtxt('Results/gm_mod_climate_outflow_demand.csv', delimiter=',')*1233.48/1000000
ym_baseline = np.loadtxt('Results/ym_mod_climate_outflow_demand.csv', delimiter=',')*1233.48/1000000
wm_baseline = np.loadtxt('Results/wm_mod_climate_outflow_demand.csv', delimiter=',')*1233.48/1000000
sj_baseline = np.loadtxt('Results/sj_mod_climate_outflow_demand.csv', delimiter=',')*1233.48/1000000

#%%
cm_gm_baseline = np.loadtxt('Results/cm_gm_mod_climate_outflow_demand.csv', delimiter=',')*1233.48/1000000

cm_corrected_baseline = cm_baseline - cm_gm_baseline
#%%
total_baseline = cm_corrected_baseline.flatten() + gm_baseline.flatten() + ym_baseline.flatten() + wm_baseline.flatten() +\
				 sj_baseline.flatten()

df = pd.DataFrame({'Y':total_baseline,\
 'cm': cm_corrected_baseline.flatten(), \
 'gm': gm_baseline.flatten(), \
 'ym': ym_baseline.flatten(),\
  'wm': wm_baseline.flatten(),\
   'sj': sj_baseline.flatten()})

df_hist = pd.DataFrame({'Y':total_hist,\
 'cm': cm_corrected, \
 'gm': gm_hist, \
 'ym': ym_hist,\
  'wm': wm_hist,\
   'sj': sj_hist})
columns = ['cm', 'gm', 'ym', 'wm', 'sj']
labels = ['Upper Colorado','Gunnison','Yampa','White','Southwest']
positions1 = range(1, len(columns)*2, 2)  # [1, 3, 5, 7, 9]
positions2 = range(2, len(columns)*2+1, 2)  # [2, 4, 6, 8, 10]

'''new paper figure kde plots for total outflows with changes to historical 10th, median percentile'''
plt.rcParams.update({'font.size': 16})  # set default font size for everything

fig, axes = plt.subplots(1, 1, figsize=(10, 6), sharey=True)

col='Y'

ind=0
# Offset each KDE vertically to simulate "positions"
data = df[col].dropna()  # Drop NaNs for KDE
sns.kdeplot(np.median(data.values.reshape(105,20000),axis=0)-np.median(df_hist[col]), vertical=True, legend='Relative median outflows', bw_adjust=0.5,ax=axes)
print(np.percentile(np.percentile(data.values.reshape(105,20000),50,axis=0),70))
print(np.percentile(df_hist[col],50))
print(np.percentile(data.values.reshape(105,20000),10,axis=0))

print(np.sum(np.median(data.values.reshape(105,20000),axis=0)-np.median(df_hist[col])<0))

sns.kdeplot(np.percentile(data.values.reshape(105,20000),5,axis=0)-np.percentile(df_hist[col],5), vertical=True, legend='Relative 5th percentile outflows', bw_adjust=0.5,ax=axes)
# sns.kdeplot(np.percentile(data.values.reshape(105,20000),95,axis=0)-np.percentile(df_hist[col],95), vertical=True, legend='Relative 95th percentile outflows', bw_adjust=0.5,ax=axes)

axes.set_ylim([-6500,7000])
axes.set_xlabel('Density')
# axes.set_title(labels[ind])
axes.set_ylabel('Cumulative outflows relative\n to baseline [Million m$^3$]', fontsize=16)
# Note: vertical KDEs simulate boxplot positions but don't align perfectly
plt.legend(['Relative Median Outflows', 'Relative 5th Percentile Outflows'])

plt.show()

'''4b - Vertical KDE’s for changes relative to baseline median and baseline worst 10%ile outflows 4c'''
plt.rcParams.update({'font.size': 16})  # set default font size for everything

fig, axes = plt.subplots(1, 5, figsize=(10, 6), sharey=True)

ind=0
# Plot KDEs for each column at shifted x positions (like the 'positions' argument)
for col, pos in zip(columns, positions1):
	 # Offset each KDE vertically to simulate "positions"
	data = df[col].dropna()  # Drop NaNs for KDE

	print(min(np.median(data.values.reshape(105,20000),axis=0)-np.median(df_hist[col])))
	sns.kdeplot(np.median(data.values.reshape(105,20000),axis=0)-np.median(df_hist[col]), vertical=True, label=labels[ind], bw_adjust=0.5,ax=axes[ind])
	# sns.kdeplot(np.percentile(data.values.reshape(105,20000),10,axis=0)-np.percentile(df_hist[col],10), vertical=True, label=labels[ind], bw_adjust=0.5,ax=axes[ind])
	axes[ind].set_ylim([-1200,1200])
	# sns.kdeplot(df_hist[col], vertical=True, label=labels[ind], bw_adjust=0.5,ax=axes[ind])
	axes[ind].set_xlabel('')
	axes[ind].set_title(labels[ind])
	if ind==0:
		axes[ind].set_ylabel('Outflows relative to \nbaseline median [Million m$^3$]')
	 # Note: vertical KDEs simulate boxplot positions but don't align perfectly
	ind=ind+1
# plt.legend(['Relative to Baseline Median', 'Relative to Worst 10th Percentile'])
plt.show()

'''saving anova data across time without outliers'''
save_anova =[]
# df = pd.read_csv('your_data.csv')
for hmm in range(105):#1000
	df = pd.DataFrame({'Y':total_baseline[[hmm + 105 * i for i in range(0, 20000)]]-np.median(total_hist),\
	 'cm': cm_corrected_baseline.flatten()[[hmm + 105 * i for i in range(0, 20000)]]-np.median(cm_corrected), \
	 'gm': gm_baseline.flatten()[[hmm + 105 * i for i in range(0, 20000)]]-np.median(gm_hist), \
	 'ym': ym_baseline.flatten()[[hmm + 105 * i for i in range(0, 20000)]]-np.median(ym_hist),\
	  'wm': wm_baseline.flatten()[[hmm + 105 * i for i in range(0, 20000)]]-np.median(wm_hist),\
	   'sj': sj_baseline.flatten()[[hmm + 105 * i for i in range(0, 20000)]]-np.median(sj_hist)})

	# Step 2: Detect outliers using IQR for each column
	outlier_mask = pd.DataFrame(False, index=df.index, columns=df.columns)

	for col in df.columns:
		Q1 = df[col].quantile(0.25)
		Q3 = df[col].quantile(0.75)
		IQR = Q3 - Q1
		lower_bound = Q1 - 1.5 * IQR
		upper_bound = Q3 + 1.5 * IQR
		outlier_mask[col] = (df[col] < lower_bound) | (df[col] > upper_bound)

	# Step 3: Combine masks to find any-row with an outlier in any variable
	any_outlier = outlier_mask.any(axis=1)

	# Step 4: Get clean data and indices of outliers
	outlier_indices = df.index[any_outlier].tolist()
	clean_df = df[~any_outlier]  # rows with no outliers in any column

	# Fit linear model
	model = ols('Y ~ cm + gm + ym + wm + sj', data=clean_df).fit()

	# Perform ANOVA
	anova_table = sm.stats.anova_lm(model, typ=2)
	
	# print(anova_table['PR(>F)'].apply(lambda x: f"{x:.10f}"))

	anova_table['Variance_Proportion'] = anova_table['sum_sq'] / anova_table['sum_sq'].sum()
	# save_anova.append(anova_table['Variance_Proportion'])

	save_anova.append(anova_table['F'])
# print(np.median(save_anova['F']))
df = pd.concat(save_anova, axis=1).transpose()
print(df.median())
# import pickle

'''Plotting 4b'''
with open('save_anova_time_median.pkl', 'rb') as f:
    save_anova = pickle.load(f)

print(len(save_anova))

df = pd.concat(save_anova, axis=1).transpose()
print(df.median())
# Convert to DataFrame and drop 'Residual'
df = pd.Series(df.median())
df_filtered = df.drop("Residual")

# Plotting the pie chart
plt.figure(figsize=(8, 6))
plt.pie(df_filtered, labels=['Upper Colorado','Gunnison','Yampa','White','Southwest'], autopct='%1.1f%%', startangle=140,colors = ['#BC6C25','#DDA15E','#FEFAE0','#283618','#606C38'])
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
plt.show()

import matplotlib.pyplot as plt

labels = ['Upper Colorado','Gunnison','Yampa','White','Southwest']
values = [9.427540e32, 6.925734e32, 3.402385e32, 2.622225e31, 3.060171e33]

plt.figure(figsize=(10,5))
plt.bar(labels, values)
plt.ylabel("F-statistic", fontsize=20)
plt.xlabel("West Slope basin", fontsize=20)
# plt.title("F-statistic by Group")
plt.xticks(rotation=45)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.tight_layout()
plt.show()

