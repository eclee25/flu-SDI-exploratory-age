#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/4/14
###Function: Child and adult attack rates are normalized to the percent deviation in average baseline across all seasons. Percent deviation is calculated as ((raw attack rate/avg attack rate across all seasons)-1)*100. The "-1" adjusts the ratio average to 0.
#### Compare children and adults to their own average baselines across all seasons to explore relative attack rates of each age group in mild, moderate, and severe seasons.

###Import data: OR_allweeks_outpatient.csv, totalpop_age.csv

###Command Line: python F6_AR_season_CA_normalized.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###

### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
fs = 24
fssml = 16
# mild_s = fxn.gp_mild
# mod_s = fxn.gp_mod
# sev_s = fxn.gp_sev
s_lab = fxn.gp_seasonlabels
sevcol = fxn.gp_severitycolors
bw = fxn.gp_barwidth
agelab = fxn.gp_agelabels
agecol = fxn.gp_agecolors


### functions ###

### import data ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

# d_wk[week] = seasonnum, d_incid[wk] = (child incid per 100,000, adult incid per 100,000, other incid per 100,000)
d_wk, d_incid = fxn.week_incidCA_processing(incid, pop)
# d_perc_totAR[seasonnum] = (% contribution of child AR to total AR, % contribution of adult AR to total AR, % contribution of other ages AR to total AR)
# d_tot_attack[seasonnum] = total attack rate for weeks 40 to 20 by 100,000
d_perc_totAR, d_tot_attack = fxn.contributions_CAO_to_attack(d_wk, d_incid)

# initialize figure
fig = plt.figure()

ax = fig.add_subplot(1,1,1)

cdat = [d_perc_totAR[k][0] for k in ps]
adat = [d_perc_totAR[k][1] for k in ps]
odat = [d_perc_totAR[k][2] for k in ps]

child = ax.bar(ps, cdat, bw, color=agecol[0], align='center')
adult = ax.bar(ps, adat, bw, color=agecol[1], align='center', bottom=cdat)
other = ax.bar(ps, odat, bw, color=agecol[2], align='center', bottom=np.add(cdat,adat))
# label formatting
ax.set_ylabel('Percent of Total Attack Rate', fontsize=fs)
ax.legend([child, adult, other], agelab, loc='upper left')
ax.set_xticks(range(2,10))
ax.set_xticklabels(s_lab, fontsize=fssml)
ax.set_xlim([1,10])
ax.set_ylim([0,100])

# show total attack rate per 100,000 for each year
for s in ps:
	plt.text(s, 5, int(d_tot_attack[s]), ha='center', va='bottom', fontsize=fssml)
plt.text(5.5, 11, 'Total attack rate per 100,000', fontsize=fssml, ha='center')

# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F6/F6_attackCAO_stacked100.png' , transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
