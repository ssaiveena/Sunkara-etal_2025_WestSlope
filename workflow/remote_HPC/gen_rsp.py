import os
from string import Template
import numpy as np
import sys

realizations = np.arange(1000)

BASIN_NAME = sys.argv[1] 	# EXAMPLES: sj2015, gm2015 etc.
SOW = sys.argv[2] 			# BASELINE is 1, then goes sequentially till 9


'''Read RSP template'''
T = open('./' + BASIN_NAME +'B_template.rsp', 'r')
template_RSP = Template(T.read())


for j in realizations:
	scenario = 'S' + str(j) + '_' + SOW
	d = {'XBM': '../../generated_input_files/xbm/' + BASIN_NAME + 'x_' + scenario + '.xbm'}

	new_rsp = template_RSP.safe_substitute(d)
	f1 = open(scenario + '/' + BASIN_NAME +'B_'+scenario+'.rsp', 'w')
	f1.write(new_rsp)
	f1.close()