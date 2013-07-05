#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: June 4, 2013
###Function: 
#### generate a metric that represents the potential interactive effect between the prominent subtype and the vax strain match for the prominent subtype
#### draw a plot of OR (y-axis) vs this interaction metric (x-axis)
#### same plot is represented in two ways -- labels are season number or prominent subtype(s)

###Import data: subtype.csv, odds_c_a1.csv, odds_c_a3_a, odds_c_a3_b

###Command Line: python OR_subtype_vaxmatch_v6-4-13.py
##############################################


### notes ###
# potential interactive effect: vax match and prominent subtypes. % isolates that are H1 * % H1 isolates that matched H1 vax strain = # H1 isolates/# isolates * # H1 matched isolates/# H1 isolates

### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##

### data structures ###
child1, child3a, child3b, adult1, adult3a, adult3b = [],[],[],[],[],[] # attack rates for children and adults for total, severe, and mild cases
y1, y3a, y3b = [],[],[] # odds ratios for total, severe, and mild cases
seasonnum, match_iso, psubtypelab = [],[],[] # season number, # matched isolates for prominent subtypes/# total isolates, prominent subtype label

### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn


### functions ###
def importer (csvreadfile, adultlist, childlist, ilicol):
	ct=0	
	for row in csvreadfile:
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/USadult)
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/USchild)
		else:
			ct+=1	

def ORgen (ylist, childlist, adultlist):
	for i in range(0,len(childlist)):
		ylist.append((childlist[i]/(1-childlist[i]))/(adultlist[i]/(1-adultlist[i])))
# 	print childlist[i], 1-childlist[i], adultlist[i], 1-adultlist[i]

def subtype_vaxmatch_import (csvreadfile, season, interact, s_label):
	for row in csvreadfile:
		H1i, H3i, Bi, TOTi = float(row[4]), float(row[5]), float(row[6]), float(row[7])
		H1im, H3im, Bim, TOTim = float(row[8]), float(row[9]), float(row[10]), float(row[11])
		season.append(int(row[0])) # season number
		s_label.append(row[2])
		val = int(row[3])
		# subtype value determines how percentage will be calculated 
		if val == 1: # H1 matched isolates/# isolates
			interact.append(H1im/TOTi)
		elif val == 2: # H3 matched isolates/# isolates
			interact.append(H3im/TOTi)
		elif val == 5: # H1+B matched isolates/# isolates
			interact.append((H1im+Bim)/TOTi)
		elif val == 6: # H3+B matched isolates/# isolates
			interact.append((H3im+Bim)/TOTi)
		elif val == 7: # H1+H3+B matched isolates/# isolates
			interact.append((H1im+H3im+Bim)/TOTi)
		#print val, H1im, H3im, Bim, TOTi


### import data ###
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a1.csv','r')
d1=csv.reader(d1in, delimiter=',')
d3ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_a.csv','r')
d3a=csv.reader(d3ain, delimiter=',')
d3bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_b.csv','r')
d3b=csv.reader(d3bin, delimiter=',')
subtypein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/subtype3.csv','r')
subtype=csv.reader(subtypein, delimiter=',')

### program ###
importer(d1, adult1, child1, 2)
importer(d3a, adult3a, child3a, 2)
importer(d3b, adult3b, child3b, 2)
ORgen(y1, child1, adult1)
ORgen(y3a, child3a, adult3a)
ORgen(y3b, child3b, adult3b)
subtype_vaxmatch_import(subtype, seasonnum, match_iso, psubtypelab)
print match_iso

# plot OR vs # matched isolates of prominent subtypes that season / # total isolates (labels represent season num)
plt.scatter(match_iso, y1, marker='o', color = 'black', label= "all cases")
plt.scatter(match_iso, y3a, marker='o', color = 'red', label= "severe cases")
plt.scatter(match_iso, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, match_iso, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, match_iso, y3a):
	plt.annotate(num, xy = (perc, OR), xytext = (-10,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, match_iso, y3b):
	plt.annotate(num, xy = (perc, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Matched isolates (prominent subtypes only)/ Total isolates')
plt.legend(loc="upper left")
plt.show()

# same plot as above except labels are prominent subtype
plt.scatter(match_iso, y1, marker='o', color = 'black', label= "all cases")
for lab, perc, OR in zip(psubtypelab, match_iso, y1):
	plt.annotate(lab, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Matched isolates (prominent subtypes only)/ Total isolates')
plt.legend(loc="upper left")
plt.show()




















