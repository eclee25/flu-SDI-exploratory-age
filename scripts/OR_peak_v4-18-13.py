#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 5/16/13
###Function: 
######## Find peakweek and attack rate of peakweek among children, adults, and total population
######## Plot scatter: child:adult OR (x-axis) vs. peakweek child, adult, and total (y-axis)
######## Plot scatter: child:adult OR (x-axis) vs. attack rate of peakweek child, adult, and total (y-axis)

###Import data: odds_c_a1.csv, odds_c_a3_a, odds_c_a3_b, odds_c_a2_a through j

###Command Line: python 
##############################################


### notes ###
# peak values for child and adult are normalized over US population; peak values for total population are simply ILI sums
# 2010 Census age demographics, table 2: http://www.census.gov/prod/cen2010/briefs/c2010br-03.pdf
# child = 5-19 yo, adult = 20-59 yo

### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import datetime

## local packages ##

### data structures ###
peakweek_c, peakweek_a, peakweek_t = [],[],[] #unadjusted week number of peakweek ILI counts divided by US population of age group
peakval_c, peakval_a, peakval_t = [],[],[] #values of peakweek ILI counts divided by US population of age group
peakwknum_c, peakwknum_a, peakwknum_t = [],[],[] #peak week number for each flu season
peakwkplot_c, peakwkplot_a, peakwkplot_t = [],[],[] #peak week number for plotting on the y-axis
adult2a, adult2b, adult2c, adult2d, adult2e, adult2f, adult2g, adult2h, adult2i, adult2j=[],[],[],[],[],[],[],[],[],[] #adultlist for peakweek
child2a, child2b, child2c, child2d, child2e, child2f, child2g, child2h, child2i, child2j=[],[],[],[],[],[],[],[],[],[] #childlist for peakweek
total2a, total2b, total2c, total2d, total2e, total2f, total2g, total2h, total2i, total2j=[],[],[],[],[],[],[],[],[],[] #totallist for peakweek
date2a, date2b, date2c, date2d, date2e, date2f, date2g, date2h, date2i, date2j=[],[],[],[],[],[],[],[],[],[] #datelist

x1, x3a, x3b=[],[],[] #single season OR, regular, severe, mild
adult1, adult3a, adult3b, child1, child3a, child3b=[],[],[],[],[],[]#adult and child lists for single season OR


### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn
UStotal = 308745538 #US total population


### functions ###
def importer_y (csvreadfile, adultlist, childlist, ilicol, datelist, totallist):
	ct=0
	for row in csvreadfile:
		yr = int(row[2][:4])
		month = int(row[2][5:7])
		day = int(row[2][8:])
		date = datetime.date(yr, month, day)
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/USadult)
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/USchild)
		else:
			ct+=1
			totallist.append(float(USadult*adultlist[-1] + USchild*childlist[-1] + float(row[ilicol]))/UStotal)
			datelist.append(date)

def importer (csvreadfile, adultlist, childlist, ilicol):
	ct=0	
	for row in csvreadfile:
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/USadult)
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/USchild)
		else:
			ct+=1

def peakweekval (c_alist, datelist, peakweeklist, peakvallist):
	dummymax = max(c_alist)
	maxindex = [index for index, item in enumerate(c_alist) if item == dummymax]
	peakweeklist.append(datelist[maxindex[0]])
	peakvallist.append(dummymax)
	
def ORgen (ylist, childlist, adultlist):
	for i in range(0,len(childlist)):
		ylist.append(float((childlist[i]/(1-childlist[i]))/(adultlist[i]/(1-adultlist[i]))))
# 	print childlist[i], 1-childlist[i], adultlist[i], 1-adultlist[i] # check on OR calc
	
def valtoplot (vallist, plotlist):
	for i in vallist:
		if i > 39:
			plotlist.append(int(i-39)) #set wk40 at 1 on y-axs, assume 53 weeks in a year
		elif i < 40:
			plotlist.append(int(i+14))

