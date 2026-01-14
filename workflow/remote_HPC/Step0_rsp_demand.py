import math
import numpy as np
from string import Template
import os
import pandas as pd
import sys
import shutil

# =============================================================================
# Experiment set up
# =============================================================================
# Read in SOW parameters
LHsamples = np.loadtxt('LHsamples_1000.txt')
nSamples = len(LHsamples[:,0])
realizations = 20
# =============================================================================
# Load global information (applicable to all SOW)
# =============================================================================
# For RSP
# T = open('Statemod_files/sj2015B_template.rsp', 'r')
# template_RSP = Template(T.read())
#
# # =============================================================================
# # Loop though all SOWs
# # # =============================================================================
# for k in range(nSamples):
#    for j in range(realizations):
#        d = {}
#        d['IWR'] = '../../../Statemod_files/sj2015B.iwr'
#        d['DDM'] = '../../../Statemod_files/sj2015B.ddm'
#        d['XBM'] = '../../../xbm/San_Juan/sj2015x_S' + str(k) + '_' + str(j) + '.xbm'
#        if j ==0:
#          os.chdir('Experiment_files/wodemand/')
#          os.mkdir('S_' + str(k))
#          os.chdir('../../')
#        S1 = template_RSP.safe_substitute(d)
#        f1 = open('Experiment_files/wodemand/S_' + str(k) + '/sj2015B_S' + str(k) + '_' + str(j) + '.rsp', 'w')
#        f1.write(S1)
#        f1.close()

T = open('Statemod_files/cm2015B_template.rsp', 'r')
template_RSP = Template(T.read())

# =============================================================================
# Loop though all SOWs
# # =============================================================================
for k in range(nSamples):
   for j in range(realizations):
       d = {}
       d['IWR'] = '../../../Experiment_files/HMM_1000/S_' + str(k) + '/cm2015B_S' + str(k) + '_' + str(j) + '.iwr'
       d['DDM'] = '../../../Experiment_files/HMM_1000/S_' + str(k) + '/cm2015B_S' + str(k) + '_' + str(j) + '.ddm'
       d['XBM'] = '../../../xbm/Upper_Colorado/cm2015x_S' + str(k) + '_' + str(j) + '.xbm'
       # d['IWR'] = '../../../Statemod_files/cm2015B.iwr'
       # d['DDM'] = '../../../Statemod_files/cm2015B.ddm'
       # d['XBM'] = '../../../xbm/Upper_Colorado/cm2015x_S' + str(k) + '_' + str(j) + '.xbm'
       # if j ==0:
       #   os.chdir('Experiment_files/wodemand/')
       #   os.mkdir('S_' + str(k))
       #   os.chdir('../../')
       S1 = template_RSP.safe_substitute(d)
       f1 = open('Experiment_files/HMM_1000/S_' + str(k) + '/cm2015B_S' + str(k) + '_' + str(j) + '.rsp', 'w')
       f1.write(S1)
       f1.close()

# T = open('Statemod_files/gm2015B_template.rsp', 'r')
# template_RSP = Template(T.read())
#
# for k in range(nSamples):
#    for j in range(realizations):
#        d = {}
#        d['IWR'] = '../../../Statemod_files/gm2015B.iwr'
#        d['DDM'] = '../../../Statemod_files/gm2015B.ddm'
#        d['XBM'] = '../../../xbm/Gunnison/gm2015x_S' + str(k) + '_' + str(j) + '.xbm'
#        # if j ==0:
#        #   os.chdir('Experiment_files/wodemand/')
#        #   os.mkdir('S_' + str(k))
#        #   os.chdir('../../')
#        S1 = template_RSP.safe_substitute(d)
#        f1 = open('Experiment_files/wodemand/S_' + str(k) + '/gm2015B_S' + str(k) + '_' + str(j) + '.rsp', 'w')
#        f1.write(S1)
#        f1.close()
#
# T = open('Statemod_files/ym2015B_template.rsp', 'r')
# template_RSP = Template(T.read())
# for k in range(nSamples):
#    for j in range(realizations):
#        d = {}
#        d['IWR'] = '../../../Statemod_files/ym2015B.iwr'
#        d['DDM'] = '../../../Statemod_files/ym2015B.ddm'
#        d['XBM'] = '../../../xbm/Yampa/ym2015x_S' + str(k) + '_' + str(j) + '.xbm'
#        # if j ==0:
#        #   os.chdir('Experiment_files/wodemand/')
#        #   os.mkdir('S_' + str(k))
#        #   os.chdir('../../')
#        S1 = template_RSP.safe_substitute(d)
#        f1 = open('Experiment_files/wodemand/S_' + str(k) + '/ym2015B_S' + str(k) + '_' + str(j) + '.rsp', 'w')
#        f1.write(S1)
#        f1.close()
#
# T = open('Statemod_files/wm2015B_template.rsp', 'r')
# template_RSP = Template(T.read())
# for k in range(nSamples):
#    for j in range(realizations):
#        d = {}
#        d['IWR'] = '../../../Statemod_files/wm2015B.iwr'
#        d['DDM'] = '../../../Statemod_files/wm2015B.ddm'
#        d['XBM'] = '../../../xbm/White/wm2015x_S' + str(k) + '_' + str(j) + '.xbm'
#        # if j ==0:
#        #   os.chdir('Experiment_files/wodemand/')
#        #   os.mkdir('S_' + str(k))
#        #   os.chdir('../../')
#        S1 = template_RSP.safe_substitute(d)
#        f1 = open('Experiment_files/wodemand/S_' + str(k) + '/wm2015B_S' + str(k) + '_' + str(j) + '.rsp', 'w')
#        f1.write(S1)
#        f1.close()