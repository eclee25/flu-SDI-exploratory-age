#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/26/14
###Function: Incidence per 100,000 vs. week number for flu weeks (wks 40-20). Incidence is per 100,000 for the US population in the second calendar year of the flu season.

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python F2_incid_time.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions as fxn

### data structures ###

### functions ###
### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
fs = 24
fssml = 16

### program ###
# import data
# d_wk[week] = seasonnum, d_incid53ls[seasonnum] = [ILI wk 40 per 10000, ILI wk 41,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_wk, d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(incid, pop)

# plot values
for s in ps:
	plt.plot(xrange(fw), d_incid53ls[s][:fw], marker = 'o', color = colvec[s-2], label = sl[s-2], linewidth = 2)
plt.xlim([0, fw-1])
plt.xticks(range(fw)[::5], wklab[:fw:5]) 
plt.ylim([0, 60])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('Incidence per 100,000', fontsize=fs)
plt.legend(loc='upper left')
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F2/incid_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()




