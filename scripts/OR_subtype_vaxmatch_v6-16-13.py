#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: June 16, 2013
###Function: 
#### generate a metric that represents the potential interactive effect between the prominent subtype and the vax strain match for the prominent subtype
#### draw a plot of OR (y-axis) vs this interaction metric (x-axis)
#### same plot is represented in two ways -- labels are season number or prominent subtype(s)

### Updates from 6/4/14 version
#### 1) call ORgenerator_v060713 
#### 2) change OR from normalization by US population to normalization by zip3 popstat
#### 3) change import data to zipcode_bysseas

###Import data: subtype.csv, zipcode_bysseas_cl_v6-12-13.csv

###Command Line: python OR_subtype_vaxmatch_v6-12-13.py
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
import ORgenerator_v060713 as od # 6/16 add script

### data structures ###
# 6/16 add lists to correspond to new functions
child1, adult1, y1, z3s, snum_sdi = [],[],[],[],[] # attack rates for children and adults for all cases, odds ratios for all cases, zip3s in dataset; season number code in import dataset
avgOR1, sdOR1 = [],[] # average ORs across zip3s for each season, standard deviation of ORs for each season (dispersion of zip3 ORs around the mean)
seasonnum, match_iso, psubtypelab = [],[],[] # season number, # matched isolates for prominent subtypes/# total isolates, prominent subtype label

### parameters ###
# USchild = 20348657 + 20677194 + 22040343 #US child popn
# USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn


### functions ###
# 6/16 rm in-script functions for OR generation

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
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_bysseas_cl_v6-12-13.csv','r') # 6/16 change file name
d1=csv.reader(d1in, delimiter=',')
subtypein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/subtype3.csv','r')
subtype=csv.reader(subtypein, delimiter=',')

### program ###

# 6/16 change functions and variable names
od.importer_ORzip3(d1, adult1, child1, 3, 4, z3s, 2, snum_sdi)
od.ORgen_zip3mn(y1, child1, adult1, snum_sdi, avgOR1, sdOR1)
subtype_vaxmatch_import(subtype, seasonnum, match_iso, psubtypelab)
print match_iso

# plot OR vs # matched isolates of prominent subtypes that season / # total isolates (labels represent season num)
plt.errorbar(match_iso, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, match_iso, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Matched isolates (prominent subtypes only)/ Total isolates')
plt.legend(loc="upper left")
ylim([2, 7]) # 6/16 add ylim bc error bars are very large
plt.show()

# same plot as above except labels are prominent subtype
plt.errorbar(match_iso, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for lab, perc, OR in zip(psubtypelab, match_iso, avgOR1):
	plt.annotate(lab, xy = (perc, OR), xytext = (-8,6), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Matched isolates (prominent subtypes only)/ Total isolates')
plt.legend(loc="upper left")
ylim([2, 7])
plt.show()




















