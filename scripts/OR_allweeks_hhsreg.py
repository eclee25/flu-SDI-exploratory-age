#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 2/3/14
###Function: Draw OR and normalized OR time series for each HHS region

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/popstat_zip3_season_cl.csv, /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_cl.csv

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from collections import defaultdict
from itertools import product
from time import clock


## local modules ##

### data structures ###
# d_pop[(zip3, season, agegroup)] = popstat
# d_z3hhs[zip3] = hhs region
d_pop, d_z3hhs = {}, {} # from pop data
# d_ILI[(zip3, season, agegroup, wk)] = ILI
# d_seasonweeks[season] = [wk1, wk2, ...]
d_ILI, d_seasonweeks = {}, defaultdict(list) # from OR data
# d_incid[(season, region, agegroup)] = [incidwk1, incidwk2, ...]
d_incid = defaultdict(list)
# d_CAincidrate[(season, region)] = [sum of C&A/sum of C&A pop*10000 in wk1, sum of C&A/sum of C&A pop*10000 in wk2]
# incidence rate per 100
d_CAincidrate = defaultdict(list)
# d_OR[(season, region)] = [ORwk1, ORwk2, ...]
d_OR = defaultdict(list)
# d_normOR[(season, region)] = [normORwk1, normORwk2, ...]
# ORs are normalized by first 'normwks' weeks of season in that specific region
d_normOR = defaultdict(list)



### parameters ###
regions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
seasons = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
normwks = 10 # number of weeks at beginning of season over which OR will be normalized

### plotting settings ###
colorvec = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
labelvec = ['Boston (R1)', 'New York (R2)', 'Philadelphia (R3)', 'Atlanta (R4)', 'Chicago (R5)', 'Dallas (R6)', 'Kansas City (R7)', 'Denver (R8)', 'San Francisco (R9)', 'Seattle (R10)']
xlabels = range(40,54)
xlabels.extend(range(1,40))

### functions ###
def incid_reg_wk (dict_ILI, weeklist, zip3list, seasonnum, hhsregion): 
	''' Generate child and adult ILI incidence at the week level for each HHS region by adding child and adult ILI cases for all zip3s in that region for that week. Generates values for an incidence dictionary where dict_incid[(season, region, agegroup)] = [incidwk1, incidwkd2, ...]. This function returns the list of ILI cases for each week in the season-region combination for children and adults. '''
	# dict_incid[(season, region, agegroup) = [incidwk1, incidwk2]
	incidwklist_child, incidwklist_adult = [], []
	
	# d_ILI[(zip3, season, agegroup, wk)] = ILI
	for week in sorted(weeklist):
		c_clock = clock()
		incidwk_child = sum([d_ILI[(zip3, seasonnum, 'C', week)] for zip3 in zip3list if (zip3, seasonnum, 'C', week) in d_ILI])
		print clock() - c_clock, week, incidwk_child
		incidwk_adult = sum([d_ILI[(zip3, seasonnum, 'A', week)] for zip3 in zip3list if (zip3, seasonnum, 'A', week) in d_ILI])
		incidwklist_child.append(float(incidwk_child))
		incidwklist_adult.append(float(incidwk_adult))
	
	return incidwklist_child, incidwklist_adult
	
	
def reg_season (dict_seasonweeks, dict_z3hhs, seasonnum, hhsregion):
	''' Return a list of weeks and a list of zip3s for a given season and HHS region. These lists will be fed into a different function that generates child and adult ILI ILI counts at the weekly level for a single season and region.
	'''
	weeklist = dict_seasonweeks[seasonnum]
	zip3list = [key for key in dict_z3hhs if dict_z3hhs[key] == hhsregion]
	return weeklist, zip3list

### import data ###
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/popstat_zip3_season_cl.csv','r')
ORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_cl.csv', 'r')
popin.readline()
pop = csv.reader(popin, delimiter=',')
ORin.readline()
OR = csv.reader(ORin, delimiter=',')

for row in pop:
	zip3, season, agegroup, popstat, hhs = str(row[0]), str(row[3]), str(row[4]), int(row[2]), str(row[8])
	d_pop[(zip3, season, agegroup)] = popstat
	d_z3hhs[zip3] = hhs
for row in OR:
	season, zip3, agegroup, ILI = str(row[0]), str(row[2]), str(row[3]), int(row[4])
	wk = date(int(row[1][:4]), int(row[1][5:7]), int(row[1][8:]))
	d_ILI[(zip3, season, agegroup, wk)] = ILI
	d_seasonweeks[season].append(wk)

# process d_seasonweeks so that wk lists only unique weeks in sorted order for each season
for k in d_seasonweeks:
	d_seasonweeks[k] = sorted(set(d_seasonweeks[k]))

### program ###

