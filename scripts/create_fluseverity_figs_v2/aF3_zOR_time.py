#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/14/14
###Function: OR of incidence in adults to incidence in children vs. week number normalized by the first 'gp_normweeks' of the season. Incidence in children and adults is normalized by the size of the child and adult populations in the second calendar year of the flu season. 10/14/14 OR age flip.

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python aF3_zOR_time.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v2 as fxn

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

# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)

# plot values
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for s in ps:
	ax.plot(xrange(len(wklab)), d_zOR53ls[s], marker = 'o', color = colvec[s-2], label = sl[s-2], linewidth = 2)
ax.legend(loc='upper left')
ax.set_xticks(range(len(wklab))[::5])
ax.set_xticklabels(wklab[::5]) 
ax.set_xlim([0, fw-1])
ax.set_xlabel('Week Number', fontsize=fs)
ax.set_ylabel(fxn.gp_sigmat, fontsize=fs)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v2/F2/zOR_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# ## BIGGERSTAFF PRESENTATION PLOT ##
# # plot values
# for s in ps:
# 	plt.plot(xrange(fw), d_zOR53ls[s][:fw], marker = 'o', color = colvec[s-2], label = sl[s-2], linewidth = 2)
# # create dict with begin_retro and begin_early for each season?
# plt.xlim([0, fw-1])
# plt.xticks(range(fw)[::5], wklab[:fw:5]) 
# plt.xlabel('Week Number', fontsize=fs)
# plt.ylabel('zOR (%s week baseline)' % (norm), fontsize=fs)
# plt.legend(loc='upper left')
# # grey bar for approximate retrospective period
# plt.fill([15, 16, 16, 15], [-20, -20, 40, 40], facecolor='grey', alpha=0.4)
# # # grey bar for approximate early warning area
# # plt.fill([9, 10, 10, 9], [-20, -20, 40, 40], facecolor='grey', alpha=0.4)
# plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Presentations/Biggerstaff_2014_6_2/Figures/zOR_time_retro.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()




