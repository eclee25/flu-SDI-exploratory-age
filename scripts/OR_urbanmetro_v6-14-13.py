#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/14/13
###Function: 
#### 1) create scatter of OR by zipcode vs. urban metro RUCC avg 2013

### Update from 6/7/13 version
#### removed zip3s that did not have complete age group data in a single season so need to change import data and redraw charts
#### ORs represent means of ORs normalized by age-specific zip3 popstat instead of attack rate divided by size of child and adult US populations (as did 6/7 version); consequently, import data has changed from odds_c_a1, odds_c_a3_a, odds_c_a3_b to zipcode_bysseas datasets


###Import data: zipcode_bysseas_cl_v6-12-13.csv; zipcode_cl_1v6-12-13.csv through zipcode_cl_10v6-12-13.csv

###Command Line: python OR_urbanmetro_v6-14-13.py
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


## local packages ##
import ORgenerator_v060713 as od

### data structures ###
child1, adult1, zip3_sdi, snum_sdi = [],[],[],[] # attack rates for children and adults for total by zipcode, zip3s from sdi data, season number in sdi data
y1 = [] # odds ratios for total cases by zipcode
zipdict, rucc_bin = {},[] # dictionary of zip3 and rural-urban categorization, list of rucc 1-3 bins that correspond with order of zip3s in sdi data
cs1, cs2, cs3, cs4, cs5, cs6, cs7, cs8, cs9, cs10 = [],[],[],[],[],[],[],[],[],[] # childlist for seasons 1-10
as1, as2, as3, as4, as5, as6, as7, as8, as9, as10 = [],[],[],[],[],[],[],[],[],[] # adultlist for seasons 1-10
ys1, ys2, ys3, ys4, ys5, ys6, ys7, ys8, ys9, ys10 = [],[],[],[],[],[],[],[],[],[] # OR for seasons 1-10
rbs1, rbs2, rbs3, rbs4, rbs5, rbs6, rbs7, rbs8, rbs9, rbs10 = [],[],[],[],[],[],[],[],[],[] # rucc_mn_bin for seasons 1-10
z3s1, z3s2, z3s3, z3s4, z3s5, z3s6, z3s7, z3s8, z3s9, z3s10 = [],[],[],[],[],[],[],[],[],[] # zip3_sdi for seasons 1-10
sns1, sns2, sns3, sns4, sns5, sns6, sns7, sns8, sns9, sns10 = [],[],[],[],[],[],[],[],[],[] # season number from sdi data for dataset broken into seasons 1-10

### parameters ###

### functions ###
# create a dictionary of zip3, rural-urban categorization as key, value
def createzipdict(csvreadfile, dictname):
	ct=0
	for row in csvreadfile:
		if ct==0:
			ct+=1
			continue
		else: 
			zipdict[str(row[0])] = int(row[3])


### import data ### # 6/14 change import file names
zORin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_bysseas_cl_v6-12-13.csv','r') # use to calculate OR by zip3
zOR=csv.reader(zORin, delimiter=',')
zOR1in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_1v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR1=csv.reader(zOR1in, delimiter=',')
zOR2in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_2v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR2=csv.reader(zOR2in, delimiter=',')
zOR3in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_3v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR3=csv.reader(zOR3in, delimiter=',')
zOR4in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_4v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR4=csv.reader(zOR4in, delimiter=',')
zOR5in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_5v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR5=csv.reader(zOR5in, delimiter=',')
zOR6in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_6v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR6=csv.reader(zOR6in, delimiter=',')
zOR7in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_7v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR7=csv.reader(zOR7in, delimiter=',')
zOR8in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_8v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR8=csv.reader(zOR8in, delimiter=',')
zOR9in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_9v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR9=csv.reader(zOR9in, delimiter=',')
zOR10in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_cl_10v6-12-13.csv','r') # use to calculate OR by zip3 (one season chart)
zOR10=csv.reader(zOR10in, delimiter=',')
RUCCavgin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Rural_Urban/R_export/zip3_RUCC2013avg_crosswalk.csv','r') # categorization of urban/rural by zip3
RUCCavg=csv.reader(RUCCavgin, delimiter=',')


### program ###

### analyze all zip3-season data together to see if there are patterns
createzipdict(RUCCavg, zipdict)
od.importer_zip3(zOR, adult1, child1, 3, 4, zip3_sdi, 2, snum_sdi, zipdict, rucc_bin) 
print "rucc_binlen:", len(rucc_bin)
print "child1len:", len(child1), "adult1len:", len(adult1)
od.ORgen(y1, child1, adult1)
print "y1len:", len(y1)

# OR vs. urban rural code (all seasons together)
rulab = ['populous urban metro area', 'small metro area', 'rural non-metro area']
xaxjitter = [x + np.random.uniform(-0.4, 0.4, 1) for x in rucc_bin]
print "length x-axis jitter:",len(xaxjitter)
plt.scatter(xaxjitter, y1, marker='o', color = 'black', label= "zipcode prefix")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
plt.show()
# urban areas tend to have larger ranges of ORs
# number of zip3s: 396 populous urban metro - 322 smaller urban metro - 167 rural (note: not all zip3s are available for all the seasons)


#### analyze ORs by season
od.importer_zip3(zOR1, as1, cs1, 3, 4, z3s1, 2, sns1, zipdict, rbs1)
print "rucc_binlen:", len(rbs1)
print "childlen:", len(cs1), "adultlen:", len(as1)
od.ORgen(ys1, cs1, as1)
print "ylen:", len(ys1)

