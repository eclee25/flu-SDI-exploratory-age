#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/6/2013
###Function: Draw charts for each season for week number (x) by odds of children ILI to adult ILI normalized by US child and adult visits of any diagnosis for each flu season

###Import data: 

###Command Line: python 
##############################################


### notes ###
# child = 5-19 yo, adult = 20-59 yo

### were there changes in reporting requirements over the years? both ILI and any diagnosis counts seem to have increased over the years and they seem particularly high for the 2009-10 flu season for both metrics even though that data is only a partial year

### are adults more likely to develop secondary symptoms such that flu-related illnesses are less likely to be categorized as flu for adults than for children? Or perhaps adults are waiting later to go to the doctor when they have the flu so their illness is categorized as something else

### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##

### data structures ###
adult2a, adult2b, adult2c, adult2d, adult2e, adult2f, adult2g, adult2h, adult2i, adult2j=[],[],[],[],[],[],[],[],[],[]
child2a, child2b, child2c, child2d, child2e, child2f, child2g, child2h, child2i, child2j=[],[],[],[],[],[],[],[],[],[]
y2a, y2b, y2c, y2d, y2e, y2f, y2g, y2h, y2i, y2j=[],[],[],[],[],[],[],[],[],[]
ad_dict = {}
adult1, child1, adult3a, child3a, adult3b, child3b = [],[],[],[],[],[]
y1, y3a, y3b = [],[],[]

### parameters ###

### functions ###
def importer2 (csvreadfile, adultlist, childlist, ilicol, seasonnum):
	for row in csvreadfile:
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/float(ad_dict[str(seasonnum)+"A"]))
			#print float(row[ilicol]), float(ad_dict[str(seasonnum)+"A"])
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/float(ad_dict[str(seasonnum)+"C"]))
			#print float(row[ilicol]), float(ad_dict[str(seasonnum)+"C"])

def ORgen (ylist, childlist, adultlist):
	for i in range(0,len(childlist)):
		ylist.append((childlist[i]/(1-childlist[i]))/(adultlist[i]/(1-adultlist[i])))
		print childlist[i], 1-childlist[i], adultlist[i], 1-adultlist[i]

def importer3 (csvreadfile, adultlist, childlist, ilicol):
	for row in csvreadfile:
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/float(ad_dict[str(row[0])+"A"]))
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/float(ad_dict[str(row[0])+"C"]))
			
### import data ###
anydiagin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/anydiag.csv','r')
anydiag=csv.reader(anydiagin, delimiter=',')
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

# import any diagnosis count 
for row in anydiag:
	ad_smarker = str(row[0])+str(row[1])
	ad_visits = float(row[2])
	ad_dict[ad_smarker] = ad_visits

# import weekly data normalized by any diagnosis counts for each flu season
importer2(d2a, adult2a, child2a, 3, 1)
importer2(d2b, adult2b, child2b, 3, 2)
importer2(d2c, adult2c, child2c, 3, 3)
importer2(d2d, adult2d, child2d, 3, 4)
importer2(d2e, adult2e, child2e, 3, 5)
importer2(d2f, adult2f, child2f, 3, 6)
importer2(d2g, adult2g, child2g, 3, 7)
importer2(d2h, adult2h, child2h, 3, 8)
importer2(d2i, adult2i, child2i, 3, 9)
importer2(d2j, adult2j, child2j, 3, 10)

# generate odds ratios
ORgen(y2a, child2a, adult2a)
ORgen(y2b, child2b, adult2b)
ORgen(y2c, child2c, adult2c)
ORgen(y2d, child2d, adult2d)
ORgen(y2e, child2e, adult2e)
ORgen(y2f, child2f, adult2f)
ORgen(y2g, child2g, adult2g)
ORgen(y2h, child2h, adult2h)
ORgen(y2i, child2i, adult2i)
ORgen(y2j, child2j, adult2j)

x2 = range(0,33)
x2lab=range(40,53)+range(1,21)
y2e.pop(13) 
y2j.pop(13)

# plot
#plt.plot(x2, y2a, marker='o', color = 'grey', label= "season 1")
plt.plot(x2, y2b, marker='o', color = 'black', label= "01-02")
plt.plot(x2, y2c, marker='o', color = 'red', label= "02-03")
plt.plot(x2, y2d, marker='o', color = 'orange', label= "03-04")
plt.plot(x2, y2e, marker='o', color = 'gold', label= "04-05")
plt.plot(x2, y2f, marker='o', color = 'green', label= "05-06")
plt.plot(x2, y2g, marker='o', color = 'blue', label= "06-07")
plt.plot(x2, y2h, marker='o', color = 'cyan', label= "07-08")
plt.plot(x2, y2i, marker='o', color = 'darkviolet', label= "08-09")
plt.plot(x2, y2j, marker='o', color = 'hotpink', label= "09-10")
plt.xlabel('Week number')
plt.ylabel('Odds ratio of attack rate, child:adult (any visit ct normalized)') #5-16-13 changed label
ylim([0,15])
plt.legend(loc="lower right")
plt.xticks(x2, x2lab, rotation = 90)
plt.show()


# adults and children have similar numbers of ILI visits, but adults visit the doctor magnitudes more often than do children


############# all seasons chart ###############
# import total data
importer3(d1, adult1, child1, 2)
importer3(d3a, adult3a, child3a, 2)
importer3(d3b, adult3b, child3b, 2)
x1 = range(1,11,1)

# generate child:adult attack rate odds ratio for each season
ORgen(y1, child1, adult1)
ORgen(y3a, child3a, adult3a)
ORgen(y3b, child3b, adult3b)

# plot
plt.plot(x1, y1, marker='o', color = 'black', label= "total")
plt.plot(x1, y3a, marker='o', color = 'red', label= "severe cases")
plt.plot(x1, y3b, marker='o', color = 'green', label = "milder cases")
plt.xlabel('Season number')
plt.ylabel('Odds ratio of attack rate, child:adult (any visit ct normalized)')
ylim([0,12])
plt.legend(loc="upper left")
plt.show()



