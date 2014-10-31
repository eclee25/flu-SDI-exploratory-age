#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/15/14
###Function: OR of incidence in adults to incidence in children vs. week number normalized by the first 'gp_normweeks' of the season. Incidence in children and adults is normalized by the size of the child and adult populations in the second calendar year of the flu season. 
# 10/14/14 OR age flip.
# 10/15/14 ILI incidence ratio

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python aF3_zOR_time.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v3 as fxn

### data structures ###
### functions ###
### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
norm = fxn.gp_normweeks
fs = 24
fssml = 16

### program ###

# dict_wk[wk] = seasonnum
# dict_incid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
# dict_OR53ls[s] = [OR wk 40,... OR wk 39] (children and adults adjusted for SDI data coverage and ILI-seeking behavior)
# dict_zOR53ls[s] = [zOR wk 40,... zOR wk 39] (children and adults adjusted for SDI data coverage and ILI-seeking behavior)
d_wk, d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_OR_processing(incid, pop)
# dict_indices[(snum, classif period)] = [wk index 1, wk index 2, etc.]
d_indices = fxn.identify_retro_early_weeks(d_wk, d_incid53ls)

# plot values
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for s in ps:
	ax.plot(xrange(len(wklab)), d_zOR53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
	beg_retro, end_retro = d_indices[(s, 'r')]
	beg_early, end_early = d_indices[(s, 'e')]
	plt.plot(range(beg_retro, end_retro), d_zOR53ls[s][beg_retro:end_retro], marker = 'o', color = 'black', linewidth = 4)
	plt.plot(range(beg_early, end_early), d_zOR53ls[s][beg_early:end_early], marker = 'o', color = 'grey', linewidth = 4)
ax.legend(loc='upper left')
ax.set_xticks(range(len(wklab))[::5])
ax.set_xticklabels(wklab[::5]) 
ax.set_xlim([0, fw-1])
ax.set_xlabel('Week Number', fontsize=fs)
ax.set_ylabel(fxn.gp_sigmat, fontsize=fs)
# plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v3/F2/zOR_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()
# plt.show()

plt.savefig(fxn.filename_dummy1, transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
