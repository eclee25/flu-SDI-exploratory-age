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

## local modules ##
import functions as fxn

### data structures ###

### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
fs = 24
fssml = 16
mild_s = fxn.gp_mild
mod_s = fxn.gp_mod
sev_s = fxn.gp_sev
s_lab = fxn.gp_seasonlabels
sevcol = fxn.gp_severitycolors
bw = fxn.gp_barwidth
sevlab = fxn.gp_severitylabels

### functions ###

### import data ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

# d_wk[week] = seasonnum, d_incid[wk] = (child incid per 100,000, adult incid per 100,000, other incid per 100,000)
d_wk, d_incid = fxn.week_incidCA_processing(incid, pop)
# # d_attackCA_norm[seasonnum] = (norm C attack rate, norm A attack rate)
d_attackCA_norm = fxn.normalize_attackCA(d_wk, d_incid)

print d_attackCA_norm

# initialize figure
fig = plt.figure()

# bar chart of normalized child attack rates
ax = fig.add_subplot(2,1,1)

mild = ax.bar(mild_s, [d_attackCA_norm[k][0] for k in mild_s], bw, color=sevcol[0], align='center')
moderate = ax.bar(mod_s, [d_attackCA_norm[k][0] for k in mod_s], bw, color=sevcol[1], align='center')
severe = ax.bar(sev_s, [d_attackCA_norm[k][0] for k in sev_s], bw, color=sevcol[2], align='center')
# label formatting
# ax.set_ylabel('Percent Deviation from Baseline')
plt.gca().xaxis.set_major_locator(plt.NullLocator()) # hide xticks and xlabels
ax.hlines(y=0, xmin=0, xmax=10)
ax.legend([mild, moderate, severe], sevlab, loc='upper left')
ax.set_title('Child Attack Rate', fontsize=fs)
ax.set_xlim([1,10])
ax.set_ylim([-55,80])

# bar chart of normalized adult attack rates
ax = fig.add_subplot(2,1,2)

ax.bar(mild_s, [d_attackCA_norm[k][1] for k in mild_s], bw, color=sevcol[0], align='center')
ax.bar(mod_s, [d_attackCA_norm[k][1] for k in mod_s], bw, color=sevcol[1], align='center')
ax.bar(sev_s, [d_attackCA_norm[k][1] for k in sev_s], bw, color=sevcol[2], align='center')
# label formatting
ax.hlines(y=0, xmin=0, xmax=10)
ax.set_xticks(range(2,10))
ax.set_xticklabels(s_lab)
ax.set_title('Adult Attack Rate', fontsize=fs)
ax.set_xlim([1,10])
ax.set_ylim([-55,80])

# reduce space between subplots
plt.subplots_adjust(hspace=0.15)
# yaxis text, vertical alignment moves text towards center of two plots
plt.text(0.25, 15,'Percent Deviation from Baseline', va='bottom', rotation='vertical', fontsize=fssml)

# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F6/F6_attackCA_percdev_bipanel.png' , transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
