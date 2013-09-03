#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 9/2/13
###Function: draw OR by week for all weeks

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
# ilidict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
ilidict, wkdict = {}, {}
# ORdict[week] = OR
# ARdict[week] = attack rate per 10000
ORdict, ARdict = {}, {}

### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn from 2010 Census
seasons = range(1,11) #seasons for which ORs will be generated

### plotting settings ###
colorvec = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
labelvec = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10']
xlabels = range(40,54)
xlabels.extend(range(1,40))

### functions ###

### import data ###
datain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
data=csv.reader(datain, delimiter=',')

### program ###

# OR by week chart
# ilidict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
# weeks = unique list of weeks for dataset
ilidict, wkdict, weeks = od.import_dwk(data, 0, 1, 2, 3)
ORdict, ARdict = od.ORgen_wk(ilidict, weeks)
for s in seasons:
	# wkdummy will represent list of weeks for chart in season to use as key for OR dict
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy)
	if s == 1:
		chartORs = [ORdict[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(13, 13 + len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	elif len(wkdummy) == 53:
		# wkdummy needs to be sorted bc dict values don't have order
		chartORs = [ORdict[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(len(sorted(wkdummy)))
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
	else:
		chartORs = [ORdict[wk] for wk in sorted(wkdummy)]
		avg53 = (chartORs[12] + chartORs[13])/2
		chartORs.insert(13, avg53)
		chartwks = xrange(len(sorted(wkdummy)) + 1)
		print "season number and num weeks", s, len(wkdummy)
		plt.plot(chartwks, chartORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1], linewidth = 2)
plt.xlim([0, 52])
plt.ylim([1, 10])
plt.xlabel('Week Number')
plt.ylabel('OR, c:a (US pop normalized)')
plt.legend(loc = 'upper left')
plt.xticks(xrange(53), xlabels)
plt.show()





