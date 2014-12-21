#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14
###Function: OR of incidence in adults to incidence in children vs. week number. Incidence in children and adults is normalized by the size of the child and adult populations in the second calendar year of the flu season. 
# 10/14/14 OR age flip.
# 10/15/14 ILI incidence ratio incorporates any diagnosis visits (obsolete)
# 10/19 incidence rate adjusted by any diagnosis visits (coverage adj = visits S9/visits S#) and ILI care-seeking behavior; change to relative risk
# 10/31 coverage adjustment no longer age-specific

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python F_RR_time_v5.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v5 as fxn

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
fs = 24
fssml = 16

### program ###

# dict_wk[wk] = seasonnum
# dict_totIncid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
# dict_totIncidAdj53ls[s] = [adjusted incid rate per 100000 wk 40, ...adj incid wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
# dict_RR53ls[s] = [RR wk 40,... RR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
# dict_zRR53ls[s] = [zRR wk 40,... zRR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
# dict_indices[(snum, classif period)] = [wk index 1, wk index 2, etc.]
d_indices = fxn.identify_retro_early_weeks(d_wk, d_totIncidAdj53ls)

# plot values
for s in ps:
	plt.plot(d_RR53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
for s in ps:
	beg_retro, end_retro = d_indices[(s, 'r')]
	beg_early, end_early = d_indices[(s, 'e')]
	plt.plot(range(beg_retro, end_retro), d_RR53ls[s][beg_retro:end_retro], marker = 's', color = fxn.gp_retro_early_colors[0], linewidth = 4)
	plt.plot(range(beg_early, end_early), d_RR53ls[s][beg_early:end_early], marker = 's', color = fxn.gp_retro_early_colors[1], linewidth = 4)
plt.xlim([0, 53])
plt.xticks(range(len(wklab))[::5], wklab[::5]) 
plt.ylim([0.1, 1])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('RR, adult:child', fontsize=fs)
plt.legend(loc='upper right')
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/RR_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()




