#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/10/13
###Function: 
# 1. format data in <<FIPS>> <<OR>> and output csv file for each season (zip3s are present for all 10 seasons)
# 2. format data in <<FIPS>> <<incidence>> and output csv file for each season (zip3s are present for all 10 seasons)
# 3. format data in <<FIPS>> <<incidence>> and output csv file for each week in a single season (zip3s are present for each week in single season)

###Import data: 
# function1: SDI_Data/explore/R_export/zip3_fips_popsize.csv, zip3_ILI_season.csv

###Command Line: python create_choropleth_data.py
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import sys


## local packages ##
sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab')
import GeneralTools as gt
sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/county_maps_python_code')
import draw_maps as maps


### data structures ###
d_zf, d_fp = {},{} # zip3-all fips dictionary, fips-population size dictionary
d_zmaxf = {} # zip3-most populous fips dictionary
d_maxfz = {} # fips-list of zip3s for which that fips code is the most populous one
d_zi, d_zpopstat = {},{} # zip3-ILI dictionary per season and child marker, zip3-popstat dictionary per season and child marker
l_zip3 = [] # list of zip3s present in the ILI dataset
d_attack = {} # fips-[child ILI/child popstat, adult ILI/adult popstat] dictionary
d_OR = {} # (season, fips)-OR dictionary
### parameters ###

### functions ###
def imp_spatial (csvfile, dict_zf, dict_fp, zip3col, fipscol, popcol):
	ct=0
	for row in csvfile:
		if ct==0:
			ct+=1
			continue
		dict_fp[str(row[fipscol])] = int(row[popcol])
		if str(row[zip3col]) not in dict_zf.keys():
			dict_zf[str(row[zip3col])] = [str(row[fipscol])]
		else:
			dict_zf[str(row[zip3col])].append(str(row[fipscol]))
	print len(dict_zf.keys()), len(dict_fp.keys()) # should match number of unique zip3s and unique fips codes in imported dataset
# dict_zf = zip3-> list of fips codes
# dict_fp = fips code-> population in 2010 Census

def imp_ILI (csvfile, dict_zi, dict_zpopstat, zip3list):
	ct=0
	for row in csvfile:
		if ct==0:
			ct+=1
			continue
		if len(row[0]) == 6: # season 10
			tup = str(row[0][0:2]), str(row[0][2:5]), str(row[0][5]) # season number, zip3, child marker
			dict_zi[tup] = int(row[1])
			dict_zpopstat[tup] = int(row[2])
			zip3list.append(str(row[0][2:5]))
		elif len(row[0]) < 6: # seasons 1-9
			tup = str(row[0][0]), str(row[0][1:4]), str(row[0][4])
			dict_zi[tup] = int(row[1])
			dict_zpopstat[tup] = int(row[2])
			zip3list.append(str(row[0][1:4]))
	print len(dict_zi.keys()), len(dict_zpopstat.keys()) # should equal number of rows in csvfile
# 	for k,v in dict_zi.iteritems():
# 		print k,v 

# dict_zi = zip3-> ILI
# dict_zpopstat = zip3-> popstat

### import data ###
zfpin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/zip3_fips_popsize.csv','r')
zfp=csv.reader(zfpin, delimiter=',')
ILIin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/zip3_ILI_season.csv','r')
ILI=csv.reader(ILIin, delimiter=',')

### program ###
imp_spatial(zfp, d_zf, d_fp, 0, 1, 2) # create zip3-listoffips and fips-2010population dictionaries
imp_ILI(ILI, d_zi, d_zpopstat, l_zip3)

# create a dictionary between zip3-most populous fips code in that zip3
for z,fips in d_zf.iteritems():
	popvals = [d_fp[f] for f in fips]
	maxfip = [f for f in fips if d_fp[f] == max(popvals)]
	d_zmaxf[z] = str(maxfip[0])
# beware: some fips codes are 'most populous' for multiple zip3s. the ILI and popstat values will need to be summed these fips codes

# create a dictionary with fips-list of zip3s for which that fips code is the most populous one
for z, mf in d_zmaxf.iteritems():
	if mf not in d_maxfz.keys():
		d_maxfz[mf] = [str(z)]
	else:
		d_maxfz[mf].append(str(z))
# for k,v in d_maxfz.iteritems():
# 	print k,v 

## output: k = fips, v = attack rate for children and adults
# for each fips code, grab the associated zip3s (mult zip3s could be affiliated with a single fips code), the ILI values and the popstat values
for mf, zip3s in d_maxfz.iteritems():
	for i in range(1,11):
		ilivalsC = [d_zi[str(i), z, 'C'] for z in zip3s if z in l_zip3] # list of ILI values that correspond to these zip3s
		ilivalsA = [d_zi[str(i), z, 'A'] for z in zip3s if z in l_zip3]
		popstatvalsC = [d_zpopstat[str(i), z, 'C'] for z in zip3s if z in l_zip3] # list of popstat values that correspond to these zip3s
		popstatvalsA = [d_zpopstat[str(i), z, 'A'] for z in zip3s if z in l_zip3]
		if ilivalsC: # don't want to write empty values into dictionary
			d_attack[i, mf] = [float(sum(ilivalsC))/float(sum(popstatvalsC)), float(sum(ilivalsA))/float(sum(popstatvalsA))] # fips-[child ILI, child popstat, adult ILI, adult popstat] dictionary
			d_OR[i, mf] = (d_attack[i,mf][0]/(1-d_attack[i,mf][0]))/(d_attack[i,mf][1]/(1-d_attack[i,mf][1])) # (season, FIPS)-OR dictionary and write csv

for k,v in d_OR.iteritems():
	print k,v

# for i in range(1,11): 
# 	for k,v in d_OR.iteritems():
# 		if k[0]==i:
#  			with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/fips_OR_season%d.csv' %(i), 'a') as f:
# 				print k,v
# 				f.write(str(k[1]))
# 				f.write(',')
# 				f.write(str(v))
# 				f.write('\n')
# 	f.close()

maps.draw_maps('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/fips_OR_season1','county')


# for (name, mobile) in ab.iteritems():
#     with open(...., "a") as f:
#         print ('Contact %s at %s' % (name, mobile))
#         f.write(name)
#         f.write(mobile)




















