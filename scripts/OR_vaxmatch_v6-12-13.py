#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/12/13
###Function: 
## 1. Generate a scatterplot of the OR (x-axis) by the vaccine match for each season

### Updates from 5/22/13 version:
#### call ORgenerator script to calculate odds ratios
#### OR represents the average OR for all zip3s

### rerun 8/7/13 with updated prominent subtype information

###Import data: vaxmatch.csv, zipcode_bysseas_cl_v6-12-13.csv

###Codebook
# prominent SUBTYPE_marker: 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B
# H1_MATCH: percent of H1 virus isolates that were characterized as antigenically similar to the H1 component of the season's Northern Hemisphere trivalent flu vaccine, rounded to the nearest whole percent. 
# H3_MATCH: same as H1_MATCH with H3 virus isolates
# B_MATCH: same as H1_MATCH with B virus isolates across both Yamagata and Victoria lineages. M
# TOT_MATCH: percent of all virus isolates that were characterized as antigenically similar to any of the trivalent vaccine strains, rounded to the nearest whole percent. These levels are not the same to those used by the CDC website to categorize vaccine strain match.
# MLVL: qualitative code that represents level of vaccine strain match with strains circulating during the season. This is calculated as percent of virus isolates that match one vaccine strain in the trivalent vaccine out of the total number of virus isolates collected that season. These are the codes we have defined: very low = 0-20%; low = 21-40%; medium = 41-60%; high = 61-80%; very high = 81-100%
# MLVL_marker: match level marker for plotting 1 = very low; 2 = low; 3 = medium; 4 = high; 5 = very high

###Command Line: python 
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
child1, adult1, y1, z3s, snum_sdi = [],[],[],[],[] # attack rates for children and adults for all cases, odds ratios for all cases, zip3s in dataset; season number code in import dataset
avgOR1, sdOR1 = [],[] # average ORs across zip3s for each season, standard deviation of ORs for each season (dispersion of zip3 ORs around the mean)
seasonnum, subtypemarker, H1match, H3match, Bmatch, totmatch, mlvlmarker = [],[],[],[],[],[],[]


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

def vaxmatch_import (csvreadfile, season, s_marker, match1, match3, matchb, matcht, mlvl_marker):
# csvreadfile is csv file object: season number, flu season, prominent subtypes, prominent subtypes marker (see header of script), percent of H1/H3/B/all isolates that antigenically match the vaccine strains, vaccine match bin (qualitative code), vaccine match bin marker
	for row in csvreadfile:
		season.append(int(row[0]))
		s_marker.append(int(row[3]))
		match1.append(float(row[4]))
		match3.append(float(row[5]))
		matchb.append(float(row[6]))
		matcht.append(float(row[7]))
		mlvl_marker.append(int(row[9]))


### import data ###
vaxmatchin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/vaxmatch2.csv','r')
vaxmatch=csv.reader(vaxmatchin, delimiter=',')
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/zipcode_bysseas_cl_v6-12-13.csv','r')
d1=csv.reader(d1in, delimiter=',')


### program ###
od.importer_ORzip3(d1, adult1, child1, 3, 4, z3s, 2, snum_sdi)
od.ORgen_zip3mn(y1, child1, adult1, snum_sdi, avgOR1, sdOR1)
vaxmatch_import (vaxmatch, seasonnum, subtypemarker, H1match, H3match, Bmatch, totmatch, mlvlmarker)
print totmatch

print "length of mlvlmarker:", len(mlvlmarker)
print "length of avgORlist:", len(avgOR1), len(sdOR1)

# OR vs qualitative bins for vaccine strain match level
mlvllab = ['','very low', 'low', 'medium', 'high', 'very high','']
xaxis = range(0,7)
# xaxjitter = [x + np.random.uniform(-0.3, 0.3, 1) for x in mlvlmarker]
plt.errorbar(mlvlmarker, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, mlvl, OR in zip(seasonnum, mlvlmarker, avgOR1):
	plt.annotate(num, xy = (mlvl, OR), xytext = (5,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Vaccine strain match level')
plt.legend(loc="upper left")
plt.xticks(xaxis, mlvllab)
ylim([2,7])
plt.show()

# OR vs vaccine strain match percent (across all three vaccine strains)
# xaxjitter = [x + np.random.uniform(-5, 5, 1) for x in totmatch]
plt.errorbar(totmatch, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, totmatch, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Trivalent vaccine strain match (%)')
plt.legend(loc="upper left")
xlim([-10,110])
ylim([2,7])
plt.show()


# OR vs Influenza B vaccine strain match percent
# xaxjitter = [x + np.random.uniform(-5, 5, 1) for x in Bmatch]
plt.errorbar(Bmatch, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, Bmatch, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Influenza B vaccine match (%)')
plt.legend(loc="upper left")
xlim([-10,110])
ylim([2,7])
plt.show()

# OR vs H1 vaccine strain match percent
# xaxjitter = [x + np.random.uniform(-5, 5, 1) for x in H1match]
plt.errorbar(H1match, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, H1match, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('H1 vaccine match (%)')
plt.legend(loc="upper left")
xlim([-10,110])
ylim([2,7])
plt.show()

# OR vs H3 vaccine strain match percent
# xaxjitter = [x + np.random.uniform(-5, 5, 1) for x in H3match]
plt.errorbar(H3match, avgOR1, yerr=sdOR1, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, H3match, avgOR1):
	plt.annotate(num, xy = (perc, OR), xytext = (5,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('H3 vaccine match (%)')
plt.legend(loc="upper left")
xlim([-10,110])
ylim([2,7])
plt.show()



