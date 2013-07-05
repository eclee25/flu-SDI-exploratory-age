#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/16/13
###Function: To create chart of prominent subtype (x-axis) during flu season by odds ratio of attack rate (y-axis)

### Updates from 5/20/13 version:
#### call ORgenerator script to calculate odds ratios
#### OR represents the average OR for all zip3s

###Import data: subtype.csv, zipcode_bysseas_cl_v6-12-13.csv

### Codebook:
### SUBTYPE_marker: 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B

###Command Line: python OR_subtype_v6-16-13.py
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##
import ORgenerator_v060713 as od # 6/16 add script for OR generation functions

### data structures ###
# 6/16 add and remove necessary lists for calling od script
child1, adult1, y1, z3s, snum_sdi = [],[],[],[],[] # attack rates for children and adults for all cases, odds ratios for all cases, zip3s in dataset; season number code in import
avgOR1, sdOR1 = [],[] # average ORs across zip3s for each season, standard deviation of ORs for each season (dispersion of zip3 ORs around the mean)
seasonnum, subtypeplot, domsubtypeplot = [],[],[] # season number, subtype marker for plotting
H1i_perc, H3i_perc, Bi_perc, TOTiso = [],[],[],[] # percentage of H1, H3, B isolates out of total isolates and number of total isolates collected

### parameters ###
# USchild = 20348657 + 20677194 + 22040343 #US child popn
# USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn


### functions ###
# def importer (csvreadfile, adultlist, childlist, ilicol):
# 	ct=0	
# 	for row in csvreadfile:
# 		if row[1] == "A":
# 			adultlist.append(float(row[ilicol])/USadult)
# 		elif row[1] == "C":
# 			childlist.append(float(row[ilicol])/USchild)
# 		else:
# 			ct+=1
# 	
#
# def ORgen (ylist, childlist, adultlist):
# 	for i in range(0,len(childlist)):
# 		ylist.append((childlist[i]/(1-childlist[i]))/(adultlist[i]/(1-adultlist[i])))
# # 	print childlist[i], 1-childlist[i], adultlist[i], 1-adultlist[i]


def subtype_import (csvreadfile, season, s_marker, ds_marker, H1iso_perc, H3iso_perc, Biso_perc, TOTiso):
	for row in csvreadfile:
		H1i, H3i, Bi, TOTi = float(row[4]), float(row[5]), float(row[6]), float(row[7])
		season.append(int(row[0])) # season number
		s_marker.append(int(row[3])) # subtype value for plotting
		H1iso_perc.append(H1i/TOTi*100)
		H3iso_perc.append(H3i/TOTi*100)
		Biso_perc.append(Bi/TOTi*100)
		TOTiso.append(TOTi)
		if H1i>H3i and H1i>Bi:
			ds_marker.append(1) # plurality of H1 isolates
		elif H3i>H1i and H3i>Bi:
			ds_marker.append(2) # plurality of H3 isolates
		else:
			ds_marker.append(3) # plurality of B isolates

### import data ###
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_bysseas_cl_v6-12-13.csv','r')
d1=csv.reader(d1in, delimiter=',')
subtypein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/subtype3.csv','r')
subtype=csv.reader(subtypein, delimiter=',')

### program ###
od.importer_ORzip3(d1, adult1, child1, 3, 4, z3s, 2, snum_sdi)
od.ORgen_zip3mn(y1, child1, adult1, snum_sdi, avgOR1, sdOR1)
subtype_import(subtype, seasonnum, subtypeplot, domsubtypeplot, H1i_perc, H3i_perc, Bi_perc, TOTiso)
print "len(sdOR1):", len(sdOR1)
print "len(subtypeplot):", len(subtypeplot)

# remove 2000-01 data since it isn't a full season
# subtypeplot, y1, y3a, y3b, seasonnum = subtypeplot[-1], y1[-1], y3a[-1], y3b[-1], seasonnum[-1]


# 6/16 change plot variables so they correspond to new list names and add sd errorbars
# 6/16 rm unnecessary code for severe and mild cases
# OR vs. qualitative code of prominent subtype (20% isolate = prominent)
xaxis = range(0,9)
subtypelab = ['','H1','H3','B','H1 & H3','H1 & B','H3 & B','H1 & H3 & B','']
plt.errorbar(subtypeplot, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, subtype, OR in zip(seasonnum, subtypeplot, avgOR1):
	plt.annotate(num, xy = (subtype, OR), xytext = (10,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Prominent Subtypes')
plt.legend(loc="upper left")
plt.xticks(xaxis, subtypelab)
ylim([2,7])
plt.show()

# OR vs. qualitative code of plurality subtype (greatest percentage of isolates)
xaxis = range(1,4)
domsubtypelab = ['H1', 'H3', 'B']
plt.errorbar(domsubtypeplot, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, subtype, OR in zip(seasonnum, domsubtypeplot, avgOR1):
	plt.annotate(num, xy = (subtype, OR), xytext = (10,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Largest plurality subtype')
plt.legend(loc="upper right")
plt.xticks(xaxis, domsubtypelab)
ylim([2,7])
plt.show()

# OR vs. percentage of H1 isolates
plt.errorbar(H1i_perc, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, H1i_perc, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('H1 isolates (% of total)')
plt.legend(loc="upper right")
ylim([2,7])
plt.show()

# OR vs. percentage of H3 isolates
plt.errorbar(H3i_perc, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, H3i_perc, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,2), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('H3 isolates (% of total)')
plt.legend(loc="upper right")
ylim([2,7])
plt.show()

# OR vs. percentage of B isolates
plt.errorbar(Bi_perc, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, Bi_perc, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,2), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('B isolates (% of total)')
plt.legend(loc="upper right")
ylim([2,7])
plt.show()

# OR vs. number of isolates collected
plt.errorbar(TOTiso, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, TOTiso, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,2), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Number of isolates collected')
plt.legend(loc="upper right")
ylim([2,7])
plt.show()







