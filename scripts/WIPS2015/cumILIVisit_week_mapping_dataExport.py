#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 2/1/15
###Function: Export data to plot weekly cumulative ILI per 10,000 population map over the course of the season

###Import data: mapping_code/cleanedmapdata/zip3_incid_week.txt
###Export data: mapping_code/cleanedmapdata/zip3_cumILIVisit10000_week.txt

###Command Line: python cumILIVisit_week_mapping_dataExport.py
##############################################


### notes ###

### packages ###
import csv
import numpy as np
from datetime import date
## local packages ##
### data structures ###
### parameters ###
### functions ###
def import_week_data(filename):
	print 'running import_week_data'
	dict_zip3ILI_week, dict_zip3Pop_week, dict_wk = {},{},{}
	for row in filename:
		week, zip3 = str(row[1]), str(row[2])
		ili, popstat = int(row[3]), float(row[4])
		Sun_dt = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		wk, seas, _ = fxn.SDIweek(Sun_dt) # Thu date, season, wknum
		dict_zip3ILI_week[(wk, zip3)] = ili
		dict_zip3Pop_week[(wk, zip3)] = popstat 
		dict_wk[wk] = seas

	return dict_zip3ILI_week, dict_zip3Pop_week, dict_wk

def cumIncid_week_processing(dict_zip3ILI_week, dict_zip3Pop_week, dict_wk):
	print 'running cumIncid_week_processing'
	seasons = sorted(set(dict_wk.values()))
	zip3s = sorted(set([key[1] for key in dict_zip3ILI_week]))

	dict_cumILI_week = {}
	for s in seasons:
		dummyweeks = sorted([week for week in dict_wk if dict_wk[week] == s])
		for z in zip3s:
			orig_ILI_ls = [dict_zip3ILI_week.get((wk,z), 0) for wk in dummyweeks]
			cum_ILI_ls = list(np.cumsum(orig_ILI_ls))
			for week in dummyweeks:
				dict_cumILI_week[(week, z)] = cum_ILI_ls.pop(0)
	# calculate cumulative incidence
	dict_cumIncid_week = {}
	for key in dict_cumILI_week:
		zip3Pop = dict_zip3Pop_week.get(key, float('nan'))
		dict_cumIncid_week[key] = dict_cumILI_week[key]/zip3Pop * 10000

	return dict_cumILI_week, dict_cumIncid_week

### import data ###
iliin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/zip3_incid_week.txt','r')
iliin.readline() # move cursor beyond the header
ili=csv.reader(iliin, delimiter=',')

### program ###
d_zip3ILI_week, d_zip3Pop_week, d_wk = import_week_data(ili)
d_cumILI_week, d_cumIncid_week = cumIncid_week_processing(d_zip3ILI_week, d_zip3Pop_week, d_wk)

with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/zip3_cumILIVisit10000_week.txt', 'a') as f:
	for k,v in sorted(d_cumIncid_week.iteritems()):
		f.write(str(d_wk[k[0]])) # season number
		f.write(',')
		f.write(str(k[1])) # zip3
		f.write(',')
		f.write(str(k[0])) # week
		f.write(',')
		f.write(str(v)) # cumulative incidence per 10,000
		f.write(',')
		f.write(str(d_zip3Pop_week.get(k, float('nan')))) # zip3 population size
		f.write('\n')
