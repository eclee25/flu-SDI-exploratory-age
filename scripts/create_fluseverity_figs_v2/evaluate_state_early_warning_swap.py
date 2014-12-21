#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/15/14
###Function: What is the distribution of state early warnings that match national classifications across the 2001-02 through 2008-09 seasons (state level peak based retro classification)?
# What is the distribution of region early warnings that match national classifications (region-lvl peak based retro classification)?
# 10/15/14 age swap

###Import data: 

###Command Line: python evaluation_state_early_warning.py
##############################################


### notes ###


### packages/modules ###
import csv
from collections import defaultdict
import numpy as np

## local modules ##
import functions_v2 as fxn

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

## region analysis
# d_reg[(season, reg)] = = (retrospective mean zOR, early warning mean zOR)
d_reg = {}
# d_reg_match[reg] = [match S2, match S3, etc where match is represented as 1=match, 0=no match]
d_reg_match_early = defaultdict(list) # early warning for region match retro for national
d_reg_match_retro = defaultdict(list) # retro for region match retro for national
d_reg_match_r2r = defaultdict(list) # early warning for region match early warning for national
# d_correct_by_season_reg[seasonnum] = (# correct regions early warning, # correct regions retrospective)
d_correct_by_season_reg = {}

### parameters ###
nw = fxn.gp_normweeks

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
	# codes: -1 = mild, 0 = moderate, 1 = severe
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
			er_state = sum(dict_statematch[state])
			fwriter.write("%s,%s,%s,%s\n" % (state, er, rr, er_state))


### import data ###
# national level data: season, mn_retro, mn_early
natin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications_%s_swap.csv' %(nw),'r')
natin.readline() # skip header
nat=csv.reader(natin, delimiter=',')

# state level data: season, state, mn_retro, mn_early
stin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classifications_%sst_swap.csv' %(nw),'r') # 7/31/14: retrospective classif based on state incidence (instead of national incidence)
stin.readline() # skip header
st=csv.reader(stin, delimiter=',')

# region level data: season, state, mn_retro, mn_early
regin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_regional_classifications_%sreg_swap.csv' %(nw),'r') # 7/31/14: retrospective classif based on region incidence (instead of national incidence)
regin.readline() # skip header
reg=csv.reader(regin, delimiter=',')


### program ###
# import national level data
for line in nat:
	season = int(line[0])
	mn_retro = float(line[1])
	mn_early = float(line[2])
	# d_nat[season] = (retrospective mean zOR, early warning mean zOR)
	d_nat[season] = (mn_retro, mn_early)

# code national level data as mild (-1), moderate (0), or severe (1)
d_nat_codes = apply_severity_code(d_nat)

###########################
# import state level data
for line in st:
	season = int(line[0])
	state = str(line[1])
	mn_retro = float(line[2])
	mn_early = float(line[3])
	# d_st[(season, state)] = = (retrospective mean zOR, early warning mean zOR)
	d_st[(season, state)] = (mn_retro, mn_early)

# code state level data as mild (1), moderate (0), or severe (-1)
d_st_codes = apply_severity_code(d_st)

seasons = [key for key in sorted(d_nat)]
print 'seasons', seasons # should be in number order
states = sorted(list(set([key[1] for key in d_st]))) # list unique states

###########################
# import region level data
for line in reg:
	season = int(line[0])
	region = int(line[1])
	mn_retro = float(line[2])
	mn_early = float(line[3])
	# d_st[(season, state)] = = (retrospective mean zOR, early warning mean zOR)
	d_reg[(season, region)] = (mn_retro, mn_early)

# code state level data as mild (1), moderate (0), or severe (-1)
d_reg_codes = apply_severity_code(d_reg)

seasons = [key for key in sorted(d_nat)]
print 'seasons', seasons # should be in number order
regions = sorted(list(set([key[1] for key in d_reg]))) # list unique states

###########################
# match early warning at state level to retrospective at national level, retropsective at state level to retrospective at national level, and early warning at state level to retrospective at state level

