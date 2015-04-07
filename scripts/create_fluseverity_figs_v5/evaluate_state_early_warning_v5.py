#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/1/14
###Function: What is the distribution of state early warnings that match national classifications across the 2001-02 through 2008-09 seasons (state level peak based retro classification)?
# What is the distribution of region early warnings that match national classifications (region-lvl peak based retro classification)?
###Import data: 

###Command Line: python evaluation_state_early_warning_v5.py
##############################################


### notes ###

### packages/modules ###
import csv
from collections import defaultdict
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###
# d_nat[season] = (retrospective mean zOR, early warning mean zOR)
d_nat = {}

# state analysis
# d_st[(season, state)] = = (retrospective mean zOR, early warning mean zOR)
d_st = {}
# d_st_match[state] = [match S2, match S3, etc where match is represented as 1=match, 0=no match]
d_st_match_early = defaultdict(list) # early warning for state match retro for national
d_st_match_retro = defaultdict(list) # retro for state match retro for national
d_st_match_st2st = defaultdict(list) # early warning for state match early warning for national
# d_correct_by_season_[seasonnum] = (# correct states early warning, # correct states retrospective)
d_correct_by_season = {}

### functions ###
def function_operator(val):
	''' For each retrospective and early warning mean zOR, return -1 if the value is <-1, return 0 if the value is inclusive and between -1 and 1, and return 1 if the value is > 1.
	'''
	if val < -1:
		rtn_val = -1
	elif val >= -1 and val <= 1:
		rtn_val = 0
	elif val > 1:
		rtn_val = 1
	else: # zOR is float(nan)
		rtn_val = float('nan')
	return rtn_val

def apply_severity_code(d_mns):
	''' For a dictionary in the form dict[(season or season,region)] = (mn_retro zOR, mn_early zOR), return dict_codes[(season or season,region)] = (mn_retro code, mn_early code). 
	'''
	# d_codes[(season or season,region)] = (mn_retro code, mn_early code)
	# codes: 1 = severe, 0 = moderate, -1 = mild
	d_codes = {}
	for key in d_mns:
		d_codes[key] = tuple(map(function_operator, d_mns[key]))
	return d_codes	

