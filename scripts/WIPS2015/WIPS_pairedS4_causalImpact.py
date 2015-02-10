#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14
###Function: Incidence per 100,000 vs. week number for flu weeks (wks 40-20). Incidence is per 100,000 for the US population in the second calendar year of the flu season.
# 10/14/14 OR age flip.
# 10/15 ILI incidence ratio (obsolete)
# 10/19 incidence rate adjusted by any diagnosis visits (coverage adj = visits S9/visits S#) and ILI care-seeking behavior; change to relative risk
# 10/31 no change with v4 for incidence time series

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv

###Command Line: python F_incid_time_v6.py
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
ps = [4,7]
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = ['blue', 'orange']
wklab = fxn.gp_weeklabels
fs = 24
fssml = 16

### program ###

d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)

reference = d_totIncid53ls[7]

# plot incidence time series
ax = plt.axes()
for s, col in zip(ps, colvec):
	plt.plot(xrange(53), d_totIncid53ls[s], marker = fxn.gp_marker, color = col, label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.fill([7, 8, 8, 7], [0, 0, 60, 60], facecolor='grey', alpha=0.4)
plt.fill([11, 13, 13, 11], [0, 0, 60, 60], facecolor='grey', alpha=0.4)
ax.arrow(12, 40, 8, 0, head_width=1, head_length=0.5, fc='k', ec='k')
plt.vlines(reference.index(max(reference)), 0, 60, linestyles = 'dashed', color = 'k')
plt.xlim([0, fw-1])
plt.xticks(range(fw)[:fw:5], wklab[:fw:5]) 
plt.ylim([0, 60])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('Incidence per 100,000', fontsize=fs)
plt.legend(loc='upper right')


plt.savefig('/home/elee/Dropbox/Department/Presentations/2015_WIPS/Figures/IR_child_seas4_peak_paired_seas7_demo.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


