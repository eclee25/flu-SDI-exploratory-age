#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 5/20/13
###Function: To create chart of prominent subtype (x-axis) during flu season by odds ratio of attack rate (y-axis)

###Import data: subtype.csv, odds_c_a1.csv, odds_c_a3_a, odds_c_a3_b

### Codebook:
### SUBTYPE_marker: 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B

###Command Line: python OR_subtype_v5-20-13.py
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
seasonnum, subtypeplot, domsubtypeplot = [],[],[] # season number, subtype marker for plotting
H1i_perc, H3i_perc, Bi_perc, TOTiso = [],[],[],[] # percentage of H1, H3, B isolates out of total isolates and number of total isolates collected

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
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/odds_c_a1.csv','r')
d1=csv.reader(d1in, delimiter=',')
d3ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/odds_c_a3_a.csv','r')
d3a=csv.reader(d3ain, delimiter=',')
d3bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/odds_c_a3_b.csv','r')
d3b=csv.reader(d3bin, delimiter=',')
# subtypein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype4.csv','r')
subtypein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype5.csv','r')
subtype=csv.reader(subtypein, delimiter=',')

### program ###
importer(d1, adult1, child1, 2)
importer(d3a, adult3a, child3a, 2)
importer(d3b, adult3b, child3b, 2)
subtype_import(subtype, seasonnum, subtypeplot, domsubtypeplot, H1i_perc, H3i_perc, Bi_perc, TOTiso)
ORgen(y1, child1, adult1)
ORgen(y3a, child3a, adult3a)
ORgen(y3b, child3b, adult3b)

# remove 2000-01 data since it isn't a full season
# subtypeplot, y1, y3a, y3b, seasonnum = subtypeplot[-1], y1[-1], y3a[-1], y3b[-1], seasonnum[-1]

# OR vs. qualitative code of prominent subtype (20% isolate = prominent)
xaxis = range(1,6)
subtypelab = ['H1', 'H1 & B', 'H1 & H3 & B', 'H3 & B','H3',]
plt.scatter(subtypeplot[1:], y1[1:], marker='o', color = 'black', label= "all cases")
# plt.scatter(subtypeplot, y3a, marker='o', color = 'red', label= "severe cases")
# plt.scatter(subtypeplot, y3b, marker='o', color = 'green', label= "milder cases")
for num, subtype, OR in zip(seasonnum[1:], subtypeplot[1:], y1[1:]):
	plt.annotate(num, xy = (subtype, OR), xytext = (10,0), textcoords = 'offset points', fontsize = 16)
# for num, subtype, OR in zip(seasonnum, subtypeplot, y3a):
# 	plt.annotate(num, xy = (subtype, OR), xytext = (-10,0), textcoords = 'offset points')
# for num, subtype, OR in zip(seasonnum, subtypeplot, y3b):
# 	plt.annotate(num, xy = (subtype, OR), xytext = (-10,5), textcoords = 'offset points')
# plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)') # original plot label
plt.ylabel('OR, child:adult, seasonal attack rate', fontsize=24)  # 12/1/13 presentation label
plt.xlabel('Prominent Subtypes', fontsize=24)
plt.xticks(xaxis, subtypelab, fontsize=16)
plt.yticks(fontsize=18)
plt.show()

# OR vs. qualitative code of plurality subtype (greatest percentage of isolates)
xaxis = range(1,4)
domsubtypelab = ['H1', 'H3', 'B']
plt.scatter(domsubtypeplot, y1, marker='o', color = 'black', label= "all cases")
# plt.scatter(domsubtypeplot, y3a, marker='o', color = 'red', label= "severe cases")
# plt.scatter(domsubtypeplot, y3b, marker='o', color = 'green', label= "milder cases")
for num, subtype, OR in zip(seasonnum, domsubtypeplot, y1):
	plt.annotate(num, xy = (subtype, OR), xytext = (10,0), textcoords = 'offset points')
# for num, subtype, OR in zip(seasonnum, domsubtypeplot, y3a):
# 	plt.annotate(num, xy = (subtype, OR), xytext = (-10,0), textcoords = 'offset points')
# for num, subtype, OR in zip(seasonnum, domsubtypeplot, y3b):
# 	plt.annotate(num, xy = (subtype, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Largest plurality subtype')
plt.legend(loc="upper right")
plt.xticks(xaxis, domsubtypelab)
plt.show()

# OR vs. percentage of H1 isolates
plt.scatter(H1i_perc, y1, marker='o', color = 'black', label= "all cases")
# plt.scatter(H1i_perc, y3a, marker='o', color = 'red', label= "severe cases")
# plt.scatter(H1i_perc, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, H1i_perc, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, H1i_perc, y3a):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, H1i_perc, y3b):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('H1 isolates (% of total)')
plt.legend(loc="upper right")
plt.show()

# OR vs. percentage of H3 isolates
plt.scatter(H3i_perc, y1, marker='o', color = 'black', label= "all cases")
# plt.scatter(H3i_perc, y3a, marker='o', color = 'red', label= "severe cases")
# plt.scatter(H3i_perc, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, H3i_perc, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, H3i_perc, y3a):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, H3i_perc, y3b):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('H3 isolates (% of total)')
plt.legend(loc="upper right")
plt.show()

# OR vs. percentage of B isolates
plt.scatter(Bi_perc, y1, marker='o', color = 'black', label= "all cases")
# plt.scatter(Bi_perc, y3a, marker='o', color = 'red', label= "severe cases")
# plt.scatter(Bi_perc, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, Bi_perc, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, Bi_perc, y3a):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, Bi_perc, y3b):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('B isolates (% of total)')
plt.legend(loc="upper right")
plt.show()

# OR vs. number of isolates collected
plt.scatter(TOTiso, y1, marker='o', color = 'black', label= "all cases")
# plt.scatter(TOTiso, y3a, marker='o', color = 'red', label= "severe cases")
# plt.scatter(TOTiso, y3b, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, TOTiso, y1):
	plt.annotate(num, xy = (perc, OR), xytext = (10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, TOTiso, y3a):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,0), textcoords = 'offset points')
# for num, perc, OR in zip(seasonnum, TOTiso, y3b):
# 	plt.annotate(num, xy = (perc, OR), xytext = (-10,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Number of isolates collected')
plt.legend(loc="upper right")
plt.show()







