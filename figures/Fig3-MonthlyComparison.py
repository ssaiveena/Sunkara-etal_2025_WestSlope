import numpy as np
import matplotlib.pyplot as plt

#
def plotMonthlyFlows(abbrev, last_node,ax):
    historical = np.loadtxt('Historical_data/'+abbrev+'/MonthlyQ.csv', delimiter=',')
    historical = historical[:,last_node].reshape([105,12])

    synthetic = np.zeros([105,12,1000])
    for r in range(1000):
        synthetic[:,:,r] = np.loadtxt('Synthetic_records/Monthly/'+abbrev+'/MonthlyQ_s'+str(r)+'.csv', delimiter=' ')

    hist_90 = np.percentile(historical, 90, axis=0)
    hist_10 = np.percentile(historical, 10, axis=0)
    hist_mean = np.mean(historical, axis=0)

    synth_90 = np.max(np.percentile(synthetic, 90,axis=0),axis=1)
    synth_10 = np.min(np.percentile(synthetic, 10, axis=0), axis=1)
    synth_mean = np.mean(np.mean(synthetic, axis=0), axis=1)

    ax.fill_between(np.arange(12), np.log(synth_10*1233.48), np.log(synth_90*1233.48), alpha=.9, color='cornflowerblue')
    ax.fill_between(np.arange(12), np.log(hist_10*1233.48), np.log(hist_90*1233.48), alpha=.9, color='goldenrod')
    ax.plot(np.arange(12), np.log(synth_mean*1233.48), color='cornflowerblue', linestyle='dashed')
    ax.plot(np.arange(12), np.log(hist_mean*1233.48), color='darkgoldenrod', linestyle='dashed')


basins = ['cm', 'gm', 'ym', 'wm', 'sj']
last_nodes = [-1,-1,-1,-3,-2]
fig, axes = plt.subplots((2,3))

for i in range(len(basins)):
    plotMonthlyFlows(basins[i], last_nodes[i], axes.flatten()[i])

plt.show()

