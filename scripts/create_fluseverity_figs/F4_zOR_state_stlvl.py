#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/27/14
###Function: Draw mean retro zOR vs. state with all seasons together. Classify retrospective index according to peak week in state time series.
### 8/20/14: Draw same barplot comparing state index to national index. Which states are the most severe/mild across all seasons (state index - national index)/abs(national index). If state is milder than nation --> positive; if state is more severe than nation --> negative.

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python F4_zOR_region.py
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
import functions as fxn

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
def grabStateToRegion(state_reg_file):
	dict_state_region = {}
	for line in state_reg_file:
		state = str(line[5])
		region = int(line[8])
		dict_state_region[state] = region
	return dict_state_region

def relative_to_national(dict_st_classif, dict_nat_classif):
	''' For each state-season combination, compute (state retro - national retro)/abs(national retro) values. Positive values indicate the state experiences milder severity than the nation. Negative values indicate the state experiences greater severity than the nation.
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

### data files ###
# state zOR data
st_zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classifications_7st.csv', 'r')
st_zORin.readline()
st_zOR = csv.reader(st_zORin, delimiter=',')
# state to region number conversion
st_regin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
st_regin.readline()
st_reg = csv.reader(st_regin, delimiter=',')
# national zOR data
nat_zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications.csv', 'r')
nat_zORin.readline()
nat_zOR = csv.reader(nat_zORin, delimiter=',')

### program ###
# state-level peak-based retrospective classification 

## read state zOR data ##
# d_st_classif[(season, state abbr)] = (mean retro zOR, mean early zOR)
d_st_classif = fxn.readStateClassifFile(st_zOR)
# grab list of unique states in dataset
states = list(set([key[1] for key in d_st_classif]))

## read state to region data ##
# d_st_reg[state abbr] = region number
d_st_reg = grabStateToRegion(st_reg)

## region-color dictionary ##
# d_reg_col[region number] = str('color')
d_reg_col = dict(zip(range(1,11), cm.rainbow(np.linspace(0, 1, len(range(1,11))))))

## read national zOR data ##
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_nat_classif = fxn.readNationalClassifFile(nat_zOR)

#### processing for deviation in state and national zOR boxplot ####
# d_st_deviation[(season, state)] = relative deviation between state and national classification (retro, early) classifications
d_st_deviation = relative_to_national(d_st_classif, d_nat_classif)


#### processing for both plots ####

# d_st_distr[state abbr] = [mean retro zOR S1, mean retrozOR S2, ...]
# d_st_median[state abbr] = median of mean retro zOR across seasons (masked NaNs)
# d_st_devls[state abbr] = [dev retro S1, dev retro S2, ...]
# d_st_median2[state abbr] = median of deviation in mean retro zOR across seasons (masked NaNs)
for st in states:
	d_st_distr[st] = [d_st_classif[key][0] for key in sorted(d_st_classif) if key[1] == st]
	dummymask = np.ma.array(d_st_distr[st], mask = np.isnan(d_st_distr[st]))
	d_st_distr_mask[st] = dummymask
	dummymedian = np.ma.median(dummymask) # medians based on retrozOR
	d_st_median[st] = dummymedian
	d_st_devls[st] = [d_st_deviation[key][0] for key in sorted(d_st_deviation) if key[1] == st]
	dummymask2 = np.ma.array(d_st_devls[st], mask = np.isnan(d_st_devls[st]))
	d_st_devls_mask[st] = dummymask2
	dummymedian2 = np.ma.median(dummymask2) # medians based on deviation in retrozOR
	d_st_median2[st] = dummymedian2

## sort mean retrospective zOR medians ##
# remove states with only masked medians from the dictionary
d_st_median_sub = dict((k, d_st_median[k]) for k in d_st_median if d_st_median[k])
# sort states by median of mean retro zOR across all seasons
sort_median_dict = sorted(d_st_median_sub.iteritems(), key=operator.itemgetter(1))
# grab list of sorted states for plotting
sorted_states = [item[0] for item in sort_median_dict]
# grab list of colors in order of sorted states -- each region is its own color
sorted_colors = [d_reg_col[d_st_reg[st]] for st in sorted_states]
# grab only unmasked values for zOR boxplot
retrozOR_by_state = [[val for val in d_st_distr_mask[state].T if val] for state in sorted_states]

## sort deviation in mean retrospective zOR medians ##
# remove states with only masked medians from the dictionary
d_st_median_sub2 = dict((k, d_st_median2[k]) for k in d_st_median2 if d_st_median2[k])
# sort states by median of deviation in mean retro zOR across all seasons
sort_median_dict2 = sorted(d_st_median_sub2.iteritems(), key=operator.itemgetter(1))
# grab list of sorted states for plotting
sorted_states2 = [item[0] for item in sort_median_dict2]
# grab list of colors in order of sorted states -- each region is its own color
sorted_colors2 = [d_reg_col[d_st_reg[st]] for st in sorted_states2]
# grab only unmasked values for deviation boxplot
retroDev_by_state = [[val for val in d_st_devls_mask[state].T if val] for state in sorted_states2]

## 9/17/14 colors by state identity ##
# GU-SRD14 presentation #
severe_states = ['VA', 'NC', 'SC', 'WY']
mild_states = ['OR', 'CA']
# highlight relatively mild/severe state finding
sorted_colors3 = ['r' if st in severe_states else ('b' if st in mild_states else '0.85') for st in sorted_states2] 


print d_st_distr_mask['WY']
print d_st_devls_mask['WY']
print [d_nat_classif[s][0] for s in ps]

## draw state zOR boxplot ##
bxp = plt.boxplot(retrozOR_by_state, patch_artist=True) 
for patch, color in zip(bxp['boxes'], sorted_colors):
	patch.set_facecolor(color)
plt.ylabel(fxn.gp_sigma_r, fontsize=fs)
plt.xlim([0.5, 47.5])
plt.ylim([-4, 10])
plt.xticks(xrange(1, len(sorted_states)+1), sorted_states, rotation = 'vertical', fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F4/zOR_state_state.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

## draw deviation bw state and nat retro boxplot (sorted by retrozOR) ##
# severest states: (greatest average deviation below 0, rank order severest) DC, ID, MS, NJ, CT, WV, VA, AL
# mildest states: (greatest average deviation above 0, rank order mildest) WA, OR, CA, VT
bxp2 = plt.boxplot(retroDev_by_state, patch_artist=True) 
for patch, color in zip(bxp2['boxes'], sorted_colors2):
	patch.set_facecolor(color)
plt.axhline(y=0, color='k')
plt.ylabel(r'Deviation from National $\bar{\sigma_{r}}$', fontsize=fs)
plt.xlim([0.5, 47.5])
plt.xticks(xrange(1, len(sorted_states2)+1), sorted_states2, rotation = 'vertical', fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.ylim([-3.5,3.5])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F4/zOR_state_state_deviation.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# for sorted_colors3 plot
# plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Presentations/GU-SRD_2014_9_18/Figures/zOR_state_state_deviation.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()
