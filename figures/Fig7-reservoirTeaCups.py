import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm

def find_x_coords(yvalues):
    '''
    returns x coordinates for teacup plot

    :param yvalues:         numpy array of reservoir levels
    :return:
        x1:                 array of right side of teacup
        x2:                 array of left side of teacup
    '''

    x1 =  np.zeros(len(yvalues))
    x2 = np.zeros(len(yvalues))

    for i in range(len(yvalues)):
        x1[i] = (max(yvalues) - yvalues[i])/2
        x2[i] = 1.5 * max(yvalues) + yvalues[i]/2

    return x1, x2


def make_teacups(res_abbrev, hist_median, crit):
    '''
    Plots teacup diagrams for a reservoir for both baseline and climate ensemble

    :param res_abbrev:                      str, abbrev of res name (BM, MP or LG)
    :param crit:                            float, low storage level to plot as a benchmark
    '''

    baseline_rels = np.loadtxt('figureData/reservoir/' + res_abbrev + '_realizationPercentiles_baseline_run_1_to_99.csv',
                               delimiter=',')
    baseline_means = np.mean(baseline_rels, axis=1)/10000

    climate_rels = np.loadtxt('figureData/reservoir/' + res_abbrev + '_realizationPercentiles_AdjustedClimate_05_1_to_99.csv',
                              delimiter=',')
    climate_means = np.mean(climate_rels, axis=1)/10000

    # to plot to the top of the reservoir, make sure the max of the climate means array is the same as the baseline
    if climate_means[-1] < baseline_means[-1]:
        climate_means[-1] = baseline_means[-1]

    # add zeros to each array
    baseline_means = np.hstack([np.zeros(1), baseline_means])
    climate_means = np.hstack([np.zeros(1), climate_means])

    baseline_x1, baseline_x2 = find_x_coords(baseline_means)
    climate_x1, climate_x2 = find_x_coords(climate_means)


    # copy the baseline means and set them as the historical, then add the historical median to the middle entry
    # This overly complicated method of adding the historical median is done to make plotting the teacups easier
    hist_percentiles = baseline_means
    hist_percentiles[9] = hist_median


    # make the plot
    fig = plt.figure(figsize=(8, 3))

    ax = fig.gca()
    for i, p in enumerate(range(0, 99)):
        # make base plot
        ax.fill_between([baseline_x1[i], baseline_x2[i]], [baseline_means[i], baseline_means[i]],
                        [baseline_means[i + 1], baseline_means[i + 1]], color=cm.BrBG(p / 100), edgecolor='none')

        # fill corners
        ax.fill_between([baseline_x1[i], baseline_x1[i + 1]], [baseline_means[i + 1], baseline_means[i + 1]],
                        [baseline_means[i], baseline_means[i + 1]], color=cm.BrBG(p / 100), edgecolor='none')

        ax.fill_between([baseline_x2[i], baseline_x2[i + 1]], [baseline_means[i + 1], baseline_means[i + 1]],
                        [baseline_means[i], baseline_means[i + 1]], color=cm.BrBG(p / 100), edgecolor='none')

    hist_mean_x1, hist_mean_x2 = find_x_coords(hist_percentiles)

    crit_mean_x1, crit_mean_x2 = find_x_coords([0, crit, max(baseline_means)])

    ax.plot([hist_mean_x1[9], hist_mean_x2[9] ], np.ones(2) * hist_percentiles[9],
            linewidth=3,
            color='darkblue', linestyle='--')
    ax.plot([((max(baseline_means) - crit) / 2), (1.5 * max(baseline_means) + crit / 2)],
            np.ones(2) * crit, linewidth=3,
            color='hotpink', linestyle=':')


    # climate
    offset = max(baseline_means) * 2.25
    # ax1 = axes[1]
    for i, p in enumerate(range(0, 99)):
        # make base plot
        ax.fill_between([climate_x1[i] + offset, climate_x2[i] + offset], [climate_means[i], climate_means[i]],
                        [climate_means[i + 1], climate_means[i + 1]], color=cm.BrBG(p / 100), edgecolor='none')

        # fill corners
        ax.fill_between([climate_x1[i] + offset, climate_x1[i + 1] + offset],
                        [climate_means[i + 1], climate_means[i + 1]],
                        [climate_means[i], climate_means[i + 1]], color=cm.BrBG(p / 100), edgecolor='none')

        ax.fill_between([climate_x2[i] + offset, climate_x2[i + 1] + offset],
                        [climate_means[i + 1], climate_means[i + 1]],
                        [climate_means[i], climate_means[i + 1]], color=cm.BrBG(p / 100), edgecolor='none')

    ax.plot([hist_mean_x1[9]  + offset, hist_mean_x2[9] + offset],
            np.ones(2) * hist_percentiles[9], linewidth=3,
            color='darkblue', linestyle='--')
    ax.plot([((max(baseline_means) - crit) / 2) + offset,
             (1.5 * max(baseline_means) + crit/2) + offset],
            np.ones(2) * crit, linewidth=3,
            color='hotpink', linestyle=':')


    ax.set_xlim([0, 4.25*max(baseline_means)])
    ax.set_ylim([0, max(baseline_means)])

    print(res_abbrev)
    print('xlim: '+ str(4.25*max(baseline_means)))
    print('ylim: ' + str(max(baseline_means)))
    print(offset)


    ax.axes.get_xaxis().set_visible(False)
    #plt.show()
    plt.savefig(res_abbrev + '_mod_teacups_raw.png', bbox_inches='tight')

