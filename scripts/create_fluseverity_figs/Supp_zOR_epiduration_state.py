#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/1/14
###Function: scatter plot zOR metrics vs. epidemic duration at state level, using the state peak retrospective classification
## one plot per season per classification period vs. epidemic duration
## a single plot for all seasons for retrospective period vs. epidemic duration
## define epidemic duration as the number of weeks that falls between the point in the epidemic where cumulative incidence is 20% and 80% cumulative incidence (inclusive)

###Import data: Py_export/SDI_state_classifications_7st.csv, R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv

###Command Line: python Supp_zOR_epiduration_state.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt


## local modules ##
import functions as fxn

### data structures ###


### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
fw = fxn.gp_fluweeks
wklab = fxn.gp_weeklabels
scol = fxn.gp_colors

epi_min_perc = 10 # cumulative incidence percentage that defines beginning of epidemic
epi_max_perc = 90 # cumulative incidence percentage that defines end of epidemic

### functions ###

### data files ###

# state zOR data
st_zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classifications_7st.csv', 'r')
st_zORin.readline()
st_zOR = csv.reader(st_zORin, delimiter=',')
# state incidence files
st_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
st_incidin.readline()
stincid = csv.reader(st_incidin, delimiter=',')
st_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
st_popin.readline()
stpop = csv.reader(st_popin, delimiter=',')

### program ###
# import state classification data
# d_st_classif[(season, state abbr)] = (mean retro zOR, mean early zOR)
d_st_classif = fxn.readStateClassifFile(st_zOR)
# grab list of unique states in dataset
states = list(set([key[1] for key in d_st_classif]))


## state-level data ##
d_wk, d_zip3_st, d_incid_st, d_OR_st = fxn.week_OR_processing_state(stincid, stpop)
# dict_zOR_st[(week, state)] = zOR
d_zOR_st = fxn.week_zOR_processing_state(d_wk, d_OR_st)
# dict_incid53ls_st[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_st[(seasonnum, state)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_st[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls_st, d_OR53ls_st, d_zOR53ls_st = fxn.week_plotting_dicts_state(d_wk, d_incid_st, d_OR_st, d_zOR_st)

# plot values per season
for s in ps:
	retrozOR = [d_st_classif[(s, st)][0] for st in states]
	earlyzOR = [d_st_classif[(s, st)][1] for st in states]
	epidur = [fxn.epidemic_duration(d_incid53ls_st[(s, st)], epi_min_perc, epi_max_perc) for st in states]

	# mean retro zOR vs peak timing
	plt.plot(epidur, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
	for st, x, y in zip(states, epidur, retrozOR):
		plt.annotate(st, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
	plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
	plt.xlabel('Epidemic Duration (number of weeks), Season %s' %(s), fontsize=fs)
	plt.xticks(range(fw)[::5], fontsize=fssml)
	plt.yticks(fontsize=fssml)
	plt.xlim([0,fw])
	plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_epidur_state/zOR_retro_epidur_state_Season%s.png' %(s), transparent=False, bbox_inches='tight', pad_inches=0)
	plt.close()
	# plt.show()

	# mean retro zOR vs peak timing
	plt.plot(epidur, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
	for st, x, y in zip(states, epidur, earlyzOR):
		plt.annotate(st, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
	plt.ylabel('Mean Early Warning zOR', fontsize=fs) 
	plt.xlabel('Epidemic Duration (number of weeks), Season %s' %(s), fontsize=fs)
	plt.xticks(range(fw)[::5], fontsize=fssml)
	plt.yticks(fontsize=fssml)
	plt.xlim([0,fw])
	plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_epidur_state/zOR_early_epidur_state_Season%s.png' %(s), transparent=False, bbox_inches='tight', pad_inches=0)
	plt.close()
	# plt.show()

# mean retro zOR vs timing -- all seasons on a single plot
for s, col, lab in zip(ps, scol, sl):
	retrozOR = [d_st_classif[(s, st)][0] for st in states]
	epidur = [fxn.epidemic_duration(d_incid53ls_st[(s, st)], epi_min_perc, epi_max_perc) for st in states]
	plt.plot(epidur, retrozOR, marker = 'o', color = col, label = lab, linestyle = 'None')
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('Epidemic Duration (number of weeks)', fontsize=fs)
plt.xticks(range(fw)[::5], fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.legend(loc='upper left')
plt.xlim([0,fw])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_epidur_state/zOR_retro_epidur_state_allseas.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()