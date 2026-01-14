import numpy as np
import pandas as pd
from scipy import stats as ss
import utils
from random import random
from writeNewFiles import writeNewFiles
from mpi4py import MPI
import math

def readFiles(filename, firstLine, numSites):
    # read in all monthly flows and re-organize into nyears x 12 x nsites matrix
    with open(filename,'r') as f:
        all_split_data = [x.split('.') for x in f.readlines()]
        
    f.close()
    
    numYears = int((len(all_split_data)-firstLine)/numSites)
    MonthlyQ = np.zeros([12*numYears,numSites])
    sites = []
    for i in range(numYears):
        for j in range(numSites):
            index = firstLine + i*numSites + j
            sites.append(all_split_data[index][0].split()[1])
            all_split_data[index][0] = all_split_data[index][0].split()[2]
            MonthlyQ[i*12:(i+1)*12,j] = np.asfarray(all_split_data[index][0:12], float)
            
    MonthlyQ = np.reshape(MonthlyQ,[int(np.shape(MonthlyQ)[0]/12),12,numSites])
            
    return MonthlyQ

# read in monthly flows at all sites
MonthlyQ_all = readFiles('Statemod_files/cm2015x.xbm', 16, 208) #change this #first line 16 for all sites numsites = 165 for sj 208 for cm
#139 for gm, 208 for cm,94 for ym, 43 for wm
MonthlyQ_all_ratios = np.zeros(np.shape(MonthlyQ_all))

# divide monthly flows at each site by the monthly flow at the last node
for i in range(np.shape(MonthlyQ_all_ratios)[2]):
    MonthlyQ_all_ratios[:,:,i] = MonthlyQ_all[:,:,i]/MonthlyQ_all[:,:,-1]
    
# read in Latin hypercube sample of multipliers/shifts
# parameters: IWR, mu0, sigma0, mu1, sigma1, p00, p11, snowshift
LHsamples = np.loadtxt('../LHS_samples/LHsamples_1000.txt',usecols=[0])

# Prepend row to LHsamples with base case did this manually
# base_case = np.ones([1,1])
# #base_case[0,0] = 0
# LHsamples = np.concatenate((base_case,LHsamples),0)

AnnualQ_h = np.array(pd.read_csv('historical_data/cm2015_StateMod/AnnualQ.csv', header=None))
logAnnualQ_h = np.log(AnnualQ_h+1) # add 1 because site 47 has years with 0 flow

# get historical flow ratios
AnnualQ_h_ratios = np.zeros(np.shape(AnnualQ_h))
for i in range(np.shape(AnnualQ_h_ratios)[0]):
    AnnualQ_h_ratios[i,:] = AnnualQ_h[i,:] / np.sum(AnnualQ_h[i,-1])

# fit seasonal model to each site (model mean w/ 2 harmonics after Box-Cox transformation)
nSites = 208 #change this #94 for ym #np.shape(MonthlyQ_h)[1]-1  #edit this
#139 for gm, 94 for ym, 165 sj, 43 wm , 208 cm 
nMonths = 12
last_node = -1
historical_column = 4 
# load historical (_h) irrigation demand data
AnnualIWR_h = np.loadtxt('historical_data/cm2015_StateMod/AnnualIWR.csv',delimiter=',')
MonthlyIWR_h = np.loadtxt('historical_data/cm2015_StateMod/MonthlyIWR.csv',delimiter=',')
IWRsums_h = np.sum(AnnualIWR_h,1)
IWRfractions_h = np.zeros(np.shape(AnnualIWR_h))
for i in range(np.shape(AnnualIWR_h)[0]):
    IWRfractions_h[i,:] = AnnualIWR_h[i,:] / IWRsums_h[i]
    
IWRfractions_h = np.mean(IWRfractions_h,0)

# model annual irrigation demand anomaly as function of annual flow anomaly at last node
BetaIWR, muIWR, sigmaIWR = utils.fitIWRmodel(AnnualQ_h, AnnualIWR_h)

# load monthly fractions at last node under different hydrograph shifts
# LastNodeFractions = np.load('LastNodeFractions.npy')

# Begin parallel simulation
comm = MPI.COMM_WORLD

# Get the number of processors and the rank of processors
rank = comm.rank
nprocs = comm.size

# Determine the chunk which each processor will neeed to do
count = int(math.floor(np.shape(LHsamples)[0]/nprocs))
remainder = np.shape(LHsamples)[0] % nprocs

# Use the processor rank to determine the chunk of work each processor will do
if rank < remainder:
    start = rank*(count+1)
    stop = start + count + 1
else:
    start = remainder*(count+1) + (rank-remainder)*count
    stop = start + count

