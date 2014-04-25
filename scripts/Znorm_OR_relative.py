#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/9/14
###Function: calculate average z-ORs where the early warning and classification periods are defined as relative dates
## early warning period begins on the week after Thanksgiving and the two subsequent weeks (see My's data file: ThanksgivingWeekData_Revised.csv)
## retrospective period is based on the first two weeks of the beginning of the epidemic period (this will have to be decided from incidence charts? a file with the week data should probably be created)
### base Znorm_OR.py description
## Z-normalize (subtract mean and divide by SD) OR time series -- time series with average values greater than 1 during the classification periods are mild seasons -- time series with average values less than -1 during the classification periods are severe seasons
## Z-normalize OR time series based on mean and SD of first 7 or 10 weeks of flu season -- can first 7 or 10 weeks tell you about severity of flu season in first few weeks of second year?

###Import data: 

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import defaultdict


## local modules ##
import ORgenerator as od

### data structures ###
# ORdict_znorm[week] = OR_znorm
ORdict_znorm = {} # all data
ORdict_znorm2 = {} # offices/OP only
# retrodict[season] = [retro period week date 1, retro period week date 2, ...]
retrodict_cum = defaultdict(list)
retrodict_pk = defaultdict(list)
retrodict_cum2 = defaultdict(list)
retrodict_pk2 = defaultdict(list)

### parameters ###
USchild = 20348657 + 20677194 + 22040343 # US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 # US adult popn from 2010 Census
seasons = range(2,11) # seasons for which ORs will be generated
# Season 2 = 2001-2, Season 3 = 2002-3, etc
normwks = 7 # normalize by weeks 40-47 in season
early_period = 2 # early warning period endures 2 weeks starting with the week after Thanksgiving
retro_period = 2 # retrospective period endures 2 weeks at beginning of epidemic


### functions ###

