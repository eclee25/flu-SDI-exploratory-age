#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/8/13
###Function: 
#### 1) draw OR by season charts where season is defined as the 6 weeks before and after the peak incidence week for the total population

###Import data: SQL_export/OR_swk6.csv

###Command Line: python odds_c_a_6wk_v7-8-13.py 
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##
import ORgenerator_v070813 as od 

### data structures ###
s6dict = {}
ORdict = {}

### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn from 2010 Census
seasons = range(1,11) #seasons for which ORs will be generated

### functions ###

### import data ###
s6in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_swk6.csv','r')
s6=csv.reader(s6in, delimiter=',')

### program ###
od.import_d(s6, s6dict, 0, 1, 2)
od.ORgen_seas(s6dict, ORdict, seasons)
keys = sorted(ORdict.keys())
values = [ORdict[k] for k in sorted(ORdict.keys())]
print values
# plot OR by season chart
plt.plot(keys, values, marker='o', color = 'black', label= "total")
plt.xlabel('Season number')
plt.ylabel('Attack Rate OR, c:a (US pop normalized, peak +/- 6wks)')
plt.show()
