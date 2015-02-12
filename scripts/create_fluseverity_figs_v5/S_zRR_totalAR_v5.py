#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: mean peak-based retro zRR metric vs. total attack rate

###Import data: Py_export/SDI_nat_classif_covCareAdj_v5_7.csv, 

###Command Line: python S_zRR_totalAR_v5.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

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


print 'retro corr coef', np.corrcoef(AR, retrozOR) # 0.744 (updated 2/11/15)
print 'early corr coef', np.corrcoef(AR, earlyzOR) # 0.424 - old (would be nan with 2/11/15 update)

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# mean retro zOR vs. attack rate
ax1.plot(AR, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, AR, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax1.set_xlabel(fxn.gp_attackrate, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_ylim([-15,18])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/zRR_CFR_CHR/zRR_totalAR.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

