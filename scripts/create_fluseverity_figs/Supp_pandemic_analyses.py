#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/12/14
###Function: analyze pandemic dynamics when considering different baseline periods - between two pandemic peaks, time series after November 2009, 2008-09 baseline for entire pandemic period

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv

###Command Line: python Supp_pandemic_analyses.py
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
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
norm = fxn.gp_normweeks
fs = 24
fssml = 16
BL = fxn.gp_pandemicbaseline
tricolor = fxn.gp_agecolors

### program ###

# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)

for BL_txt, col in zip(BL, tricolor):
	d_zOR_pan = fxn.week_zOR_processing_pandemic(d_wk, d_OR, BL_txt)
	d_incid53ls_pan, d_OR53ls_pan, d_zOR53ls_pan = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR_pan)

	plotvals = d_zOR53ls_pan[9] + d_zOR53ls_pan[10]
	plt.plot(plotvals, marker = 'o', color = col, label = BL_txt, linewidth = 2)
plt.plot(d_zOR53ls[9], marker = 'o', color = 'k', linewidth=2, label='2008-09 season')

plt.xticks(range(2*len(wklab))[::5], wklab[::5] + wklab[::5]) 
plt.xlabel('Week Number (2008-09 and 2009-10)', fontsize=fs)
plt.ylabel('zOR', fontsize=fs)
plt.legend(loc='lower left')
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_time_pandemic.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()