make_teacups('BM', 54.8, 20.8)
make_teacups('LG', 37.9, 9.6)
make_teacups('MR', 29.3, 15.7)

#%% Show teacups of historical

def Hist_make_teacups(hist_median, xlim, ylim):
    # make the plot

    #x1, x2 = find_x_coords([hist_median,hist_median])

    x1 = [16.8955, 43.15]
    x2 = [129.45, 155.70]

    fig = plt.figure(figsize=(8, 3))

    ax = fig.gca()

    ax.fill_between([x1[1], x2[0]], [hist_median, hist_median], [0, 0])

    # fill corners
    ax.fill_between([x1[0], x1[1]], [hist_median, hist_median],
                    [hist_median, 0], color='#1f77b4', edgecolor='none')

    ax.fill_between([x2[0], x2[1]], [hist_median, hist_median],
                    [0, hist_median], color='#1f77b4', edgecolor='none')

    ax.set_xlim([0,xlim])
    ax.set_ylim([0,ylim+1])

    ax.plot([0,43.15], [86.3,0], c='k')
    ax.plot([43.15, 129.45], [0, 0], c='k')
    ax.plot([129.45, 172.6], [0, 86.3], c='k')
    ax.plot([0,172.6], [86.3, 86.3], c='k')
    ax.axes.get_xaxis().set_visible(False)
    plt.savefig('TeaCupBuild_med.png', bbox_inches='tight')


Hist_make_teacups(54.8, 366.75, 86.3)

# Show teacups of historical

def Hist_make_teacups_low(hist_median, xlim, ylim, crit):
    # make the plot

    x1_med = [16.8955, 43.15]
    x2_med = [129.45, 155.70]

    x1 = [16.8955, 43.15]
    x2 = [129.45, 155.70]

    #x1, x2 = find_x_coords([hist_median,hist_median])
    fig = plt.figure(figsize=(8, 3))

    ax = fig.gca()

    #ax.plot([(86.3-crit)/2, 129.45 + crit/2], np.ones(2) * crit,
    #        linewidth=3,
    #        color='indianred', linestyle='--')

    ax.plot([x1[0], x2[1]], np.ones(2) * hist_median,
            linewidth=3,
            color='darkblue', linestyle='--')


    ax.fill_between([43.15, 129.45], [crit, crit], [0, 0], color='indianred')

    # fill corners
    ax.fill_between([(86.3-crit)/2, 43.15], [crit, crit],
                    [crit, 0], color='indianred', edgecolor='none')

    ax.fill_between([129.45, 129.45 + crit/2], [crit, crit],
                    [0, crit], color='indianred', edgecolor='none')

    ax.set_xlim([0,xlim])
    ax.set_ylim([0,ylim+1])

    ax.plot([0,43.15], [86.3,0], c='k')
    ax.plot([43.15, 129.45], [0, 0], c='k')
    ax.plot([129.45, 172.6], [0, 86.3], c='k')
    ax.plot([0,172.6], [86.3, 86.3], c='k')
    ax.axes.get_xaxis().set_visible(False)
    plt.savefig('TeaCupBuild_LOW.png', bbox_inches='tight')
    #plt.show()

Hist_make_teacups_low(54.8, 366.75, 86.3, 20.8)
