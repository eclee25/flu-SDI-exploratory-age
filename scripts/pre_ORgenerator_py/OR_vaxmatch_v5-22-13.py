#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 5/22/13
###Function: 
## 1. Generate a scatterplot of the OR (x-axis) by the vaccine match for each season

###Import data: vaxmatch.csv, odds_c_a1.csv, odds_c_a3_a, odds_c_a3_b

###Codebook
# SUBTYPE_marker: 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B
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

### data structures ###
child1, child3a, child3b, adult1, adult3a, adult3b = [],[],[],[],[],[] # attack rates for children and adults for total, severe, and mild cases
y1, y3a, y3b = [],[],[] # odds ratios for total, severe, and mild cases
seasonnum, subtypemarker, H1match, H3match, Bmatch, totmatch, mlvlmarker = [],[],[],[],[],[],[]

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

def vaxmatch_import (csvreadfile, season, s_marker, match1, match3, matchb, matcht, mlvl_marker):
	for row in csvreadfile:
		season.append(int(row[0]))
		s_marker.append(int(row[3]))
		match1.append(float(row[4]))
		match3.append(float(row[5]))
		matchb.append(float(row[6]))
		matcht.append(float(row[7]))
		mlvl_marker.append(int(row[9]))
	
		


### import data ###
vaxmatchin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/vaxmatch.csv','r')
vaxmatch=csv.reader(vaxmatchin, delimiter=',')
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a1.csv','r')
d1=csv.reader(d1in, delimiter=',')
d3ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_a.csv','r')
d3a=csv.reader(d3ain, delimiter=',')
d3bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_b.csv','r')
d3b=csv.reader(d3bin, delimiter=',')


### program ###
importer(d1, adult1, child1, 2)
importer(d3a, adult3a, child3a, 2)
importer(d3b, adult3b, child3b, 2)
ORgen(y1, child1, adult1)
ORgen(y3a, child3a, adult3a)
ORgen(y3b, child3b, adult3b)
vaxmatch_import (vaxmatch, seasonnum, subtypemarker, H1match, H3match, Bmatch, totmatch, mlvlmarker)
print totmatch

# OR vs qualitative bins for vaccine strain match level
mlvllab = ['very low', 'low', 'medium', 'high', 'very high']
xaxis = range(1,6)
plt.scatter(mlvlmarker, y1, marker='o', color = 'black', label= "all cases")
plt.scatter(mlvlmarker, y3a, marker='o', color = 'red', label= "severe cases")
plt.scatter(mlvlmarker, y3b, marker='o', color = 'green', label= "milder cases")
for num, mlvl, OR in zip(seasonnum, mlvlmarker, y1):
	plt.annotate(num, xy = (mlvl, OR), xytext = (5,0), textcoords = 'offset points')
for num, mlvl, OR in zip(seasonnum, mlvlmarker, y3a):
	plt.annotate(num, xy = (mlvl, OR), xytext = (-10,0), textcoords = 'offset points')
for num, mlvl, OR in zip(seasonnum, mlvlmarker, y3b):
	plt.annotate(num, xy = (mlvl, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Vaccine strain match level')
plt.legend(loc="upper left")
plt.xticks(xaxis, mlvllab)
plt.show()

# OR vs vaccine strain match percent (across all three vaccine strains)
plt.scatter(totmatch, y1, marker='o', color = 'black', label= "all cases")
plt.scatter(totmatch, y3a, marker='o', color = 'red', label= "severe cases")
plt.scatter(totmatch, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, totmatch, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, totmatch, y3a):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, totmatch, y3b):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Trivalent vaccine strain match (%)')
plt.legend(loc="upper left")
plt.show()

# OR vs Influenza B vaccine strain match percent
plt.scatter(Bmatch, y1, marker='o', color = 'black', label= "all cases")
plt.scatter(Bmatch, y3a, marker='o', color = 'red', label= "severe cases")
plt.scatter(Bmatch, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, Bmatch, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, Bmatch, y3a):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, Bmatch, y3b):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Influenza B vaccine match (%)')
plt.legend(loc="upper left")
plt.show()

# OR vs H1 vaccine strain match percent
plt.scatter(H1match, y1, marker='o', color = 'black', label= "all cases")
plt.scatter(H1match, y3a, marker='o', color = 'red', label= "severe cases")
plt.scatter(H1match, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, H1match, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, H1match, y3a):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, H1match, y3b):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('H1 vaccine match (%)')
plt.legend(loc="upper left")
plt.show()

# OR vs H3 vaccine strain match percent
plt.scatter(H3match, y1, marker='o', color = 'black', label= "all cases")
plt.scatter(H3match, y3a, marker='o', color = 'red', label= "severe cases")
plt.scatter(H3match, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, H3match, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, H3match, y3a):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, H3match, y3b):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('H3 vaccine match (%)')
plt.legend(loc="upper left")
plt.show()



