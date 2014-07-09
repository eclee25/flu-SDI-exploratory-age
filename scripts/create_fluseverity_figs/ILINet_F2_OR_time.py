#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/18/14
###Function: OR of incidence in children to incidence in adults vs. week number. Incidence in children and adults is normalized by the size of the child and adult populations in the second calendar year of the flu season. ILINet data

###Import data: CDC_Source/Import_Data/all_cdc_source_data.csv, Census/Import_Data/totalpop_age_Census_98-14.csv

###Command Line: python ILINet_F2_OR_time.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season
# 2013-14 ILINet data is normalized by estimated population size from December 2013 because 2014 estimates are not available at this time

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions as fxn

### data structures ###
### functions ###
### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv','r')
incidin.readline() # remove header
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data/totalpop_age_Census_98-14.csv', 'r')
pop = csv.reader(popin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
sl = fxn.gp_ILINet_seasonlabels
colvec = fxn.gp_ILINet_colors
wklab = fxn.gp_weeklabels
fs = 24
fssml = 16

### program ###
# import data
# d_wk[week] = seasonnum, d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_wk, d_incid, d_OR = fxn.ILINet_week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)

# plot values
fig = plt.figure()
ax = plt.subplot(111)

for s, i in zip(ps, xrange(len(ps))):
	ax.plot(xrange(fw), d_OR53ls[s][:fw], marker = 'o', color = colvec[i], label = sl[i], linewidth = 2)
plt.xlim([0, fw-1])
plt.xticks(range(fw)[::5], wklab[:fw:5]) 
plt.ylim([0, 8])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('OR, child:adult', fontsize=fs)
# shrink current axis by 10%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width*0.9, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/ILINet/OR_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()




