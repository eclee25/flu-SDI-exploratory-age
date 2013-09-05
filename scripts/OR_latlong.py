#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 9/3/13
###Function: 
#### draw OR vs latitude chart
#### draw OR vs longitude chart

###Import data: Py_export/zip3_OR_season.txt, Py_export/zip3_ll.txt

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys

## local modules ##
import ORgenerator as od

### data structures ###
d_z311, d_z3ORs = {}, {}

### parameters ###
seasons = range(1,11) # seasons for which ORs will be generated

### functions ###


### import data ###
f1 = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/zip3_ll.txt','r')
f2 =  open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/zip3_OR_season.txt','r')

### plotting settings ###
colorvec = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
labelvec = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10']

### program ###
d_z3ll = od.import_z3_ll(f1)
d_z3ORs = od.import_z3_OR_season(f2)

## OR by latitude, one chart per season ##

# note: it is necessary to separate keys and zip3s by season because different seasons have different zip3 data in them
for s in seasons:
	# list of keys for season s chart
	keys = [k for k in d_z3ORs if k[0] == s]
	# ORs for y-axis
	ORs = [d_z3ORs[k] for k in keys]
	# list of zip3s for season s chart
	zip3s = [k[1] for k in keys]
	# latitudes for x-axis
	lats = [d_z3ll[z3][0] for z3 in zip3s]
	
	# plot points for season
	plt.scatter(lats, ORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1])
plt.xlabel('Latitude (S to N)')
plt.ylabel('OR')
plt.legend(loc = 'upper left')
plt.xlim([20, 50])
plt.show()

## OR by longitude, one chart per season ##

for s in seasons:
	# list of keys for season s chart
	keys = [k for k in d_z3ORs if k[0] == s]
	# ORs for y-axis
	ORs = [d_z3ORs[k] for k in keys]
	# list of zip3s for season s chart
	zip3s = [k[1] for k in keys]
	# longitudes for x-axis
	lats = [d_z3ll[z3][1] for z3 in zip3s]
	
	# plot points for season
	plt.scatter(lats, ORs, marker = 'o', color = colorvec[s-1], label = labelvec[s-1])
plt.xlabel('Longitude (W to E)')
plt.ylabel('OR')
plt.legend(loc = 'upper left')
plt.xlim([-160, -65])
plt.show()













