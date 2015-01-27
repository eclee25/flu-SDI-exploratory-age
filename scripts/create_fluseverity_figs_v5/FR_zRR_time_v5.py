#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/18/15
###Function: (France data) normalized RR of incidence in adults to incidence in children vs. week number normalized by the first 'gp_normweeks' of the season. 

###Import data: Documents/FRANCE_ILI_DATA_2014/inc2_inc-tranche-fr_V2.csv

###Command Line: python FR_zRR_time_v5.py
##############################################

### notes ###
# France data is extrapolated to represent the entire nation and mean incidence estimates are used.

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v5 as fxn

### data structures ###
### functions ###
### data files ###
incidin = open('/home/elee/Documents/FRANCE_ILI_DATA_2014/inc2_inc-tranche-fr_V2.csv','r')
incidin.readline()
incid = csv.reader(incidin, delimiter=';')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
# sl = fxn.gp_FR_seasonlabels
# colvec = fxn.gp_FR_colors
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
norm = fxn.gp_normweeks
fs = 24
fssml = 16

### program ###
d_wk, d_totIncid53ls, d_ageIncid53ls = fxn.FR_week_RR_processing(incid)
d_RR53ls, d_zRR53ls = fxn.FR_week_RR_processing_part2(d_wk, d_ageIncid53ls)
# dict_indices[(snum, classif period)] = [wk index 1, wk index 2, etc.]
d_indices = fxn.identify_retro_early_weeks(d_wk, d_totIncid53ls)

# plot values
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ct=0
for s in ps:
	ax.plot(xrange(len(d_zRR53ls[s])), d_zRR53ls[s], marker = fxn.gp_marker, color = colvec[ct], label = sl[ct], linewidth = fxn.gp_linewidth)
	ct+=1
for s in ps:
	beg_retro, end_retro = d_indices[(s, 'r')]
	beg_early, end_early = d_indices[(s, 'e')]
	plt.plot(range(beg_retro, end_retro), d_zRR53ls[s][beg_retro:end_retro], marker = 'o', color = fxn.gp_retro_early_colors[0], linewidth = 4)
	plt.plot(range(beg_early, end_early), d_zRR53ls[s][beg_early:end_early], marker = 'o', color = fxn.gp_retro_early_colors[1], linewidth = 4)
ax.legend(loc='upper left', prop={'size':6})
ax.set_xticks(range(len(wklab))[::5])
ax.set_xticklabels(wklab[::5]) 
ax.set_xlim([0, fw])
ax.set_ylim([-6, 8])
ax.set_xlabel('Week Number', fontsize=fs)
ax.set_ylabel(fxn.gp_sigmat, fontsize=fs)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/FR/zRR_time_S2S9.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

