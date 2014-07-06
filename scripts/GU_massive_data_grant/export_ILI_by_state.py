#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/30/2014
###Function: Export weekly incidence rate per 100,000 by state

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv

###Command Line: python export_ILI_by_state.py
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
from itertools import product

## local modules ##
sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/create_fluseverity_figs')
import functions as fxn

### data structures ###
# d_abbr[state abbreviation] = all lowercase state name
d_abbr = {}
# d_regnum[HHS region number] = [state abbr 1, state abbr 2]
d_regnum = defaultdict(list)
# d_AR_state[(seasonnum, state_abbr)] = attack rate for season-state per 100,000
d_AR_state = {}
# d_AR_region[(seasonnum, region)] = attack rate for season-region per 100,000 (summed by state)
d_AR_region = {}

### parameters ###
ps = fxn.gp_plotting_seasons
fw = fxn.gp_fluweeks

### functions ###
def print_dict_to_file(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write("season,region,AR100000\n")
		for key, value in dic.items():
			fwriter.write("%s,%s,%s\n" % (key[0], key[1], value))

### import data ###
reg_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
reg_incidin.readline()
regincid = csv.reader(reg_incidin, delimiter=',')
reg_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
reg_popin.readline()
regpop = csv.reader(reg_popin, delimiter=',')

### program ###

# HHS region number to state abbreviation
# does not include US territories, except DC
# d_regnum[HHS reg] = [state abbr1, state abbr2, etc]
d_regnum[1] = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']
d_regnum[2] = ['NY', 'NJ']
d_regnum[3] = ['DE', 'DC', 'MD', 'PA', 'VA', 'WV']
d_regnum[4] = ['AL', 'FL', 'GA', 'KY', 'MS', 'NC', 'SC', 'TN']
d_regnum[5] = ['IL', 'IN', 'MI', 'MN', 'OH', 'WI']
d_regnum[6] = ['AR', 'LA', 'NM', 'OK', 'TX']
d_regnum[7] = ['IA', 'KS', 'MO', 'NE']
d_regnum[8] = ['CO', 'MT', 'ND', 'SD', 'UT', 'WY']
d_regnum[9] = ['AZ', 'CA', 'HI', 'NV']
d_regnum[10] = ['AK', 'ID', 'OR', 'WA']

# dict_wk[week] = seasonnum, dict_incid53ls_state[(seasonnum, state abbr)] = [ILI wk 40, ILI wk 41,...],	dict_OR53ls_state[(seasonnum, state abbr)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_state[(seasonnum, state abbr)] = [zOR wk 40, zOR wk 41, ...]
d_wk, d_incid53ls_state, d_OR53ls_state, d_zOR53ls_state = fxn.week_plotting_dicts_state(regincid, regpop)

# 	d_AR_state[(seasonnum, state_abbr)] = attack rate for season-state per 100,000
for key in d_incid53ls_state:
	d_AR_state[key] = sum(d_incid53ls_state[key])

# d_AR_region[(seasonnum, region)] = attack rate for season-region per 100,000 (summed by state)
for snum, reg in product(ps, d_regnum):
	d_AR_region[(snum, reg)] = sum([d_AR_state[(snum, val)] for val in d_regnum[reg] if (snum, val) in d_AR_state])


# export data
fname_state = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/AR100000_state_season.csv'
fname_region = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/AR100000_region_season.csv'

print_dict_to_file(d_AR_state, fname_state)
print_dict_to_file(d_AR_region, fname_region)
