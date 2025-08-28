# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:44:01 2022

@author: Rohini
"""

import numpy as np
import statsmodels.api as sm

def createXBMDataFrames(filename, firstLine, numSites,abbrev):
    # split data on periods
    with open(filename,'r') as f:
        all_split_data = [x.split('.') for x in f.readlines()]
        
    f.close()
    
    numYears = int((len(all_split_data)-firstLine)/numSites)
    MonthlyQ = np.zeros([12*numYears,numSites])
    for i in range(numYears):
        for j in range(numSites):
            index = firstLine + i*numSites + j
            all_split_data[index][0] = all_split_data[index][0].split()[2]
            MonthlyQ[i*12:(i+1)*12,j] = np.asfarray(all_split_data[index][0:12], float)
            
    np.savetxt('../../historical_data/'+abbrev+'2015_StateMod/MonthlyQ.csv',MonthlyQ,fmt='%d',delimiter=',')
    
    # calculate annual flows
    AnnualQ = np.zeros([numYears,numSites])
    for i in range(numYears):
        AnnualQ[i,:] = np.sum(MonthlyQ[i*12:(i+1)*12],0)
        
    np.savetxt('../../historical_data/'+abbrev+'2015_Statemod/AnnualQ.csv',AnnualQ,fmt='%d',delimiter=',')
            
    return None

#%%

def createIWRDataFrames(filename, firstLine, numSites,abbrev):
    # split data on periods
    with open(filename,'r') as f:
        all_split_data = [x.split('.') for x in f.readlines()]
        
    f.close()
    
    numYears = int((len(all_split_data)-firstLine)/numSites)
    MonthlyIWR = np.zeros([12*numYears,numSites])
    for i in range(numYears):
        for j in range(numSites):
            index = firstLine + i*numSites + j
            all_split_data[index][0] = all_split_data[index][0].split()[2]
            MonthlyIWR[i*12:(i+1)*12,j] = np.asfarray(all_split_data[index][0:12], float)
            
    np.savetxt('./historical_data/'+abbrev+'2015_StateMod/MonthlyIWR.csv',MonthlyIWR,fmt='%d',delimiter=',')
    
    # calculate annual flows
    AnnualIWR = np.zeros([numYears,numSites])
    for i in range(numYears):
        AnnualIWR[i,:] = np.sum(MonthlyIWR[i*12:(i+1)*12],0)
        
    np.savetxt('./historical_data/'+abbrev+'2015_StateMod/AnnualIWR.csv',AnnualIWR,fmt='%d',delimiter=',')
            
    return None

#%%

def organizeMonthly(filename, firstLine, numSites):
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
#%%
def writeNewStatemodFiles(filename,abbrev, firstLine, sampleNo, realizationNo, allMonthlyData,out_directory):
    nSites = np.shape(allMonthlyData)[1]
    
    # split data on periods
    with open('../../historical_data/'+abbrev+'2015_StateMod/StateMod/'+filename,'r') as f:
        all_split_data = [x.split('.') for x in f.readlines()]
        
    f.close()
        
    # get unsplit data to rewrite firstLine # of rows
    with open('../../historical_data/'+abbrev+'2015_StateMod/StateMod/'+filename,'r') as f:
        all_data = [x for x in f.readlines()]
        
    f.close()
    
    # replace former flows with new flows
    new_data = []
    for i in range(len(all_split_data)-firstLine):
        year_idx = int(np.floor(i/(nSites)))
        #print(year_idx)
        site_idx = np.mod(i,(nSites))
        #print(site_idx)
        row_data = []
        # split first 3 columns of row on space and find 1st month's flow
        row_data.extend(all_split_data[i+firstLine][0].split())
        row_data[2] = str(int(allMonthlyData[year_idx,site_idx,0]))
        # find remaining months' flows
        for j in range(11):
            row_data.append(str(int(allMonthlyData[year_idx,site_idx,j+1])))
            
        # find total flow
        row_data.append(str(int(np.sum(allMonthlyData[year_idx,site_idx,:]))))
            
        # append row of adjusted data
        new_data.append(row_data)

    f = open(out_directory+ filename[0:-4] + '_S' + str(sampleNo) + '_' + str(realizationNo)+ filename[-4::],'w')
    # write firstLine # of rows as in initial file
    for i in range(firstLine):
        f.write(all_data[i])
        
    for i in range(len(new_data)):
        # write year, ID and first month of adjusted data
        f.write(new_data[i][0] + ' ' + new_data[i][1] + (19-len(new_data[i][1])-len(new_data[i][2]))*' ' + new_data[i][2] + '.')
        # write all but last month of adjusted data
        for j in range(len(new_data[i])-4):
            f.write((7-len(new_data[i][j+3]))*' ' + new_data[i][j+3] + '.')
            
        # write last month of adjusted data
        if filename[-4::] == '.xbm':
            if len(new_data[i][-1]) <= 7:
                f.write((7-len(new_data[i][-1]))*' ' + new_data[i][-1] + '.' + '\n')
            else:
                f.write('********\n')
        else:
            f.write((9-len(new_data[i][-1]))*' ' + new_data[i][-1] + '.' + '\n')
        
    f.close()
    
    return None


