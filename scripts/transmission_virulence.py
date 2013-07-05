#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 3/27/13
###Function: Draw chart representing relationship between transmission and virulence in the SDI data, where tranmission is estimated by percent prevalence of ILI visits among all doctor's visits that week and virulence is estimated by percent ILI vists to acute care facilities among ILI visits that week.
###Import data: H1a, H1b

###Command Line: ipython transmission_virulence.py
##############################################


### notes ###
# python closing index values are one greater than the actual index

### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##

### data structures ###
wk=[]			#week from H1a
ili_tot=[]		#total ili cases that week across all service places
incid_perc=[]	#ili cases/total vists that week*100
wk_dup=[]		#week from H1b
ili_acute=[]	#total acute cases that week 
acute_perc=[]	#acute cases/total ili cases*100

### parameters ###

### functions ###

### import data ###
H1ain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/H1a.csv','r')
H1a=csv.reader(H1ain, delimiter=',')
H1bin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export/H1b.csv','r')
H1b=csv.reader(H1bin, delimiter=',')

### program ###

# generate data
for row in H1a:	
	wk.append(row[0])
	ili_tot.append(float(row[1]))
#	incid_perc.append(float(row[3])) # different denominator than US popn (which is what is used below)
for row in H1b:
	wk_dup.append(row[0])
	ili_acute.append(float(row[1]))
b= len(ili_acute)
for i in range(0,b):
	acute_perc.append(ili_acute[i]/ili_tot[i]*100)
	print ili_acute[i], ili_tot[i], ili_acute[i]/ili_tot[i]
incid_perc = [x/308745538 * 1000000 for x in ili_tot]
# 2010 US population = 308,745,538 based on Census

# draw charts
scatter(incid_perc, acute_perc, marker = 'o', color='black')
plt.ylabel('percent acute care ILI cases of all ILI cases')
plt.xlabel('ILI cases per 1,000,000 people')
plt.show()








