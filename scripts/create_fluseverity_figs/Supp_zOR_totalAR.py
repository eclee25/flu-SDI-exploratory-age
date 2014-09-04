#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 9/2/14
###Function: mean peak-based retro zOR metric vs. total attack rate

###Import data:  SQL_export/OR_allweeks_outpatient.csv, SQL_export/OR_allweeks.csv

###Command Line: python Supp_zOR_totalAR.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###

### functions ###
### data files ###
zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications.csv','r')
zORin.readline() # rm header
zOR = csv.reader(zORin, delimiter=',')
allincidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
allincid = csv.reader(allincidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### program ###

## import severity index ##
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_nat_classif = fxn.readNationalClassifFile(zOR)

## import attack rate ##
# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid = fxn.week_incidCA_processing(allincid, pop)
# dict_tot_attack[seasonnum] = total attack rate for weeks 40 to 20 by 100,000
_, d_tot_attack = fxn.contributions_CAO_to_attack(d_wk, d_incid)

# plot values
AR = [d_tot_attack[s] for s in ps]
retrozOR = [d_nat_classif[s][0] for s in ps]
earlyzOR = [d_nat_classif[s][1] for s in ps]

print 'retro corr coef', np.corrcoef(AR, retrozOR)
print 'early corr coef', np.corrcoef(AR, earlyzOR)

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
ax1.set_ylim([-10,20])
ax1.invert_yaxis()
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_totalAR.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