def print_accuracy_to_file(dict_earlymatch, dict_retromatch, dict_statematch, state_list, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write('state,early_retro,retro_retro,early_retro_state\n')
		for state in state_list:
			er = sum(dict_earlymatch[state])
			rr = sum(dict_retromatch[state])
			# 2/23/15 some states in state_list may not be in dict_statematch since this data excludes early season early warning
			if state in dict_statematch:
				er_state = sum(dict_statematch[state])
			else:
				er_state = -99
			fwriter.write("%s,%s,%s,%s\n" % (state, er, rr, er_state))


### import data ###
# national level data: season, mn_retro, mn_early
natin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv','r')
natin.readline() # skip header
nat=csv.reader(natin, delimiter=',')
d_nat = fxn.readNationalClassifFile(nat)
# code national level data as mild (-1), moderate (0), or severe (1)
d_nat_codes = apply_severity_code(d_nat)

# state level data: season, state, mn_retro, mn_early, valid normweeks
stin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_7st.csv','r') 
stin.readline() # skip header
st=csv.reader(stin, delimiter=',')
d_st = fxn.readStateClassifFile(st)
# code state level data as mild (1), moderate (0), or severe (-1)
d_st_codes = apply_severity_code(d_st)

# state level data without early seasons: season, state, mn_retro, mn_early, valid normweeks
stWEin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_7st_withoutEarly.csv','r') 
stWEin.readline() # skip header
stWE=csv.reader(stWEin, delimiter=',')
d_stWE = fxn.readStateClassifFile(stWE)
# code state level data as mild (1), moderate (0), or severe (-1)
d_stWE_codes = apply_severity_code(d_stWE)

###########################
## dummylists ##
seasons = fxn.pseasons
states = sorted(list(set([key[1] for key in d_st]))) # list unique states

print 'Maine'
print [d_nat_codes[s] for s in seasons]
print [d_st_codes[(s, 'ME')] for s in seasons]

###########################
# with early seasons: match early warning at state level to retrospective at national level and retropsective at state level to retrospective at national level 
# use SDI_state_classif_covCareAdj_v5_7st.csv

# national retro classif
n_code = [d_nat_codes[s][0] for s in seasons]
ct = 0
for st in states:
	# include only states where all early warning and retrospective classifications are available 
	if sum(sum(np.isnan([d_st_codes[(s, st)] for s in seasons]))) == 0:
		ct += 1
		# state early warning classif
		st_code_early = [d_st_codes[(s, st)][1] for s in seasons]
		# state retrospective classif
		st_code_retro = [d_st_codes[(s, st)][0] for s in seasons]
		# d_st_match[state] = [match S2, match S3, etc where match is represented as 1=match, 0=no match]
		d_st_match_early[st] = [1  if retro==early else 0 for retro, early in zip(n_code, st_code_early)]
		d_st_match_retro[st] = [1  if r1==r2 else 0 for r1, r2 in zip(n_code, st_code_retro)]
		
		# print matches for state ew to nat retro, state retro to nat retro, and state ew to state retro
		print st, sum(d_st_match_early[st]), sum(d_st_match_retro[st])
	else:
		print st, np.isnan([d_st_codes[(s, st)] for s in seasons])
	
print 'with early seasons: %s of %s states have early and retro classif for all %s seasons' %(ct, len(states), len(seasons))

## check early warning state to retro national
# print [d_nat[key][0] for key in sorted(d_nat)]
# print [d_st[(key, 'NY')][1] for key in sorted(d_nat)]


###########################
# without early seasons: match early warning at state level to retrospective at state level
# use SDI_state_classif_covCareAdj_v5_7st_withoutEarly.csv

ct = 0
for st in states:
	# include only states where all early warning and retrospective classifications are available (2/11/15 except S4 early warning)
	if sum(sum(np.isnan([d_stWE_codes[(s, st)] for s in seasons]))) == 1:
		ct += 1
		# state early warning classif
		st_code_early = [d_stWE_codes[(s, st)][1] for s in seasons]
		# state retrospective classif
		st_code_retro = [d_stWE_codes[(s, st)][0] for s in seasons]
		# d_st_match_st2st[state] = [match state-early and state-retro S2, match S3, etc where match is represented as 1=match, 0=no match]
		d_st_match_st2st[st] = [1  if retro==early else 0 for retro, early in zip(st_code_retro, st_code_early)]
		# print matches for state ew to nat retro, state retro to nat retro, and state ew to state retro
		print st, sum(d_st_match_st2st[st])
	else:
		print st, np.isnan([d_stWE_codes[(s, st)] for s in seasons])
	
	
print 'without early seasons: %s of %s states have early and retro classif for all %s seasons' %(ct, len(states), len(seasons))

###########################
# find background accuracy rate across seasons (average number of states correct in each season)

# list states with data: with early seasons, without early seasons, union
incl_states = [st for st in d_st_match_early]
incl_statesWE = [st for st in d_st_match_st2st]

# d_correct_by_season_[seasonnum] = (# correct states early warning, # correct states retrospective)
for i, s in enumerate(seasons):
	st_early_matches = sum([d_st_match_early[st][i] for st in incl_states])
	st_retro_matches = sum([d_st_match_retro[st][i] for st in incl_states])
	st2st_matches = sum([d_st_match_st2st[st][i] for st in incl_statesWE])
	d_correct_by_season[s] = (st_early_matches, st_retro_matches, st2st_matches)

bg_rate_early = np.mean([d_correct_by_season[key][0]/float(len(incl_states)) for key in d_correct_by_season])
bg_rate_retro = np.mean([d_correct_by_season[key][1]/float(len(incl_states)) for key in d_correct_by_season])
bg_rate_st2st = np.mean([d_correct_by_season[key][2]/float(len(incl_statesWE)) for key in d_correct_by_season])

print 'bg rate early', bg_rate_early # 2/23/15: 0.3194
print 'bg rate retro', bg_rate_retro # 2/23/15: 0.5174
print 'bg rate st2st', bg_rate_st2st # 2/23/15: 0.3798

###########################
# print accuracy counts per state to file
fname = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_accuracy_counts_covCareAdj_v5.csv'
print_accuracy_to_file(d_st_match_early, d_st_match_retro, d_st_match_st2st, incl_states, fname)
