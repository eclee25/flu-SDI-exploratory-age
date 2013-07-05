#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 5/21/13
###Function: 
##	1. draw a histogram of the populations and analyze because the definitions of urban and rural need to be redefined to fit zipcode prefix areas. Census defines urban and rural for cities, towns and villages, but this does not fit the zipcode prefix area (urbanized areas: 50,000 or more; urban clusters: 2,500 to less than 50,000; rural: fewer than 2,500)
##	2. instead of an urban-rural x-axis, split into population

###Import data: popstat_by_zip3_2010.csv

###Command Line: python OR_popstat_v5-21-13.py
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
zip3, popstat = [],[]

### parameters ###


### functions ###


### import data ###
popin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/popstat_by_zip3_2010.csv','r')
pop=csv.reader(popin, delimiter=',')

### program ###

for row in pop:
	zip3.append(row[1])
	popstat.append(float(row[2]))

zip3.pop()
popstat.pop() # remove last value of each list because it represents the total population across all zip3s


# histogram of data
n, bins, patches = plt.hist(popstat, 25, normed = 1, histtype='bar')
plt.xlabel('popstat')
plt.ylabel('density')
plt.show()

# display deciles, quantiles
# 0%: 0.0
# 25%: 105,774.5
# 50%: 202,375
# 75%: 432,941.5
# 100%: 3,003,916
quants = np.percentile(popstat, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print quants # 48395.8, 83765.6, 126030, 167033.4, 202375, 267947.4, 365125.4, 513930.8, 779568.4, 3003916













