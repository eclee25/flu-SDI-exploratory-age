#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 2/6/15
###Function: Redraw figure 4A in Shifting Demographic Landscape (Bansal2010)

###Import data: 

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt

## local modules ##
### data structures ###
### parameters ###
### functions ###

### import data ###
childin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/WIPS2015/importData/child_attack_rate.txt','r')
child=csv.reader(childin, delimiter='	')
adultin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/WIPS2015/importData/adult_attack_rate.txt','r')
adult=csv.reader(adultin, delimiter='	')
### program ###
childlist, adultlist = [],[]
ct=0

for item1, item2 in zip(child, adult):
	childlist = reduce(item1, []).split()
	adultlist = reduce(item2, []).split()
	ct+=1
	print ct
	
childtest = [float(c) for c in childlist]
adulttest = [float(a) for a in adultlist]
print childtest
print adulttest
plt.plot(childtest, color='red', lwd=3)
plt.lines(adulttest, color='blue', lwd=3)
plt.ylabel('Time')
plt.xlabel('Attack Rate')
plt.show()