### import data ###
d2ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_a.csv','r')
d2a=csv.reader(d2ain, delimiter=',')
d2bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_b.csv','r')
d2b=csv.reader(d2bin, delimiter=',')
d2cin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_c.csv','r')
d2c=csv.reader(d2cin, delimiter=',')
d2din=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_d.csv','r')
d2d=csv.reader(d2din, delimiter=',')
d2ein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_e.csv','r')
d2e=csv.reader(d2ein, delimiter=',')
d2fin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_f.csv','r')
d2f=csv.reader(d2fin, delimiter=',')
d2gin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_g.csv','r')
d2g=csv.reader(d2gin, delimiter=',')
d2hin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_h.csv','r')
d2h=csv.reader(d2hin, delimiter=',')
d2iin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_i.csv','r')
d2i=csv.reader(d2iin, delimiter=',')
d2jin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a2_j.csv','r')
d2j=csv.reader(d2jin, delimiter=',')

d1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a1.csv','r')
d1=csv.reader(d1in, delimiter=',')
d3ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_a.csv','r')
d3a=csv.reader(d3ain, delimiter=',')
d3bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/odds_c_a3_b.csv','r')
d3b=csv.reader(d3bin, delimiter=',')

### program ###

# generate y-axis PEAK WEEK
# importer(d2a, adult2a, child2a, 3, adultdate2a, date2a, total2a) #incomplete flu season's worth of data
importer_y(d2b, adult2b, child2b, 3, date2b, total2b)
importer_y(d2c, adult2c, child2c, 3, date2c, total2c)
importer_y(d2d, adult2d, child2d, 3, date2d, total2d)
importer_y(d2e, adult2e, child2e, 3, date2e, total2e)
importer_y(d2f, adult2f, child2f, 3, date2f, total2f)
importer_y(d2g, adult2g, child2g, 3, date2g, total2g)
importer_y(d2h, adult2h, child2h, 3, date2h, total2h)
importer_y(d2i, adult2i, child2i, 3, date2i, total2i)
importer_y(d2j, adult2j, child2j, 3, date2j, total2j)
# peakweekval(adult2a, date2a, peakweek_a, peakval_a)
peakweekval(adult2b, date2b, peakweek_a, peakval_a)
peakweekval(adult2c, date2c, peakweek_a, peakval_a)
peakweekval(adult2d, date2d, peakweek_a, peakval_a)
peakweekval(adult2e, date2e, peakweek_a, peakval_a)
peakweekval(adult2f, date2f, peakweek_a, peakval_a)
peakweekval(adult2g, date2g, peakweek_a, peakval_a)
peakweekval(adult2h, date2h, peakweek_a, peakval_a)
peakweekval(adult2i, date2i, peakweek_a, peakval_a)
peakweekval(adult2j, date2j, peakweek_a, peakval_a)
# peakweekval(child2a, date2a, peakweek_c, peakval_c)
peakweekval(child2b, date2b, peakweek_c, peakval_c)
peakweekval(child2c, date2c, peakweek_c, peakval_c)
peakweekval(child2d, date2d, peakweek_c, peakval_c)
peakweekval(child2e, date2e, peakweek_c, peakval_c)
peakweekval(child2f, date2f, peakweek_c, peakval_c)
peakweekval(child2g, date2g, peakweek_c, peakval_c)
peakweekval(child2h, date2h, peakweek_c, peakval_c)
peakweekval(child2i, date2i, peakweek_c, peakval_c)
peakweekval(child2j, date2j, peakweek_c, peakval_c)
# peakweekval(total2a, date2a, peakweek_t, peakval_t)
peakweekval(total2b, date2b, peakweek_t, peakval_t)
peakweekval(total2c, date2c, peakweek_t, peakval_t)
peakweekval(total2d, date2d, peakweek_t, peakval_t)
peakweekval(total2e, date2e, peakweek_t, peakval_t)
peakweekval(total2f, date2f, peakweek_t, peakval_t)
peakweekval(total2g, date2g, peakweek_t, peakval_t)
peakweekval(total2h, date2h, peakweek_t, peakval_t)
peakweekval(total2i, date2i, peakweek_t, peakval_t)
peakweekval(total2j, date2j, peakweek_t, peakval_t)

