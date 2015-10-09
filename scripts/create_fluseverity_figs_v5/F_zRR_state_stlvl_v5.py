#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/1/14
###Function: Draw mean retro zOR vs. state with all seasons together. Classify retrospective index according to peak week in state time series.
### 8/20/14: Draw same barplot comparing state index to national index. Which states are the most severe/mild across all seasons (state index - national index)/abs(national index). If state is milder than nation --> positive; if state is more severe than nation --> negative.
# 11/7/14: care-seeking for ILI = age-specific estimate for state in 2009-10 BRFSS; states with missing data are filled in with the corresponding census region's age-specific estimate
# 7/21/15: update notation, colors
# 7/30/15: update state notation
# 10/8/15: rm lines, overline

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python F_zRR_state_stlvl_v5.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from collections import defaultdict
import operator
import matplotlib.cm as cm

## local modules ##
import functions_v5 as fxn

### data structures ###
# d_st_distr[state abbr] = [mean retro zOR S1, mean retrozOR S2, ...]
d_st_distr = defaultdict(list)
# d_st_distr_mask[state abbr] = [mean retro zOR S1, mean retrozOR S2, ...], where NaNs are masked
d_st_distr_mask = defaultdict(list)
# d_st_median[state abbr] = median of mean retro zOR across all seasons for a given state, where NaN is removed from median calculation
d_st_median = {}
# d_reg_col[region number] = str('color')
d_reg_col = {}
# d_st_devls[state abbr] = [dev retro S1, dev retro S2, ...]
d_st_devls = defaultdict(list)
# d_st_devls_mask[state abbr] = [dev retro S1, dev retro S2, ...], where NaNs are masked
d_st_devls_mask = defaultdict(list)
# d_st_median2[state abbr] = median of deviation in mean retro zOR across all seasons for a given state, where NaN is removed from median calculation
d_st_median2 = {}

### called/local plotting parameters ###
ps = fxn.pseasons
fs = 24
fssml = 12

### functions ###
def relative_to_national(dict_st_classif, dict_nat_classif):
	''' For each state-season combination, compute (state retro - national retro)/abs(national retro) values. Positive values indicate the state experiences greater severity than the nation. Negative values indicate the state experiences milder severity than the nation.
	'''
	states = list(set([key[1] for key in dict_st_classif]))
	seasons = sorted([key for key in dict_nat_classif])
	# dict_st_deviation[(season, state)] = (retro dev from nat, early dev from nat)
	dict_st_deviation = {}

	for key in dict_st_classif:
		snum = key[0]
		stclassif_retro, stclassif_early = dict_st_classif[key] # state zOR
		natclassif_retro, natclassif_early = dict_nat_classif[snum] # nat zOR in same season
		relative_deviation_retro = (stclassif_retro - natclassif_retro)/abs(natclassif_retro)
		relative_deviation_early = (stclassif_early - natclassif_early)/abs(natclassif_early)
		dict_st_deviation[key] = (relative_deviation_retro, relative_deviation_early)

	return dict_st_deviation

def identify_state_deviation_colors(dict_st_devls_mask):
	''' Identify which states may be colored as being more severe or more mild than other states across study seasons. Severe or mild means 75% of data points were above or below deviation = 0. Moderately more severe or more mild means 70% of data points were above or below deviation = 0.
	'''
	severe_states, almostsevere_states = [],[]
	mild_states, almostmild_states = [],[]
	
	# identify which states may be severer or milder relative to all other states
	for state in dict_st_devls_mask:
		q25, q30, q70, q75 = np.percentile(dict_st_devls_mask[state], [25, 30, 70, 75])
		if q25 >= 0:
			severe_states.append(state)
		elif q30 >= 0:
			almostsevere_states.append(state)
		elif q75 <= 0:
			mild_states.append(state)
		elif q70 <= 0:
			almostmild_states.append(state)

		print state, q25, q30, q70, q75

	return severe_states, almostsevere_states, mild_states, almostmild_states


### data files ###
# state zOR data
st_zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_7st.csv', 'r')
st_zORin.readline()
st_zOR = csv.reader(st_zORin, delimiter=',')
# national zOR data
nat_zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv', 'r')
nat_zORin.readline()
nat_zOR = csv.reader(nat_zORin, delimiter=',')

### program ###
# state-level peak-based retrospective classification 