# generate nYears of flows at all sites for each SOW
nYears = np.shape(AnnualQ_h)[0]
for i in range(start, stop):
    for realization in range(1):
        print(i)
       # create matrices to store nYears of synthetic (_s), real-space (AnnualQ_s), 
        # log space (logAnnualQ_s), z-scores (z_s) and quantiles (q_s) at all sites
        logAnnualQ_s = np.empty([nYears]) # last node only
        AnnualIWR_s = np.empty([nYears,nSites])
                        
        # load generated annual Q_s from iwr model
        AnnualQ_s = np.array(pd.read_csv('Synthetic_records/samples/AnnualQ_s' + str(realization) + '.txt', sep=' ', header=None))
        AnnualQ_s = AnnualQ_s[:,0]#change this
        #Upper_Colorado Gunnison    Yampa   White   SanJuan_Dolores

        # calculate annual IWR anomalies based on annual flow anomalies at last node
        TotalAnnualIWRanomalies_s = BetaIWR*(AnnualQ_s-np.mean(AnnualQ_s)) + \
            ss.norm.rvs(muIWR, sigmaIWR,len(AnnualQ_s))

        TotalAnnualIWR_s = np.mean(IWRsums_h)*LHsamples[i] + TotalAnnualIWRanomalies_s
        #Replace IWR multiplier with 1 for streamflow only scenarios
        TotalAnnualIWR_s_flowOnly = np.mean(IWRsums_h) + TotalAnnualIWRanomalies_s
        AnnualIWR_s = np.dot(np.reshape(TotalAnnualIWR_s,[np.size(TotalAnnualIWR_s),1]), \
                                     np.reshape(IWRfractions_h,[1,np.size(IWRfractions_h)]))
        AnnualIWR_s_flowOnly = np.dot(np.reshape(TotalAnnualIWR_s_flowOnly,[np.size(TotalAnnualIWR_s_flowOnly),1]), \
                                     np.reshape(IWRfractions_h,[1,np.size(IWRfractions_h)]))
        
        # Get historical flow ratios for last node monthly
        last_node_breakdown = np.zeros([105, 12])
        for ind in range(np.shape(last_node_breakdown)[0]):
            last_node_breakdown[ind, :] = MonthlyQ_all[ind, :, last_node] / AnnualQ_h[ind, last_node]
    
        # disaggregate annual flows and demands at all sites using randomly selected neighbor from k nearest based on flow
        dists = np.zeros([nYears,np.shape(AnnualQ_h)[0]])
        for j in range(nYears):
            for m in range(np.shape(AnnualQ_h)[0]):
                dists[j,m] = dists[j,m] + (AnnualQ_s[j] - AnnualQ_h[m,-1])**2
                    
        probs = np.zeros([int(np.sqrt(np.shape(AnnualQ_h)[0]))])
        for j in range(len(probs)):
            probs[j] = 1/(j+1)
            
        probs = probs / np.sum(probs)
        for j in range(len(probs)-1):
            probs[j+1] = probs[j] + probs[j+1]
            
        probs = np.insert(probs, 0, 0)   
        MonthlyIWR_s = np.zeros([nYears,np.shape(MonthlyIWR_h)[1],12])
        MonthlyIWR_s_flowOnly = np.zeros([nYears,np.shape(MonthlyIWR_h)[1],12])
        for j in range(nYears):
            # select one of k nearest neighbors for each simulated year
            neighbors = np.sort(dists[j,:])[0:int(np.sqrt(np.shape(AnnualQ_h)[0]))]
            indices = np.argsort(dists[j,:])[0:int(np.sqrt(np.shape(AnnualQ_h)[0]))]
            randnum = random()
            for k in range(1,len(probs)):
                if randnum > probs[k-1] and randnum <= probs[k]:
                    neighbor_index = indices[k-1]
           
            # use selected neighbors to downscale flows and demands each year at last node, accounting for time shift of peak
            proportions = last_node_breakdown[neighbor_index, :] * AnnualQ_s[j]
            # proportions = LastNodeFractions[neighbor_index,int(np.round(LHsamples[i,-1],0)),:]
            
            for k in range(np.shape(MonthlyIWR_h)[1]):
                if np.sum(MonthlyIWR_h[neighbor_index*12:(neighbor_index+1)*12,k]) > 0:
                    proportions = MonthlyIWR_h[neighbor_index*12:(neighbor_index+1)*12,k] / \
                        np.sum(MonthlyIWR_h[neighbor_index*12:(neighbor_index+1)*12,k])
                else:
                    proportions = np.zeros([12])
                
                MonthlyIWR_s[j,k,:] = proportions*AnnualIWR_s[j,k]
                MonthlyIWR_s_flowOnly[j,k,:] = proportions*AnnualIWR_s_flowOnly[j,k]
        
        design = 'LHsamples_original_1000'
        
        # write new irrigation demands to file for LHsample i
        writeNewFiles('cm2015B.iwr', 463, i, realization+1, MonthlyIWR_s, '',design) # a for all uncertainties#change this
        #463 for cm, 377 for sj, 202 for wm, 620 for gm, 370 for ym

        # write new irrigation demands to file for LHsample i
        #writeNewFiles('cm2015B.iwr', 463, i, realization+1, MonthlyIWR_s_flowOnly, 'f',design) # f for flow uncertainties only
