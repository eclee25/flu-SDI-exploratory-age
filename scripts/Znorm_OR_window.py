#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/2/14
###Function: calculate moving window z-normalized average across all weeks to examine zOR trends during flu and non-flu seasons
## try different window sizes for sensitivity

###Import data: 

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys


## local modules ##
import ORgenerator as od

### data structures ###
# ORdict_znorm[week] = OR_znorm
ORdict_znorm = {} # all data
ORdict_znorm2 = {} # offices/OP only

### parameters ###
USchild = 20348657 + 20677194 + 22040343 # US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 # US adult popn from 2010 Census
seasons = range(2,11) # seasons for which ORs will be generated
normwks = 10 # number of weeks at beginning of season over which OR will be normalized

### plotting settings ###
colorvec = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
labelvec = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10']
xlabels = range(40,54)
xlabels.extend(range(1,40))

### functions ###
def znorm_window (normweeks, dict_OR):
	'''Generate dictionary of z-normalized OR based on the average and SD of normweeks immediately before the week in question.'''
	
	# dict_zOR_window[week] = zOR normalized by normweeks
	dict_zOR_window = {}
	
	OR_norm_ls = []
	window_mean, window_sd = float('nan'), float('nan')
	for wk in sorted(dict_OR):
# 		print wk, window_mean, len(OR_norm_ls), OR_norm_ls
		dict_zOR_window[wk] = (dict_OR[wk] - window_mean)/window_sd
		OR_norm_ls.append(dict_OR[wk])
		if len(OR_norm_ls) == normweeks:
			window_mean = float(np.mean(OR_norm_ls))
			window_sd = np.std(OR_norm_ls)
			OR_norm_ls.pop(0)

	return dict_zOR_window

### import data ###
datain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
data=csv.reader(datain, delimiter=',')
data2in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_office.csv','r')
data2=csv.reader(data2in, delimiter=',')

### program ###

## data processing ##
# all data #
ilidict, wkdict, weeks = od.import_dwk(data, 0, 1, 2, 3)
# ilidict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
ORdict, ARdict = od.ORgen_wk(ilidict, weeks)
# ORdict[week] = OR
# ARdict[week] = attack rate per 10000

# create dict of zOR based on moving window of normwks size
zORdict_window = znorm_window(normwks, ORdict)


## plots ##
# all data #
for s in seasons:
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy)
	if s == 1:
		chartORs = [zORdict_window[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(13, 13 + len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	elif len(wkdummy) == 53:
		chartORs = [zORdict_window[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	else:
		chartORs = [zORdict_window[wk] for wk in sorted(wkdummy)]
		avg53 = (chartORs[12] + chartORs[13])/2
		chartORs.insert(13, avg53)
		chartwks = xrange(len(sorted(wkdummy)) + 1)
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
# vertical line representing end of flu season
plt.plot([33, 33], [-10, 15], color = 'k', linewidth = 1)
# horizontal line representing sd = 1 (sd>1 is mild)
plt.plot([0, 52], [1, 1], color = 'k', linewidth = 1)
# horizontal line representing sd = -1 (sd<1 is severe)
plt.plot([0, 52], [-1, -1], color = 'k', linewidth = 1)
# # grey bar for classification period
# plt.fill([15, 16, 16, 15], [-10, -10, 15, 15], facecolor='grey', alpha=0.4)
# # grey bar for early warning area
# plt.fill([8, 10, 10, 8], [-10, -10, 15, 15], facecolor='grey', alpha=0.4)
plt.xlim([0, 52])
plt.ylim([-10, 15])
plt.xlabel('Week Number', fontsize=24) # 12/1/13 increase size
plt.ylabel('z-OR (%s wk moving window), child:adult' % normwks, fontsize=24)
plt.legend(loc = 'upper left')
plt.xticks(xrange(53), xlabels)
plt.show()