# data processing
for snum, regnum in product(seasons, regions):
	wklsdummy, z3lsdummy = reg_season(d_seasonweeks, d_z3hhs, snum, regnum)
	# d_incid[(season, region, agegroup)] = [incidwk1, incidwk2]
	c_incid, a_incid = incid_reg_wk(d_ILI, wklsdummy, z3lsdummy, snum, regnum)
	d_incid[(snum, regnum, 'C')] = c_incid
	d_incid[(snum, regnum, 'A')] = a_incid
	c_pop_dummy, a_pop_dummy = sum([d_pop[(zip3, snum, 'C')] for zip3 in z3lsdummy]), sum([d_pop[(zip3, snum, 'A')] for zip3 in z3lsdummy])
	
	# d_CAincidrate[(season, region)] = [sum of C&A/sum of C&A pop in wk1, sum of C&A/sum of C&A pop in wk2]
	d_CAincidrate[(snum, regnum)] = [(c + a)/(c_pop_dummy + a_pop_dummy)*10000 for c, a, in zip(d_incid[(snum, regnum, 'C')], d_incid[(snum, regnum, 'A')])]
	
	# create OR dictionary
	# dict_OR[(season, region)] = [ORwk1, ORwk2, ...]
	d_OR[(snum, regnum)] = [((c/c_pop_dummy)/(1-(c/c_pop_dummy)))/((a/a_pop_dummy)/(1-(a/a_pop_dummy))) for c, a in zip(d_incid[(snum, regnum, 'C')], d_incid[(snum, regnum, 'A')])]
	
	# create normalized OR dictionary
	mndummy = np.mean(d_OR[(snum, regnum)][:normwks])
	sddummy = np.std(d_OR[(snum, regnum)][:normwks])
	d_normOR[(snum, regnum)] = [(OR - mndummy)/sddummy for OR in d_OR[(snum, regnum)]]

### plots ###
# regular OR plots by region for each season
for s in seasons:
	for r in regions:
		if s == '01':
			chartORs = d_OR[(s, r)]
			chartwks = xrange(13, 13 + len(chartORs))
			print 'snumber, region, num weeks', s, r, len(chartORs)
			plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
		elif len(d_OR[(s, r)]) == 53:
			chartORs = d_OR[(s, r)]
			chartwks = xrange(len(chartORs))
			print 'snumber, region, num weeks', s, r, len(chartORs)
			plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
		else:
			chartORs = d_OR[(s, r)]
			avg53 = (chartORs[12] + chartORs[13])/2
			chartORs.insert(13, avg53)
			chartwks = xrange(len(chartORs))
			print 'snumber, region, num weeks', s, r, len(chartORs)
			plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
	plt.plot([33, 33], [0, 15], color = 'k', linewidth = 1)
	plt.xlim([0, 52])
	plt.ylim([0, 15])
	plt.xlabel('Week Number, Season %s' % int(s), fontsize=24)
	plt.ylabel('OR, child:adult', fontsize=24)
	plt.legend(loc = 'upper left')
	plt.xticks(xrange(53), xlabels)
	plt.show()
		
# normalized OR plots by region for each season
for s in seasons:
	for r in regions:
		if s == '01':
			chartORs = d_normOR[(s, r)]
			chartwks = xrange(13, 13 + len(chartORs))
			print 'snumber, region, num weeks', s, r, len(chartORs)
			plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
		elif len(d_normOR[(s, r)]) == 53:
			chartORs = d_normOR[(s, r)]
			chartwks = xrange(len(chartORs))
			print 'snumber, region, num weeks', s, r, len(chartORs)
			plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
		else:
			chartORs = d_normOR[(s, r)]
			avg53 = (chartORs[12] + chartORs[13])/2
			chartORs.insert(13, avg53)
			chartwks = xrange(len(chartORs))
			print 'snumber, region, num weeks', s, r, len(chartORs)
			plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
	# vertical line representing end of flu season
	plt.plot([33, 33], [-10, 15], color = 'k', linewidth = 1)
	# horizontal line representing sd = 1
	plt.plot([0, 53], [1, 1], color = 'k', linewidth = 1)
	plt.xlim([0, 52])
	plt.ylim([-10, 15])
	plt.xlabel('Week Number, Season %s' % int(s), fontsize=24)
	plt.ylabel('z-normalized OR (%s wks), child:adult' % normwks, fontsize=24)
	plt.legend(loc = 'upper left')
	plt.xticks(xrange(52), xlabels)
	plt.show()	
		
# sum of child and adult incidence by region for each season
for s in seasons:
	for r in regions:
		if s == '01':
			chartincids = d_CAincidrate[(s, r)]
			chartwks = xrange(13, 13 + len(chartincids))
			print 'snumber, region, num weeks', s, r, len(chartincids)
			plt.plot(chartwks, chartincids, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
		elif len(d_CAincidrate[(s, r)]) == 53:
			chartincids = d_CAincidrate[(s, r)]
			chartwks = xrange(len(chartincids))
			print 'snumber, region, num weeks', s, r, len(chartincids)
			plt.plot(chartwks, chartincids, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
		else:
			chartincids = d_CAincidrate[(s, r)]
			avg53 = (chartincids[12] + chartincids[13])/2
			chartincids.insert(13, avg53)
			chartwks = xrange(len(chartincids))
			print 'snumber, region, num weeks', s, r, len(chartincids)
			plt.plot(chartwks, chartincids, marker = 'o', color = colorvec[int(r)-1], label = labelvec[int(r)-1], linewidth = 2)
	# vertical line representing end of flu season
	plt.plot([33, 33], [-10, 25], color = 'k', linewidth = 1)
	plt.xlim([0, 52])
	plt.ylim([0, 9])
	plt.xlabel('Week Number, Season %s' % int(s), fontsize=24)
	plt.ylabel('Child & adult incidence per 10,000', fontsize=24)
	plt.legend(loc = 'upper right')
	plt.xticks(xrange(53), xlabels)
	plt.show()	
		
		
		
		
		
		
		
		
		
		