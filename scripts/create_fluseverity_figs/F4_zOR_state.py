#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/27/14
###Function: Draw mean retro zOR vs. state with all seasons together

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

### called/local plotting parameters ###
ps = fxn.pseasons
fs = 24
fssml = 12

### functions ###
def readStateClassifFile(state_file):
	dict_state_classif = {}
	for line in state_file:
		season, state = int(line[0]), str(line[1])
		mean_retro_zOR, mean_early_zOR = float(line[2]), float(line[3])
		dict_state_classif[(season, state)] = (mean_retro_zOR, mean_early_zOR)
	return dict_state_classif

def grabStateToRegion(state_reg_file):
	dict_state_region = {}
	for line in state_reg_file:
		state = str(line[5])
		region = int(line[8])
		dict_state_region[state] = region
	return dict_state_region

### data files ###
# state zOR data
st_zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classifications.csv', 'r')
st_zORin.readline()
st_zOR = csv.reader(st_zORin, delimiter=',')
# state to region number conversion
st_regin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
st_regin.readline()
st_reg = csv.reader(st_regin, delimiter=',')

### program ###
# nation-level peak-based retrospective classification 

## read state zOR data ##
# d_st_classif[(season, state abbr)] = (mean retro zOR, mean early zOR)
d_st_classif = readStateClassifFile(st_zOR)
# grab list of unique states in dataset
states = list(set([key[1] for key in d_st_classif]))

## read state to region data ##
# d_st_reg[state abbr] = region number
d_st_reg = grabStateToRegion(st_reg)

## region-color dictionary ##
# d_reg_col[region number] = str('color')
d_reg_col = dict(zip(range(1,11), cm.rainbow(np.linspace(0, 1, len(range(1,11))))))

# d_st_distr[state abbr] = [mean retro zOR S1, mean retrozOR S2, ...]
# d_st_median[state abbr] = median of mean retro zOR across seasons (masked NaNs)
for st in states:
	d_st_distr[st] = [d_st_classif[key][0] for key in d_st_classif if key[1] == st]
	dummymask = np.ma.array(d_st_distr[st], mask = np.isnan(d_st_distr[st]))
	d_st_distr_mask[st] = dummymask
	dummymedian = np.ma.median(dummymask)
	d_st_median[st] = dummymedian

# remove states with only masked medians from the dictionary
d_st_median_sub = dict((k, d_st_median[k]) for k in d_st_median if d_st_median[k])

# sort states by median of mean retro zOR across all seasons
sort_median_dict = sorted(d_st_median_sub.iteritems(), key=operator.itemgetter(1))
# grab list of sorted states for plotting
sorted_states = [item[0] for item in sort_median_dict]
# grab list of colors in order of sorted states -- each region is its own color
sorted_colors = [d_reg_col[d_st_reg[st]] for st in sorted_states]

# grab only unmasked values for boxplot
retrozOR_by_state = [[val for val in d_st_distr_mask[state].T if val] for state in sorted_states]

## draw figure ##
bxp = plt.boxplot(retrozOR_by_state, patch_artist=True) 
for patch, color in zip(bxp['boxes'], sorted_colors):
	patch.set_facecolor(color)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlim([0.5, 47.5])
plt.ylim([-4, 10])
plt.xticks(xrange(1, len(sorted_states)+1), sorted_states, rotation = 'vertical', fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F4/zOR_state_national.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

