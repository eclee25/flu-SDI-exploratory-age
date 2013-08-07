#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/7/13
###Function: draw attack rates by week for weeks 40 to 20 in SDI data

###Import data: SQL_export/AR_wk.csv

###Command Line: python 
##############################################


### notes ###


### packages ###
import csv
import matplotlib.pyplot as plt
import sys
from datetime import date
import numpy as np
from collections import defaultdict



## local packages ##
# sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab')
# import GeneralTools as gt

### data structures ###
d_swili = defaultdict(list) # (seasonnum) = list of total ili cases each week
d_spop = {} # (january seasonnum) = total pop size # flu seasons span two calendar years so grab the population size for the second year to use as the denominator
d_sAR = defaultdict(list) # (seasonnum) = list of weekly attack rates

### plotting parameters ###
xplot = range(1,35)
xlabels = range(40,54)
xlabels.extend(range(1,21))
colorvec = ['black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
labelvec = ['01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10']



### functions ###
# import ili cases by week into a dict
def import_ILI (csvfile, d_ILI, seascol, ilicol):
	for row in csvfile:
		d_ILI[int(row[seascol])].append(float(row[ilicol]))

# import population size by season into a dict
def import_pop (csvfile, d_pop, yrcol, popcol):
	for row in csvfile:
		snum = str(row[yrcol][2:4])
		snum = int(snum)
		d_spop[snum] = int(row[popcol])

def calcAR (d_ILI, d_pop, d_AR): 
	for snum in np.arange(2,11):
		if (snum == 5 or snum ==10):
			d_AR[snum] = [ili/d_pop[snum]*100000 for ili in d_ILI[snum]] # attack rate per 100,000
			print "number of weeks in season", snum, len(d_AR[snum])
		else:
			d_AR[snum] = [ili/d_pop[snum]*100000 for ili in d_ILI[snum]] # attack rate per 100,000
			avg53 = (d_AR[snum][12] + d_AR[snum][13])/2
			print d_AR[snum][12], d_AR[snum][13], avg53
			d_AR[snum].insert(13, avg53)
# seasons 5 and 10 have an extra week so average the 52nd wk attack rate and 1st wk attack rate to get 53rd wk


### import data ###
ARin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/AR_wk.csv','r')
AR=csv.reader(ARin, delimiter=',')
popin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop.csv','r')
pop=csv.reader(popin, delimiter=',')

### program ###
import_ILI(AR, d_swili, 0, 2)
import_pop(pop, d_spop, 0, 1)
calcAR(d_swili, d_spop, d_sAR)

# plot attack rates by week
for snum in np.arange(2,11):
	print len(xplot), len(d_sAR[snum])
	plt.plot(xplot, d_sAR[snum], marker='o', color=colorvec[snum-2], label=labelvec[snum-2], linewidth=2)
plt.xlabel('Week Number')
plt.ylabel('Incidence per 100,000')
plt.legend(loc="upper right")
plt.xticks(xplot,xlabels)
plt.show()



















