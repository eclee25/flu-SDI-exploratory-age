#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/25/13
###Function: Draw OR by season severity plots where season severity is defined as attack rate per 100,000 in acute care or inpatient facilities in flu peak weeks

###Import data: SQL_export/OR_swk6.csv, SQL_export/seasonseverity.csv

###Command Line: python 
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

## local packages ##
import ORgenerator as od

### data structures ###
s6dict, ORdict = {},{}
sevdict = {} # season-severity proxy dictionary

### parameters ###
seasons = range(2,11) #seasons for which ORs will be generated

### functions ###



### import data ###
s6in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_swk6.csv','r')
s6=csv.reader(s6in, delimiter=',')
sevin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/seasonseverity.csv','r')
sev=csv.reader(sevin, delimiter=',')

### program ###
s6dict = od.import_d(s6, 0, 1, 2)
ORdict = od.ORgen_seas(s6dict, seasons)
sevdict = od.import_gen_d(sev, 0, 3)

# plot data
# [1:] drops season 1 data for presentation plot
xvals = [float(sevdict[k]) for k in sorted(sevdict)[1:]]
yvals = [ORdict[k] for k in sorted(ORdict)]

print "sevdict pairs", sorted(sevdict.items())
print "sevdict keys", sorted(sevdict)
print "ORdict pairs", sorted(ORdict.items())
print "ORdict keys", sorted(ORdict)
# values without season 1 data
print "sevdict values", xvals
print "ORdict values", yvals

plt.scatter(xvals, yvals, marker='o', color = 'black', label= "total")
for num, AR, OR in zip(sorted(sevdict)[1:], xvals, yvals):
	plt.annotate(num, xy = (AR, OR), xytext = (-2, 5), textcoords = 'offset points', fontsize=18)
# plt.xlabel('Attack Rate per 100,000 in acute care/inpatient at peak weeks')
plt.xlabel('Season Severity\nAttack Rate in inpatient facilities per 100,000 at peak weeks', fontsize=18)
plt.xticks(fontsize=16)
# plt.ylabel('Attack Rate OR, c:a (US pop normalized, peak +/- 6wks)')
plt.ylabel('OR at Peak Weeks, child:adult', fontsize=24)
plt.yticks(fontsize=16)
plt.show()

corr = stats.pearsonr(xvals[:-1], yvals[:-1])
print 'Pearson correlation coefficient', corr