for d in range(len(peakweek_a)):
	peakwknum_a.append(peakweek_a[d].isocalendar()[1])
	peakwknum_c.append(peakweek_c[d].isocalendar()[1])
	peakwknum_t.append(peakweek_t[d].isocalendar()[1])

# y-axis values
print peakwknum_c #week number for child peak
print peakwknum_a #week number for adult peak
print peakwknum_t
# 01-02; 02-03; 03-04; 04-05; 05-06; 06-07; 07-08; 08-09; 09-10
# peak weeks do not necessarily correspond to max odds ratio weeks (although they sometimes do)
# children peak prior to or at the same time as adults
# 08-09 season, child peakweek represents seasonal peak and adult peak is an artifact of the H1N1 reports. Child seasonal peak was greater than the jump in ILI counts due to the H1N1 reports. Adult seasonal peak week was actually also in week 8 (same as the child and total population seasonal peak week)

# x-axis for plotting
valtoplot(peakwknum_c, peakwkplot_c)
valtoplot(peakwknum_a, peakwkplot_a)
valtoplot(peakwknum_t, peakwkplot_t)

# generate y-axis OR by season
# import total data
importer(d1, adult1, child1, 2)
# importer(d3a, adult3a, child3a, 2) # if we want to do severe and mild comparisons for peakweek as well
# importer(d3b, adult3b, child3b, 2)

# generate child:adult attack rate odds ratio for each season
ORgen(x1, child1, adult1)
# ORgen(x3a, child3a, adult3a)
# ORgen(x3b, child3b, adult3b)

# drop season 1 data bc 00-01 is incomplete
x1=x1[1:]
x1a=[i+.02 for i in x1]
x1c=[i-.02 for i in x1]
x1lab = range(2,11) # changed x1lab to reflect season numbers in the mysql database 5/20/13 ECL

# xticks - peakweek plot
y2 = range(1,35)
y2lab=range(40,54)+range(1,21)

# swap axes ECL 5-17-13
# plot OR vs. peakweek
plt.scatter(peakwkplot_t, x1, marker='o', color = 'black', label= "total popn")
plt.scatter(peakwkplot_c, x1c, marker='o', color = 'lightskyblue', label= "child (5-19)")
plt.scatter(peakwkplot_a, x1a, marker='o', color = 'red', label= "adult (20-59)")
for val, label, peakwkplot_t in zip(x1, x1lab, peakwkplot_t):
	plt.annotate(label, xy = (peakwkplot_t, val), xytext = (-5,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Peak week')
plt.legend(loc="upper left")
plt.xticks(y2, y2lab)
plt.show()

# attack rate per 100,000
peakval_tplt = [i*100000 for i in peakval_t]
peakval_cplt = [i*100000 for i in peakval_c]
peakval_aplt = [i*100000 for i in peakval_a]

print peakval_cplt
print peakval_aplt

# plot OR vs. peakweek attack rate
plt.scatter(peakval_tplt, x1, marker='o', color = 'black', label= "total popn")
plt.scatter(peakval_cplt, x1, marker='o', color = 'lightskyblue', label= "child (5-19)")
plt.scatter(peakval_aplt, x1, marker='o', color = 'red', label= "adult (20-59)")
for x1, label, peakval_tplt in zip(x1, x1lab, peakval_tplt):
	plt.annotate(label, xy = (peakval_tplt, x1), xytext = (0,5), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (US popn normalized)')
plt.xlabel('Peak week attack rate (per 100,000)')
plt.legend(loc="lower right")
plt.show()













