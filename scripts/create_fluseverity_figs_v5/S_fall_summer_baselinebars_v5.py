#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/25/14
###Function: barplot comparing number of "any diagnosis" visits during the 7 week fall baseline (wks 40-6) and 7 week summer baseline (wks 33-39)
# 2/11/15: migrated from create_fluseverity_figs folder; Sunday to Thursday date conversion affects the anydiag_baseline_comparison function, so this should be run again

###Import data: 

###Command Line: python S_fall_summer_baselinebars_v5.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v5 as fxn

### plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
bw = fxn.gp_barwidth

### functions ###

### import data ###
anydiagin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/fall_summer_baselinebars.csv','r')
anydiagin.readline() # rm header
anydiag=csv.reader(anydiagin, delimiter=',')

### process baseline data ###
# dict_anydiag[season] = (# anydiag fall BL per week, # anydiag summer BL per week)
d_anydiag = fxn.anydiag_baseline_comparison(anydiag)

# plot values
fallBL = [d_anydiag[s][0] for s in ps]
summerBL = [d_anydiag[s][1] for s in ps]
print fallBL
print summerBL

# bar chart of normalized child attack rates
xloc = np.arange(len(ps))
fig, ax = plt.subplots()
fall = ax.bar(xloc, fallBL, bw, color='green', align='center')
summer = ax.bar(xloc+bw, summerBL, bw, color='orange', align='center')
ax.legend([fall[0], summer[0]], ('Fall BL', 'Summer BL'), loc='upper left')
ax.set_xticks(xloc+bw/2)
ax.set_xticklabels(sl, fontsize=fssml)
ax.set_ylabel('Any Diagnosis Visits', fontsize=fs)
ax.set_xlabel('Season', fontsize=fs)

plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/fall_summer_baselinebars.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