## read state zOR data ##
# d_st_classif[(season, state abbr)] = (mean retro zOR, mean early zOR)
d_st_classif = fxn.readStateClassifFile(st_zOR)
# grab list of unique states in dataset
states = list(set([key[1] for key in d_st_classif]))

## read national zOR data ##
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_nat_classif = fxn.readNationalClassifFile(nat_zOR)

#### processing for deviation in state and national zOR boxplot ####
# d_st_deviation[(season, state)] = relative deviation between state and national classification (retro, early) classifications
d_st_deviation = relative_to_national(d_st_classif, d_nat_classif)


#### processing for both plots ####

# d_st_distr[state abbr] = [mean retro zOR S1, mean retrozOR S2, ...]
# d_st_median[state abbr] = median of mean retro zOR across seasons
# d_st_devls[state abbr] = [dev retro S1, dev retro S2, ...]
# d_st_median2[state abbr] = median of deviation in mean retro zOR across seasons (masked NaNs)
ct = 0
for st in states:
	dummyclassif = [d_st_classif[key][0] for key in sorted(d_st_classif) if key[1] == st]
	# plot data for states where data is available for all seasons
	if sum(np.isnan(dummyclassif)) == 0:
		ct += 1
		d_st_distr_mask[st] = dummyclassif
		d_st_median[st] = np.median(dummyclassif)
		dummydeviation = [d_st_deviation[key][0] for key in sorted(d_st_deviation) if key[1] == st]
		d_st_devls_mask[st] = dummydeviation
		d_st_median2[st] = np.median(dummydeviation)

print '%s of %s states have data for all %s seasons' %(ct, len(states), len(ps))

## severity index bxp sort by median ## 
# sort states by median of mean retro zRR across all seasons
sort_median_dict = sorted(d_st_median.iteritems(), key=operator.itemgetter(1))
# grab list of sorted states for plotting
sorted_states = [item[0] for item in sort_median_dict]
# grab values for index boxplot
retrozOR_by_state = [[val for val in d_st_distr_mask[state]] for state in sorted_states]

## deviation bxp sort by median ##
# sort states by median of deviation in mean retro zOR across all seasons
sort_median_dict2 = sorted(d_st_median2.iteritems(), key=operator.itemgetter(1))
# grab list of sorted states for plotting
sorted_states2 = [item[0] for item in sort_median_dict2]
# grab values for deviation boxplot
retroDev_by_state = [[val for val in d_st_devls_mask[state]] for state in sorted_states2]

## 11/1/14: highlight severe states ##
sev_st, asev_st, mild_st, amild_st = identify_state_deviation_colors(d_st_devls_mask)

print sev_st, asev_st, mild_st, amild_st

# highlight severe state finding
sorted_colors_ix = ['r' if st in sev_st else ('#abd9e9' if st in amild_st else ('#FFA07A' if st in asev_st else ('b' if st in mild_st else '0.85'))) for st in sorted_states] 
sorted_colors_dev = ['r' if st in sev_st else ('#abd9e9' if st in amild_st else ('#FFA07A' if st in asev_st else ('b' if st in mild_st else '0.85'))) for st in sorted_states2] 

print 'nat classif', [d_nat_classif[s][0] for s in ps]

## draw state zOR boxplot ##
bxp = plt.boxplot(retrozOR_by_state, patch_artist=True) 
for patch, color in zip(bxp['boxes'], sorted_colors_ix):
	patch.set_facecolor(color)
plt.ylabel(fxn.gp_sigma_r_st, fontsize=fs)
plt.xlim([0.5, 37.5])
plt.ylim([-8, 8])
plt.xticks(xrange(1, len(sorted_states)+1), sorted_states, rotation = 'vertical', fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_state_state.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

## draw deviation bw state and nat retro boxplot (sorted by retrozOR) ##
# severest states: (greatest average deviation above 0, rank order severest) 
# mildest states: (greatest average deviation below 0, rank order mildest) 
bxp2 = plt.boxplot(retroDev_by_state, patch_artist=True) 
for patch, color in zip(bxp2['boxes'], sorted_colors_dev):
	patch.set_facecolor(color)
plt.axhline(y=0, color='k')
plt.ylabel(r'Deviation of $\overline{\rho_{s,r}(\tau)}$ from $\overline{\rho_{s,r}}$', fontsize=fs)
plt.xlim([0.5, 37.5])
plt.xticks(xrange(1, len(sorted_states2)+1), sorted_states2, rotation = 'vertical', fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.ylim([-4,4])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/MainFigures/zRR_state_state_deviation.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