for st in states:
	# national retro mean zOR
	n_code = [d_nat_codes[s][0] for s in seasons]
	# state early warning mean zOR
	st_code_early = [d_st_codes[(s, st)][1] for s in seasons]
	# state retrospective mean zOR
	st_code_retro = [d_st_codes[(s, st)][0] for s in seasons] 
	# d_st_match[state] = [match S2, match S3, etc where match is represented as 1=match, 0=no match]
	d_st_match_early[st] = [1  if retro==early else 0 for retro, early in zip(n_code, st_code_early)]
	d_st_match_retro[st] = [1  if r1==r2 else 0 for r1, r2 in zip(n_code, st_code_retro)]
	# d_st_match_st2st[state] = [match state-early and state-retro S2, match S3, etc where match is represented as 1=match, 0=no match]
	d_st_match_st2st[st] = [1  if retro==early else 0 for retro, early in zip(st_code_retro, st_code_early)]
	
	# print state accuracy for early warning & retro to national, and early warning & retro at state level
	print st, sum(d_st_match_early[st]), sum(d_st_match_retro[st]), sum(d_st_match_st2st[st])

	## checks
	# print 'nat', n_code
	# print 'state', st_code
	# print st, d_st_match[st]

## checks
# print [d_nat[key][0] for key in sorted(d_nat)]
# print [d_st[(key, 'NY')][1] for key in sorted(d_nat)]


###########################
# find background accuracy rate across seasons (average number of states correct in each season)

# d_correct_by_season_[seasonnum] = (# correct states early warning, # correct states retrospective)
for i in range(len(seasons)):
	d_correct_by_season[i+2] = (sum([d_st_match_early[st][i] for st in states]), sum([d_st_match_retro[st][i] for st in states]))

bg_rate_early = np.mean([d_correct_by_season[key][0]/float(len(states)) for key in d_correct_by_season])
bg_rate_retro = np.mean([d_correct_by_season[key][1]/float(len(states)) for key in d_correct_by_season])

print 'bg rate early', bg_rate_early
print 'bg rate retro', bg_rate_retro


###########################
# match early warning at region level to retrospective at national level, retropsective at region level to retrospective at national level, and early warning at region level to retrospective at region level

for reg in regions:
	# national retro mean zOR
	n_code = [d_nat_codes[s][0] for s in seasons]
	# reg early warning mean zOR
	reg_code_early = [d_reg_codes[(s, reg)][1] for s in seasons]
	# reg retrospective mean zOR
	reg_code_retro = [d_reg_codes[(s, reg)][0] for s in seasons] 
	# d_reg_match[reg] = [match S2, match S3, etc where match is represented as 1=match, 0=no match]
	d_reg_match_early[reg] = [1  if retro==early else 0 for retro, early in zip(n_code, reg_code_early)]
	d_reg_match_retro[reg] = [1  if r1==r2 else 0 for r1, r2 in zip(n_code, reg_code_retro)]
	# d_reg_match_r2r[reg] = [match reg-early and reg-retro S2, match S3, etc where match is represented as 1=match, 0=no match]
	d_reg_match_r2r[reg] = [1  if retro==early else 0 for retro, early in zip(reg_code_retro, reg_code_early)]
	
	# print state accuracy for early warning & retro to national, and early warning & retro at state level
	print reg, sum(d_reg_match_early[reg]), sum(d_reg_match_retro[reg]), sum(d_reg_match_r2r[reg])


###########################
# find background accuracy rate across seasons (average number of regions correct in each season)

# d_correct_by_season_[seasonnum] = (# correct states early warning, # correct states retrospective)
for i in range(len(seasons)):
	d_correct_by_season_reg[i+2] = (sum([d_reg_match_early[reg][i] for reg in regions]), sum([d_reg_match_retro[reg][i] for reg in regions]))

bg_rate_early = np.mean([d_correct_by_season_reg[key][0]/float(len(states)) for key in d_correct_by_season_reg])
bg_rate_retro = np.mean([d_correct_by_season_reg[key][1]/float(len(states)) for key in d_correct_by_season_reg])

print 'bg rate early region', bg_rate_early
print 'bg rate retro region', bg_rate_retro



###########################
# print accuracy counts per state to file
fname = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_accuracy_counts_stlvl_swap.csv'
print_accuracy_to_file(d_st_match_early, d_st_match_retro, d_st_match_st2st, states, fname)

###########################
# print accuracy counts per reg to file
fname = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_region_accuracy_counts_reglvl_swap.csv'
print_accuracy_to_file(d_reg_match_early, d_reg_match_retro, d_reg_match_r2r, regions, fname)
