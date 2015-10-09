#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: mean peak-based retro zRR metric vs. total attack rate
# 7/20/15: new notation
# 10/8/15: rm vert lines, color points, p-values

###Import data: Py_export/SDI_nat_classif_covCareAdj_v5_7.csv, 

###Command Line: python S_zRR_totalAR_v5.py
##############################################


### notes ###
### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

## local modules ##
import functions_v5 as fxn

### data structures ###

### functions ###
### data files ###
natixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv', 'r')
natixin.readline() # remove header
natix = csv.reader(natixin, delimiter=',')
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fw = fxn.gp_fluweeks
fs = 24
fssml = 16

### program ###

## import severity index ##
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_nat_classif = fxn.readNationalClassifFile(natix)

## import adjusted attack rate ##
d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)

# plot values
AR = [sum(d_totIncidAdj53ls[s][:fw]) for s in ps]
retrozOR = [d_nat_classif[s][0] for s in ps]
earlyzOR = [d_nat_classif[s][1] for s in ps]
vals = zip(AR, retrozOR, earlyzOR)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# updated 10/8/15
print 'retro corr coef', scipy.stats.pearsonr(AR, retrozOR) # R = 0.744, p-value = 0.034
print 'early corr coef', scipy.stats.pearsonr(AR, earlyzOR) # NaN

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# mean retro zOR vs. attack rate
for key in d_plotCol:
	ax1.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][1] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, AR, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax1.set_xlabel(fxn.gp_attackrate, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_ylim([-15,18])
ax1.set_xlim([1400,1900])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_totalAR.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