### import data ###
datain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
data=csv.reader(datain, delimiter=',')
# 4/23/14 added outpatient data
data2in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
data2=csv.reader(data2in, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')


### program ###

ilidict, wkdict, weeks = od.import_dwk(data, 0, 1, 2, 3)
# ilidict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
ORdict, ARdict = od.ORgen_wk(ilidict, weeks)
# ORdict[week] = OR
# ARdict[week] = attack rate per 10000
Thxdict = od.import_relative_early_period(thanks, 14, 13)
# Thxdict[seasonnum] = Sunday of Thanksgiving week date


# offices/op data only
ilidict2, wkdict2, weeks = od.import_dwk(data2, 0, 1, 2, 3)
# ilidict2[(week, age marker)] = ILI
# wkdict2[week] = seasonnum
ORdict2, ARdict2 = od.ORgen_wk(ilidict2, weeks)
# ORdict2[week] = OR
# ARdict2[week] = attack rate per 10000


## processing step: z-normalization ##
for s in seasons:
	# wkdummy will represent list of weeks in season to use as key for OR dict
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = list(sorted(set(wkdummy)))
	s_mean = np.mean([ORdict[wk] for wk in sorted(wkdummy)[:normwks]])
	s_sd = np.std([ORdict[wk] for wk in sorted(wkdummy)[:normwks]])
	dictdummyls = [(ORdict[wk]-s_mean)/s_sd for wk in sorted(wkdummy)]
	for w, z in zip(sorted(wkdummy), dictdummyls):
		ORdict_znorm[w] = z
	
	# dictionary with retro period weeks for each season
	print 'season', s
	retrodict_cum[s] = od.import_relative_retro_period(wkdummy, ARdict, .15, 'cum_incid', retro_period) # cumulative incidence is difficult because it is over the course of the entire flu season; if considering only the main epidemic period, any value before 0.15 should be in the growth phase of the epidemic
	retrodict_pk[s] = od.import_relative_retro_period(wkdummy, ARdict, 3, 'peak_wk', retro_period) # 2 wks prior to the peak week is safely within the growth phase of the epidemic curve
	
	# offices/op data
	s_mean2 = np.mean([ORdict2[wk] for wk in sorted(wkdummy)[:normwks]])
	s_sd2 = np.std([ORdict2[wk] for wk in sorted(wkdummy)[:normwks]])
	dictdummyls2 = [(ORdict2[wk]-s_mean2)/s_sd2 for wk in sorted(wkdummy)]
# 	print 'Office data: s_mean, s_sd, s_cv:', s_mean2, s_sd2, s_sd2/s_mean2
	for w, z in zip(sorted(wkdummy), dictdummyls2):
		ORdict_znorm2[w] = z
	
	# dictionary with retro period weeks for each season, office/op data 
	retrodict_cum2[s] = od.import_relative_retro_period(wkdummy, ARdict2, .15, 'cum_incid', retro_period) # cumulative incidence is difficult because it is over the course of the entire flu season; if considering only the main epidemic period, any value before 0.15 should be in the growth phase of the epidemic
	retrodict_pk2[s] = od.import_relative_retro_period(wkdummy, ARdict2, 3, 'peak_wk', retro_period) # 2 wks prior to the peak week is safely within the growth phase of the epidemic curve

# # all data
# # open file to write zOR averages
# # fwriter = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/zOR_avgs_relative.csv', 'w+')
# # fwriter.write('season,retro_mn,early_mn\n')
#
# # add 53rd week to season data if needed
# for s in seasons: 
# 	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
# 	wkdummy = list(sorted(set(wkdummy)))
# 	if s == 1:
# 		chartORs = [ORdict_znorm[wk] for wk in sorted(wkdummy)]
# 		chartwks = xrange(13, 13 + len(sorted(wkdummy)))
# 		print "season number and num weeks", s, len(wkdummy), len(chartORs)
# 	elif len(wkdummy) == 53:
# 		chartORs = [ORdict_znorm[wk] for wk in sorted(wkdummy)]
# 		chartwks = xrange(len(sorted(wkdummy)))
# 		print "season number and num weeks", s, len(wkdummy),  len(chartORs)
# 	else:
# 		chartORs = [ORdict_znorm[wk] for wk in sorted(wkdummy)]
# 		avg53 = (chartORs[12] + chartORs[13])/2
# 		chartORs.insert(13, avg53)
# 		chartwks = xrange(len(sorted(wkdummy)) + 1)
# 		print "season number and num weeks", s, len(wkdummy),  len(chartORs)
# 		
# 	# processing: grab average z-OR during early warning and retrospective periods (after adding week 53 to all seasons)
# # 	class_mn = 
# 	# early warning period is week after Thanksgiving week plus 1 subsequent week
# 	early_mn = np.mean([ORdict_znorm[wk] for wk in sorted(wkdummy) if wk > Thxdict[s]][1:early_period+1])
# 	# retrospective period may be defined as the two week period after x% cumulative incidence is surpassed or the two week period starting x weeks prior to peak incidence week
# 	retro_mn_cum = np.mean([ORdict_znorm[wk] for wk in retrodict_cum[s]])
# 	retro_mn_pk = np.mean([ORdict_znorm[wk] for wk in retrodict_pk[s]])
# 	
# 	# view results in terminal
# 	print 'season', s, early_mn, retro_mn_cum, retro_mn_pk
#
# # 	
# # 	fwriter.write('%s,%s,%s\n' % (s, retro_mn_pk, early_mn))
# # fwriter.close()

# office/OP data
# open file to write zOR averages
# fwriter = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/zOR_avgs_relative_outpatient.csv', 'w+')
# fwriter.write('season,retro_mn,early_mn\n')

# add 53rd week to season data if needed
for s in seasons: 
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = list(sorted(set(wkdummy)))
	if s == 1:
		chartORs = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(13, 13 + len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy), len(chartORs)
	elif len(wkdummy) == 53:
		chartORs = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy),  len(chartORs)
	elif s == 9:
		chartOR_dummy = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		avg53 = (chartOR_dummy[12] + chartOR_dummy[13])/2
		chartOR_dummy.insert(13, avg53)
		chartORs = chartOR_dummy[:29]
		chartwks = xrange(len(chartORs))
		print "season number and num weeks", s, len(wkdummy)
	else:
		chartORs = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		avg53 = (chartORs[12] + chartORs[13])/2
		chartORs.insert(13, avg53)
		chartwks = xrange(len(sorted(wkdummy)) + 1)
		print "season number and num weeks", s, len(wkdummy),  len(chartORs)
		
	# processing: grab average z-OR during early warning and retrospective periods (after adding week 53 to all seasons)
# 	class_mn = 
	# early warning period is week after Thanksgiving week plus 1 subsequent week
	early_mn = np.mean([ORdict_znorm2[wk] for wk in sorted(wkdummy) if wk > Thxdict[s]][1:early_period+1])
	# retrospective period may be defined as the two week period after x% cumulative incidence is surpassed or the two week period starting x weeks prior to peak incidence week
	retro_mn_cum = np.mean([ORdict_znorm2[wk] for wk in retrodict_cum2[s]])
	retro_mn_pk = np.mean([ORdict_znorm2[wk] for wk in retrodict_pk2[s]])
	
	# view results in terminal
	print 'season', s, early_mn, retro_mn_cum, retro_mn_pk

# 	
# 	fwriter.write('%s,%s,%s\n' % (s, retro_mn_pk, early_mn))
# fwriter.close()

