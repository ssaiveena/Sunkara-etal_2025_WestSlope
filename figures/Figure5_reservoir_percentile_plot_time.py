import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
# Simulate data: 1000 samples × 12 months
# data = pd.read_csv('MR_reservoir_data.csv', header=None)
hist_data_BM = [643708, 625675, 644753, 651045, 658441, 655836, 668791, 699288, 730085,
 866954, 863012, 858392]
hist_data_GB = [511951, 501355, 493073, 473892, 449751, 423026, 400883, 395979, 444877,
 519073, 534870, 524172]
hist_data_MR = [292146, 285729, 283883, 281465, 279111, 278967, 280322, 310537, 379400,
 372520, 335815, 303490]


# pd.DataFrame(data1).to_csv('MR_reservoir_data_relative_month.csv', header=False, index=False)

def plot_reservoir_data(ax, data1, res_name, data_hist1):
    # Choose fine-grained percentile steps (e.g. every 5%)
    percentile_steps = np.arange(0, 101, 1)
    percentile_data = np.percentile(data1, q=percentile_steps, axis=0).transpose()  # shape: (n_percentiles, 12)
    # Setup plot
    months = np.arange(12)

    # Colormap setup
    cmap = cm.viridis_r
    norm = mcolors.Normalize(vmin=0, vmax=100)

    # Shade between each adjacent pair of percentiles
    for i in range(len(percentile_steps) - 1):
        lower = percentile_data[:,i]
        upper = percentile_data[:,i + 1]
        mid_percentile = (percentile_steps[i] + percentile_steps[i + 1]) / 2
        color = cmap(norm(mid_percentile))
        ax.fill_between(months, lower, upper, color=color,alpha=0.9, linewidth=0,zorder=4)

    # plot for historical data
    # Choose fine-grained percentile steps (e.g. every 5%)
    # percentile_data_hist = np.percentile(data_hist1, q=percentile_steps, axis=0).transpose()  # shape: (n_percentiles, 12)
    # # Colormap setup
    # cmap = cm.Greys
    # norm = mcolors.Normalize(vmin=0, vmax=100)

    # # Shade between each adjacent pair of percentiles
    # for i in range(len(percentile_steps) - 1):
    #     lower = percentile_data_hist[:,i]
    #     upper = percentile_data_hist[:,i + 1]
    #     mid_percentile = (percentile_steps[i] + percentile_steps[i + 1]) / 2
    #     color = cmap(norm(mid_percentile))
    #     ax.fill_between(months, lower, upper, color=color, alpha=0.7)

    median = np.percentile(data_hist1, 50, axis=0).transpose()
    ax.plot(months, median, color='black', linewidth=2)
    median = np.percentile(data_hist1, 25, axis=0).transpose()
    ax.plot(months, median, color='black', linewidth=2, linestyle='--')
    median = np.percentile(data_hist1, 75, axis=0).transpose()
    ax.plot(months, median, color='black', linewidth=2, linestyle='-.')

    # Customize plot
    # ax.set_xticks(months)
    # ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    #                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=10, rotation=45)
    ax.set_xticks(np.arange(0,12,3))
    ax.set_xticklabels(['Jan',  'Apr', 'Jul',  'Oct'], fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel(res_name+ ' [%]', fontsize=12)
    ax.grid(False)

'''plot with colormap'''
fig, axes = plt.subplots(3,1, figsize=(4,7))
ax= axes.flatten()
data = pd.read_csv('BM_reservoir_data.csv', header=None)
data1 = (data-hist_data_BM)*100/1160000

data_hist = pd.read_csv('BM_reservoir_data_hist.csv', header=None)
data_hist1 = (data_hist.transpose()-hist_data_BM)*100/1160000
plot_reservoir_data(ax[0],data1, 'Blue Mesa', data_hist1)

data = pd.read_csv('GB_reservoir_data.csv', header=None)
data1 = (data-hist_data_GB)*100/665000

data_hist = pd.read_csv('GB_reservoir_data_hist.csv', header=None)
data_hist1 = (data_hist.transpose()-hist_data_GB)*100/665000
plot_reservoir_data(ax[1],data1, 'Granby', data_hist1)

data = pd.read_csv('MR_reservoir_data.csv', header=None)
data1 = (data-hist_data_MR)*100/469000
data_hist = pd.read_csv('MR_reservoir_data_hist.csv', header=None)
data_hist1 = (data_hist.transpose()-hist_data_MR)*100/469000
plot_reservoir_data(ax[2],data1, 'McPhee', data_hist1)

# Suppose this is your norm and colormap setup
norm = plt.Normalize(vmin=0, vmax=100)
cmap = cm.viridis_r  # or your colormap

# Create the ScalarMappable and colorbar
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Needed for matplotlib >=3.1 to prevent warnings

# Choose your empty subplot (e.g., ax[5] if 6 subplots total)
cbar = fig.colorbar(sm, ax=axes, orientation='horizontal',ticks=np.arange(0, 101, 20),fraction=0.05, pad=0.15)
cbar.set_label('Percentile', fontsize=10, labelpad=2)
fig.subplots_adjust(bottom=0.1)  # make room for the legend
# fig.suptitle('Change in storage from historical median')

# plt.tight_layout()
plt.show()
exit()
'''Plot Violin data'''
# data = pd.read_csv('BM_reservoir_data.csv', header=None)
# data1 = (data-hist_data_BM)*100/1160000
# print(np.shape(data1))
# # Step 2: Melt the data into long format for seaborn
# melted_data = data1.melt(var_name="Variable", value_name="Value")
# print(melted_data)
# # Step 3: Plot violin plot
# plt.figure(figsize=(12, 6))
# sns.violinplot(x="Variable", y="Value", data=melted_data, inner="box", palette="Set3")

# plt.title("Distribution of 12 Variables (Each with 1000 Points)")
# plt.xlabel("Variable (1–12)")
# plt.ylabel("Value")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

'''Plot shaded plot with 5th and 95th percentile values data'''
#the following is for the supplementary plot
fig, axes = plt.subplots(1,3, figsize=(7,4))
axis= axes.flatten()

ax=axis[0]
data = pd.read_csv('BM_reservoir_data.csv', header=None)
data1 = (data-hist_data_BM)*100/1160000
p05, p95 = np.percentile(data1, [5, 95], axis=0)
mid      = np.median(data1,        axis=0)  # or mean
x = np.arange(12)                         # 0 … 11
ax.fill_between(x, p05, p95,
                facecolor='grey',
                alpha=0.25,
                label='5th–95th percentile')

ax.plot(x, mid, color='black', lw=2, label='median')

# cosmetics
ax.set_xticks([1,4,7,10])
ax.set_xticklabels(['Jan','Apr','Jul','Oct'])   # or your real labels
ax.set_ylabel('Percentage change')
ax.set_title('Blue Mesa')
ax.legend(frameon=False)

ax=axis[1]
data = pd.read_csv('GB_reservoir_data.csv', header=None)
data1 = (data-hist_data_GB)*100/665000
p05, p95 = np.percentile(data1, [5, 95], axis=0)
mid      = np.median(data1,        axis=0)  # or mean
x = np.arange(12)                         # 0 … 11
ax.fill_between(x, p05, p95,
                facecolor='grey',
                alpha=0.25,
                label='5th–95th percentile')

ax.plot(x, mid, color='black', lw=2, label='median')

# cosmetics
ax.set_xticks([1,4,7,10])
ax.set_xticklabels(['Jan','Apr','Jul','Oct'])   # or your real labels
ax.set_ylabel('Percentage change')
ax.set_title('Granby')
ax.legend(frameon=False)

ax=axis[2]
data = pd.read_csv('MR_reservoir_data.csv', header=None)
data1 = (data-hist_data_MR)*100/469000
p05, p95 = np.percentile(data1, [5, 95], axis=0)
mid      = np.median(data1,        axis=0)  # or mean
x = np.arange(12)                         # 0 … 11
ax.fill_between(x, p05, p95,
                facecolor='grey',
                alpha=0.25,
                label='5th–95th percentile')

ax.plot(x, mid, color='black', lw=2, label='median')

# cosmetics
ax.set_xticks([1,4,7,10])
ax.set_xticklabels(['Jan','Apr','Jul','Oct'])   # or your real labels
ax.set_ylabel('Percentage change')
ax.set_title('McPhee')
ax.legend(frameon=False)
plt.tight_layout()
plt.show()