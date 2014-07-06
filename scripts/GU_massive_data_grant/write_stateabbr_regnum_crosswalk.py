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
import sys
from collections import defaultdict

## local modules ##
sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/create_fluseverity_figs')
import functions as fxn

### data structures ###
# d_regnum[HHS region number] = [state abbr 1, state abbr 2]
d_regnum = defaultdict(list)

### functions ###
def print_dregnum_to_file(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write('state,HHSregion\n')
		regionnum = range(1,11)
		for r in regionnum:
			for item in dic[r]:
				fwriter.write("%s,%s\n" % (item, r))

### import data ###

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

## write to file ##
fname_regnum = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/stateabbr_regnum_crosswalk.csv'
print_dregnum_to_file(d_regnum, fname_regnum)