#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/8/14
###Function: 
## Z-normalize (subtract mean and divide by SD) OR time series -- time series with values greater than 1 are mild seasons?
## Z-normalize OR time series based on mean and SD of first 10 weeks of flu season -- can first 10 weeks tell you about severity of flu season in first few weeks of second year?

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

### import data ###
datain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
data=csv.reader(datain, delimiter=',')
data2in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_office.csv','r')
data2=csv.reader(data2in, delimiter=',')

### program ###

# all data
ilidict, wkdict, weeks = od.import_dwk(data, 0, 1, 2, 3)
# ilidict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
ORdict, ARdict = od.ORgen_wk(ilidict, weeks)
# ORdict[week] = OR
# ARdict[week] = attack rate per 10000

# offices/op data only
ilidict2, wkdict2, weeks = od.import_dwk(data2, 0, 1, 2, 3)
# ilidict2[(week, age marker)] = ILI
# wkdict2[week] = seasonnum
ORdict2, ARdict2 = od.ORgen_wk(ilidict2, weeks)
# ORdict2[week] = OR
# ARdict2[week] = attack rate per 10000

## processing step: z-normalization ##
for s in seasons:
	# wkdummy will represent list of weeks for chart in season to use as key for OR dict
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy)
	# all data
	s_mean = np.mean([ORdict[wk] for wk in sorted(wkdummy)[:normwks]])
	s_sd = np.std([ORdict[wk] for wk in sorted(wkdummy)[:normwks]])
	dictdummyls = [(ORdict[wk]-s_mean)/s_sd for wk in sorted(wkdummy)]
	print 's, s_mean, s_sd:', s, s_mean, s_sd
	for w, z in zip(sorted(wkdummy), dictdummyls):
		ORdict_znorm[w] = z
	# offices/op data
	s_mean2 = np.mean([ORdict2[wk] for wk in sorted(wkdummy)[:normwks]])
	s_sd2 = np.std([ORdict2[wk] for wk in sorted(wkdummy)[:normwks]])
	dictdummyls2 = [(ORdict2[wk]-s_mean2)/s_sd2 for wk in sorted(wkdummy)]
	for w, z in zip(sorted(wkdummy), dictdummyls2):
		ORdict_znorm2[w] = z
	
## plots ##	
# all data
for s in seasons:
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy)
	if s == 1:
		chartORs = [ORdict_znorm[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(13, 13 + len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	elif len(wkdummy) == 53:
		chartORs = [ORdict_znorm[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	else:
		chartORs = [ORdict_znorm[wk] for wk in sorted(wkdummy)]
		avg53 = (chartORs[12] + chartORs[13])/2
		chartORs.insert(13, avg53)
		chartwks = xrange(len(sorted(wkdummy)) + 1)
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
# vertical line representing end of flu season
plt.plot([33, 33], [-10, 15], color = 'k', linewidth = 1)
# horizontal line representing sd = 1
plt.plot([0, 52], [1, 1], color = 'k', linewidth = 1)
# grey bar for classification area
plt.fill([15, 17, 17, 15], [1, 1, 15, 15], facecolor='grey', alpha=0.4)
# grey bar for early warning area
# plt.fill([8, 11, 11, 8], [1, 1, 15, 15], facecolor='grey', alpha=0.4)
plt.xlim([0, 33])
plt.ylim([-10, 15])
plt.xlabel('Week Number', fontsize=24) # 12/1/13 increase size
plt.ylabel('z-normalized OR (%s wks), child:adult' % normwks, fontsize=24)
plt.legend(loc = 'upper left')
plt.xticks(xrange(33), xlabels[:33])
plt.show()

# offices/OP only
for s in seasons:
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy)
	if s == 1:
		chartORs = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(13, 13 + len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	elif len(wkdummy) == 53:
		chartORs = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	else:
		chartORs = [ORdict_znorm2[wk] for wk in sorted(wkdummy)]
		avg53 = (chartORs[12] + chartORs[13])/2
		chartORs.insert(13, avg53)
		chartwks = xrange(len(sorted(wkdummy)) + 1)
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
# vertical line representing end of flu season
plt.plot([33, 33], [-10, 15], color = 'k', linewidth = 1)
# horizontal line representing sd = 1
plt.plot([0, 52], [1, 1], color = 'k', linewidth = 1)
plt.xlim([0, 52])
plt.ylim([-10, 15])
plt.xlabel('Week Number', fontsize=24) # 12/1/13 increase size
plt.ylabel('z-normalized OR (%s wks), child:adult - offices/OP only' % normwks, fontsize=24)
plt.legend(loc = 'upper left')
plt.xticks(xrange(53), xlabels)
plt.show()
	
