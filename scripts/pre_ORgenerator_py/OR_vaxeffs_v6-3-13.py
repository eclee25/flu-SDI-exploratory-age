#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: June 3, 2013
###Function: 1) draw charts for OR vs weighted average of vaccine effectiveness, which was calculated from data in Table 4 in Osterholm et al.
### 2) draw charts for OR vs weighted average of vax efficacy (TIV) from Table 2 in Osterholm et al.
### 3) draw charts for OR vs weighted average of vax efficacy (LAIV) from Table 3 in Osterholm et al.
### 4) draw charts for OR vs weighted average of vax efficacy (TIV & LAIV) from Tables 2 and 3 in Osterholm et al.

###Source data: 
###Vax effectiveness and efficacy: Osterholm et al. (2012) Efficacy and effectiveness of influenza vaccines: a systematic review and meta-analysis. Lancet Infectious Diseases 12: 36-44.
###OR: SDI (see odds_c_a_v4-17-13.py)

###Import data: odds_c_a1.csv, odds_c_a3_a, odds_c_a3_b

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
rowct=[]
child1, child3a, child3b, adult1, adult3a, adult3b = [],[],[],[],[],[] # attack rates for children and adults for total, severe, and mild cases
y1, y3a, y3b = [],[],[] # odds ratios for total, severe, and mild cases


### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805

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
	rowct.append(ct)

def ORgen (ylist, childlist, adultlist):
	for i in range(0,len(childlist)):
		ylist.append((childlist[i]/(1-childlist[i]))/(adultlist[i]/(1-adultlist[i])))
	print childlist[i], 1-childlist[i], adultlist[i], 1-adultlist[i]

### import data ###
d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a1.csv','r')
d1=csv.reader(d1in, delimiter=',')
d3ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_a.csv','r')
d3a=csv.reader(d3ain, delimiter=',')
d3bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_b.csv','r')
d3b=csv.reader(d3bin, delimiter=',')

### program ###

# generate weighted avg of vax effectiveness data (Seasons 2003-04 to 2008-09)
seasonnum = [4, 5, 6, 7, 8, 9] # season number according to mysql codes
vaxefv_wt = [21.0, 35.2, 21.0, 50.3, 69.3, 67.0] # weighted avg of vax effectiveness in %

# import all season data
importer(d1, adult1, child1, 2)
importer(d3a, adult3a, child3a, 2)
importer(d3b, adult3b, child3b, 2)

# generate child:adult attack rate odds ratio for each season
ORgen(y1, child1, adult1)
ORgen(y3a, child3a, adult3a)
ORgen(y3b, child3b, adult3b)

# limit ORs to values for seasons listed in snum list
y1_trunc = y1[3:9]
y3a_trunc = y3a[3:9]
y3b_trunc = y3b[3:9]

# plot vax effectiveness
plt.scatter(vaxefv_wt, y1_trunc, marker='o', color = 'black', label= "all cases")
plt.scatter(vaxefv_wt, y3a_trunc, marker='o', color = 'red', label= "severe cases")
plt.scatter(vaxefv_wt, y3b_trunc, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, vaxefv_wt, y1_trunc):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxefv_wt, y3a_trunc):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxefv_wt, y3b_trunc):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Vaccine Effectiveness (Weighted Avg %)')
plt.legend(loc="upper left")
plt.show()


### vax efficacy TIV and LAIV ###
# generate weighted avg vax efficacy data 
seasonnum = [1, 2, 3, 5, 6, 7, 8, 9]
vaxeffT_wt = [69.1, 54.6, 64.0, 61.5, 28.1, 57.8, 60.5, 76.0]
y1_effall = list(y1)
del y1_effall[3]
del y1_effall[8]
y3a_effall = list(y3a)
del y3a_effall[3]
del y3a_effall[8]
y3b_effall = list(y3b)
del y3b_effall[3]
del y3b_effall[8]

# plot vax efficacy for weighted avg of TIV and LAIV
plt.scatter(vaxeffT_wt, y1_effall, marker='o', color = 'black', label= "all cases")
plt.scatter(vaxeffT_wt, y3a_effall, marker='o', color = 'red', label= "severe cases")
plt.scatter(vaxeffT_wt, y3b_effall, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, vaxeffT_wt, y1_effall):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxeffT_wt, y3a_effall):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxeffT_wt, y3b_effall):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Vaccine Efficacy, TIV and LAIV (Weighted Avg %)')
plt.legend(loc="upper left")
plt.show()

### vax efficacy TIV ###
seasonnum = [1, 5, 6, 7, 8, 9]
vaxefftri_wt = [-7.0, 75.0, 30.3, 57.8, 63.7, 76.0]
y1_tri = list(y1)
del y1_tri[1:4]
del y1_tri[6]
y3a_tri=list(y3a)
del y3a_tri[1:4]
del y3a_tri[6]
y3b_tri=list(y3b)
del y3b_tri[1:4]
del y3b_tri[6]

# plot vaccine efficacy for TIV data only
plt.scatter(vaxefftri_wt, y1_tri, marker='o', color = 'black', label= "all cases")
plt.scatter(vaxefftri_wt, y3a_tri, marker='o', color = 'red', label= "severe cases")
plt.scatter(vaxefftri_wt, y3b_tri, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, vaxefftri_wt, y1_tri):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxefftri_wt, y3a_tri):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxefftri_wt, y3b_tri):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Vaccine Efficacy, TIV (Weighted Avg %)')
plt.legend(loc="upper left")
plt.show()


### vax efficacy LAIV ###
seasonnum = [1, 2, 3, 5, 6, 8]
vaxeffLAIV_wt = [73.3, 54.6, 64.0, 48.0, 8.0, 36.0]
y1_LAIV = list(y1)
del y1_LAIV[3]
del y1_LAIV[5]
del y1_LAIV[6:]
y3a_LAIV=list(y3a)
del y3a_LAIV[3]
del y3a_LAIV[5]
del y3a_LAIV[6:]
y3b_LAIV=list(y3b)
del y3b_LAIV[3]
del y3b_LAIV[5]
del y3b_LAIV[6:]

# plot vaccine efficacy for LAIV data only
plt.scatter(vaxeffLAIV_wt, y1_LAIV, marker='o', color = 'black', label= "all cases")
plt.scatter(vaxeffLAIV_wt, y3a_LAIV, marker='o', color = 'red', label= "severe cases")
plt.scatter(vaxeffLAIV_wt, y3b_LAIV, marker='o', color = 'green', label= "milder cases")
for num, perc, OR in zip(seasonnum, vaxeffLAIV_wt, y1_LAIV):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxeffLAIV_wt, y3a_LAIV):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
for num, perc, OR in zip(seasonnum, vaxeffLAIV_wt, y3b_LAIV):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Vaccine Efficacy, LAIV (Weighted Avg %)')
plt.legend(loc="upper left")
plt.show()


























