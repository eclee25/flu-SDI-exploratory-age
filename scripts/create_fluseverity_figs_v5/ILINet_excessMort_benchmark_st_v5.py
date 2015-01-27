#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: state-level excess P&I mortality rates (from Cecile) vs. CDC benchmark index 

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index_long.csv, CDC_Source/Import_Data/all_cdc_source_data.csv, Census/Import_Data/totalpop_age_Census_98-14.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv, excess mort data from Cecile

###Command Line: python ILINet_excessMort_benchmark_st_v5.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season
# 2013-14 ILINet data is normalized by estimated population size from December 2013 because 2014 estimates are not available at this time
# 2009-10 data is removed from cdc_severity_index_long.csv

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np
from itertools import product

## local modules ##
import functions_v5 as fxn

### data structures ###

### functions ###
### data files ###
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index_long.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_ILINet_seasonlabels
fs = 24
fssml = 16
ILIcol_ePIps = fxn.gp_ILINet_colors[1:-1]

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
d_benchmark = fxn.benchmark_import(ix, 8) # no ILINet outpatient data
# import state-level excess P&I mortality rates
d_st_excessPI = fxn.excessPI_state_import()
# seasons included in excess mortality rate data
ePI_ps = sorted(set([key[0] for key in d_st_excessPI]).intersection(ps))
# state abbrs
states = sorted(set([key[1] for key in d_st_excessPI]))

# draw plot
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)

# plot values
for s, col in zip(ePI_ps, ILIcol_ePIps):
	benchmark = [d_benchmark[s]] * len(states)
	excess_PI = [d_st_excessPI[(s, st)] for st in states]
	ax1.plot(benchmark, excess_PI, marker = 'o', color = col, linestyle = 'None')
	ax1.text(d_benchmark[s], -1.25, '%s' %(s), fontsize=fssml, horizontalalignment='center')
ax1.vlines([-1, 1], -20, 50, colors='k', linestyles='solid')
# ax1.hlines([-1, 1], -20, 30, colors='k', linestyles='solid')
# ax1.fill([-6, -1, -1, -6], [-1, -1, -20, -20], facecolor='blue', alpha=0.4)
# ax1.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
# ax1.fill([1, 10, 10, 1], [1, 1, 30, 30], facecolor='red', alpha=0.4)
ax1.annotate('Mild', xy=(-6.5,-1), fontsize=fssml)
ax1.annotate('Severe', xy=(8,19), fontsize=fssml)

ax1.set_ylabel('Excess P&I Mort. per 100,000', fontsize=fs)
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both',labelsize=fssml)
ax1.set_xlim([-7,10])
ax1.set_ylim([-2,20])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/ILINet_excessMort_benchmark_st.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()