od.importer_zip3(zOR2, as2, cs2, 3, 4, z3s2, 2, sns2, zipdict, rbs2)
od.importer_zip3(zOR3, as3, cs3, 3, 4, z3s3, 2, sns3, zipdict, rbs3)
od.importer_zip3(zOR4, as4, cs4, 3, 4, z3s4, 2, sns4, zipdict, rbs4)
od.importer_zip3(zOR5, as5, cs5, 3, 4, z3s5, 2, sns5, zipdict, rbs5)
od.importer_zip3(zOR6, as6, cs6, 3, 4, z3s6, 2, sns6, zipdict, rbs6)
od.importer_zip3(zOR7, as7, cs7, 3, 4, z3s7, 2, sns7, zipdict, rbs7)
od.importer_zip3(zOR8, as8, cs8, 3, 4, z3s8, 2, sns8, zipdict, rbs8)
od.importer_zip3(zOR9, as9, cs9, 3, 4, z3s9, 2, sns9, zipdict, rbs9)
od.importer_zip3(zOR10, as10, cs10, 3, 4, z3s10, 2, sns10, zipdict, rbs10)
od.ORgen(ys2, cs2, as2)
od.ORgen(ys3, cs3, as3)
od.ORgen(ys4, cs4, as4)
od.ORgen(ys5, cs5, as5)
od.ORgen(ys6, cs6, as6)
od.ORgen(ys7, cs7, as7)
od.ORgen(ys8, cs8, as8)
od.ORgen(ys9, cs9, as9)
od.ORgen(ys10, cs10, as10)
# OR vs. urban rural code by season
rulab = ['populous urban metro area', 'small metro area', 'rural non-metro area']
xaxjs1 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs1]
print "ys1:",len(ys1),"length x-axis jitter:",len(xaxjs1)
xaxjs2 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs2]
print "ys2:",len(ys2),"length x-axis jitter:",len(xaxjs2)
xaxjs3 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs3]
print "ys3:",len(ys3),"length x-axis jitter:",len(xaxjs3)
xaxjs4 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs4]
print "ys4",len(ys4),"length x-axis jitter:",len(xaxjs4)
xaxjs5 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs5]
print "ys5:",len(ys5),"length x-axis jitter:",len(xaxjs5)
xaxjs6 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs6]
print "ys6:",len(ys6),"length x-axis jitter:",len(xaxjs6)
xaxjs7 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs7]
print "ys7:",len(ys7),"length x-axis jitter:",len(xaxjs7)
xaxjs8 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs8]
print "ys8:",len(ys8),"length x-axis jitter:",len(xaxjs8)
xaxjs9 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs9]
print "ys9:",len(ys9),"length x-axis jitter:",len(xaxjs9)
xaxjs10 = [x + np.random.uniform(-0.4, 0.4, 1) for x in rbs10]
print "ys10:",len(ys10),"length x-axis jitter:",len(xaxjs10)

plt.scatter(xaxjs1, ys1, marker='o', color = 'grey', label= "Season 1")
plt.scatter(xaxjs2, ys2, marker='o', color = 'black', label= "Season 2")
plt.scatter(xaxjs3, ys3, marker='o', color = 'red', label= "Season 3")
plt.scatter(xaxjs4, ys4, marker='o', color = 'orange', label= "Season 4")
plt.scatter(xaxjs5, ys5, marker='o', color = 'gold', label= "Season 5")
plt.scatter(xaxjs6, ys6, marker='o', color = 'green', label= "Season 6")
plt.scatter(xaxjs7, ys7, marker='o', color = 'blue', label= "Season 7")
plt.scatter(xaxjs8, ys8, marker='o', color = 'cyan', label= "Season 8")
plt.scatter(xaxjs9, ys9, marker='o', color = 'darkviolet', label= "Season 9")
plt.scatter(xaxjs10, ys10, marker='o', color = 'hotpink', label= "Season 10")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
plt.show()


# OR vs. urban rural code each season
plt.scatter(xaxjs1, ys1, marker='o', color = 'grey', label= "Season 1")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs1, ys1, z3s1):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs2, ys2, marker='o', color = 'black', label= "Season 2")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs2, ys2, z3s2):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs3, ys3, marker='o', color = 'red', label= "Season 3")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs3, ys3, z3s3):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs4, ys4, marker='o', color = 'orange', label= "Season 4")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs4, ys4, z3s4):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs5, ys5, marker='o', color = 'gold', label= "Season 5")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs5, ys5, z3s5):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs6, ys6, marker='o', color = 'green', label= "Season 6")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs6, ys6, z3s6):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs7, ys7, marker='o', color = 'blue', label= "Season 7")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs7, ys7, z3s7):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show() 

plt.scatter(xaxjs8, ys8, marker='o', color = 'cyan', label= "Season 8")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs8, ys8, z3s8):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs9, ys9, marker='o', color = 'darkviolet', label= "Season 9")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs9, ys9, z3s9):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()

plt.scatter(xaxjs10, ys10, marker='o', color = 'hotpink', label= "Season 10")
xlab=[1,2,3]
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popn normalized)')
plt.xlabel('Urban metro categorization')
plt.legend(loc="upper right")
plt.xticks(xlab, rulab)
for x, y, lab in zip(xaxjs10, ys10, z3s10):
	plt.annotate(lab, xy = (x, y), xytext = (5,0), textcoords = 'offset points')
plt.show()








