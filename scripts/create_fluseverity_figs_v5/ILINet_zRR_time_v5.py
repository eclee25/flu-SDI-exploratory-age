#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: RR of incidence in adults to incidence in children vs. week number normalized by the first 'gp_normweeks' of the season. Incidence in children and adults is normalized by the size of the child and adult populations in the second calendar year of the flu season. ILINet data
# 11/4 convert to v5: covCare adjustment, RR, a:c

###Import data: CDC_Source/Import_Data/all_cdc_source_data.csv, Census/Import_Data/totalpop_age_Census_98-14.csv

###Command Line: python ILINet_zRR_time_v5.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season
# 2013-14 ILINet data is normalized by estimated population size from December 2013 because 2014 estimates are not available at this time

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v5 as fxn

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
norm = fxn.gp_normweeks
fs = 24
fssml = 16

### program ###
# import data
d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.ILINet_week_RR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
d_indices = fxn.identify_retro_early_weeks(d_wk, d_totIncidAdj53ls)

# plot values
fig = plt.figure()
ax = plt.subplot(111)

for s, i in zip(ps, xrange(len(ps))):
	ax.plot(xrange(fw), d_zRR53ls[s][:fw], marker = fxn.gp_marker, color = colvec[i], label = sl[i], linewidth = fxn.gp_linewidth)
for s in ps:
	beg_retro, end_retro = d_indices[(s, 'r')]
	beg_early, end_early = d_indices[(s, 'e')]
	plt.plot(range(beg_retro, end_retro), d_zRR53ls[s][beg_retro:end_retro], marker = 'o', color = fxn.gp_retro_early_colors[0], linewidth = 2)
	plt.plot(range(beg_early, end_early), d_zRR53ls[s][beg_early:end_early], marker = 'o', color = fxn.gp_retro_early_colors[1], linewidth = 2)
plt.xlim([0, fw-1])
plt.xticks(range(fw)[::5], wklab[:fw:5]) 
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel(fxn.gp_sigmat, fontsize=fs)
# shrink current axis by 10%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width*0.9, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/ILINet/ILINet_zRR_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()