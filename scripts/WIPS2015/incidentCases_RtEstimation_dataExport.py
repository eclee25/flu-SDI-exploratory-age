#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 2/3/15
###Function: Export incident ILI cases by week for total population in all service places

###Import data: SQL_export/OR_allweeks.csv, SQL_export/totalpop.csv

###Command Line: python 
##############################################

### notes ###

### packages/modules ###
import csv
from datetime import date
## local modules ##
import functions_v5 as fxn
### data structures ###

### functions ###
def export_totalILIcases(csv_incidence):
	dict_ILIage_week, dict_wk, dict_ILI_week = {},{},{}
	for row in csv_incidence: 
		week = row[1]
		Sun_dt = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		wk, seas, _ = fxn.SDIweek(Sun_dt) # Thu date, season, wknum
		dict_ILIage_week[(wk, str(row[2]))] = float(row[3])
		dict_wk[wk] = seas
	for wk in sorted(dict_wk):
		seas = dict_wk[wk]
		cases = sum([dict_ILIage_week.get((wk, age), 0) for age in ['C', 'A', 'O']])
		dict_ILI_week[(seas, wk)] = cases
	return dict_ILI_week

### data files ###
# incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
# incid = csv.reader(incidin, delimiter=',')
incid787in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient_zip787.csv', 'r')
incid787 = csv.reader(incid787in, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons

### program ###
d_ILI_week = export_totalILIcases(incid787)
for s in ps:
	filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/EpiEstim_totalILI_allLocs_787_S%s.csv' %(s)
	d_ILI_week_subset = dict((k, d_ILI_week[k]) for k in d_ILI_week if k[0]==s)
	dummyweeks = sorted([key[1] for key in d_ILI_week_subset])
	with open(filename, 'a') as f:
		for k,v in sorted(d_ILI_week_subset.iteritems()):
			f.write(str(k[0])) # season number
			f.write(',')
			f.write(str(k[1])) # week
			f.write(',')
			f.write(str(v)) # new cases
			f.write('\n')
