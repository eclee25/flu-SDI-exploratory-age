#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/10/13
###Function: 
# 1. format data in <<FIPS>> <<OR>> and output csv file for each season (zip3s are present for all 10 seasons)
# 2. format data in <<FIPS>> <<incidence>> and output csv file for each season (zip3s are present for all 10 seasons)
# 3. format data in <<FIPS>> <<incidence>> and output csv file for each week in a single season (zip3s are present for each week in single season)

# edits 7/14/13
### Export the following datasets for plotting
# 1. OR across ~500 zip3s, 1 map per season: dict[(seasonnum, zip3)] = OR
# 2. total incidence across ~ 500 zip3s, 1 map per season: dict[(seasonnum, zip3)] = (ILI, popsize)
# 3. total incidence across ~ 800 zip3s, 1 map per week (season needs to be chosen): dict[(seas, wk, zip3)] = (ILI, popsize)
# 4. all US maps: dict[zip3] = (lat, long)

### Import data: 
# function1: SDI_Data/explore/R_export/zip3_fips_popsize.csv, zip3_ILI_season.csv

# for export1: R_export/zip3_fips_popsize.csv, zip3_ILI_season.csv
# for export2: 
# for export3: SDI_Data/explore/SQL_export/choropleth_v7-1-13.csv
# for export4: mapping_code/Coord3digits.csv

### Export data:
# export1: Py_export/zip3_OR_season.txt
# export2:
# export3: Py_export/zip3_ILI_popstat_week.txt
# export4: Py_export/zip3_ll.txt

###Command Line: python create_choropleth_data.py
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import date


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
d_attack, d_OR = {},{} # fips-[child ILI/child popstat, adult ILI/adult popstat] dictionary, (season, fips)-OR dictionary
d_zOR = {} # zip3-OR dictionary

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
		if len(row[0]) == 6: # season 10, ID is one digit longer
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

### program choropleth attempt ###
imp_spatial(zfp, d_zf, d_fp, 0, 1, 2) # create zip3-listoffips and fips-2010population dictionaries
imp_ILI(ILI, d_zi, d_zpopstat, l_zip3)

# create a dictionary between zip3-most populous fips code in that zip3
for z,fips in d_zf.iteritems():
	popvals = [d_fp[f] for f in fips]
	maxfip = [f for f in fips if d_fp[f] == max(popvals)]
	d_zmaxf[z] = str(maxfip[0])
# beware: some fips codes are 'most populous' for multiple zip3s. the ILI and popstat values will need to be summed these fips codes


##### zip3 - most populous fips code module ##############
#
# # create a dictionary with fips-list of zip3s for which that fips code is the most populous one
# for z, mf in d_zmaxf.iteritems():
# 	if mf not in d_maxfz.keys():
# 		d_maxfz[mf] = [str(z)]
# 	else:
# 		d_maxfz[mf].append(str(z))
# # print d_maxfz.items():


## ECL commented out 7/14/13 because the fips code designation did not represent a large spatial error in the US. Zip3 to lat/long is the alternative we will pursue.
## output: k = fips, v = attack rate for children and adults
# # for each fips code, grab the associated zip3s (mult zip3s could be affiliated with a single fips code), the ILI values and the popstat values
# for mf, zip3s in d_maxfz.iteritems():
# 	for i in range(1,11):
# 		ilivalsC = [d_zi[str(i), z, 'C'] for z in zip3s if z in l_zip3] # list of ILI values that correspond to these zip3s
# 		ilivalsA = [d_zi[str(i), z, 'A'] for z in zip3s if z in l_zip3]
# 		popstatvalsC = [d_zpopstat[str(i), z, 'C'] for z in zip3s if z in l_zip3] # list of popstat values that correspond to these zip3s
# 		popstatvalsA = [d_zpopstat[str(i), z, 'A'] for z in zip3s if z in l_zip3]
# 		if ilivalsC: # don't want to write empty values into dictionary
# 			d_attack[i, mf] = [float(sum(ilivalsC))/float(sum(popstatvalsC)), float(sum(ilivalsA))/float(sum(popstatvalsA))] # fips-[child ILI, child popstat, adult ILI, adult popstat] dictionary
# 			d_OR[i, mf] = (d_attack[i,mf][0]/(1-d_attack[i,mf][0]))/(d_attack[i,mf][1]/(1-d_attack[i,mf][1])) # (season, FIPS)-OR dictionary and write csv
# print "length of d_OR:", len(d_OR.keys())


## data for fips code-based choropleths
# for i in range(1,11): 
# 	for k,v in d_OR.iteritems():
# 		if k[0]==i:
#  			with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/fips_OR_season%d.txt' %(i), 'a') as f:
# 				print k,v
# 				f.write(str(k[1]))
# 				f.write(',')
# 				f.write(str(v))
# 				f.write('\n')
# 	f.close()

# maps.draw_maps('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/fips_OR_season8','county')
##### end zip3 - most populous fips code module ###############


############ zip3 - lat/long module #####################
## edits 7/14/13
### Export the following datasets: 

# 1. dict[(seasonnum, zip3)] = OR
for z in l_zip3:
	for i in range(1,11):
		iliC, iliA, popC, popA = float(d_zi[str(i), z, 'C']), float(d_zi[str(i), z, 'A']), float(d_zpopstat[str(i), z, 'C']), float(d_zpopstat[str(i), z, 'A'])
		attackC, attackA = iliC/popC, iliA/popA
		if iliC:
			d_zOR[i, str(z)] = (attackC/(1-attackC))/(attackA/(1-attackA))
#print d_zOR.items():
 
# print "length d_zOR: ",len(d_zOR.keys())
# with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/zip3_OR_season.txt', 'a') as f:
# 	for k,v in d_zOR.iteritems():
# 		print k,v
# 		f.write(str(k[0])) # season number
# 		f.write(',')
# 		f.write(str(k[1])) # zip3
# 		f.write(',')
# 		f.write(str(v)) # OR
# 		f.write('\n')
# f.close() # exported on 7/14/13

# 2. dict[(seasonnum, zip3)] = (ILI, popsize)
# need to import new dataset
chdatseasin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/choropleth_seasonincid_v7-1-13.csv','r')
chdatseas=csv.reader(chdatseasin, delimiter=',')




# 3. dict[(seas, wk, zip3)] = (ILI, popsize)
## see choropleth_v7-1-13.sql
## exported as choropleth_v7-1-13.csv

# edited 7/23/13
# popsize chould be grabbed from zip3_incid_season.txt because popstat does not really change over the course of a season. All zip3s with a seasonal popstat value should be included in the dictionary. There should be 843 zip3s. If there is no ILI data for a zip3 in a particular week, it should be added to the dictionary as 0 ILI counts.
popstatin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata/zip3_incid_season.txt','r')
popstatin.readline() # move cursor beyond the header
# dict[(season, zip3)] = popstat
popstat=csv.reader(popstatin, delimiter=',')
d_popstat={}
zip3s = []
def imp_popstat (filename, dict_popstat):
	for row in filename:
		seas, zip3, popstat = str(row[0]), str(row[1]), float(row[3])
		d_popstat[(seas, zip3)] = popstat
		zip3s.append(zip3)
		
imp_popstat(popstat, d_popstat)
zip3s = set(zip3s)
print len(d_popstat.items()) # 8430 items in the dictionary

popstatin.close()

# create dict[(season, zip3, week)] = ili
iliin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata/zip3_incid_week.txt','r')
iliin.readline() # move cursor beyond the header
ili=csv.reader(iliin, delimiter=',')
d_incidwk, d_wk = {},{}
wks = []
def imp_ili (filename, dict_incidwk):
	for row in filename:
		seas, zip3, week, ili = str(row[0]), str(row[2]), date(int(row[1][0:4]), int(row[1][5:7]), int(row[1][8:])), float(row[3])
		d_incidwk[(seas, zip3, week)] = ili
		d_wk[week] = seas
		wks.append(week)
imp_ili(ili, d_incidwk)
wks = set(wks)
print len(d_incidwk.items()) # 380260 items in dictionary
iliin.close()

# create new dict[(seas, zip3, week)] = ili/popstat*10000
# include each zip3 if it is in d_popstat for a season, even if it is not in d_incidwk for a week
d_AR={}
for s, z in d_popstat.keys():
	for w in wks:
		d_AR[(d_wk[w], z, w)] = 0.0 # add season-week combinations to dictionary for each zip3 even if the zip3 ILI information is missing. We assume that the incidence is 0 for that week
		if (s, z, w) in d_incidwk:
			d_AR[(s, z, w)] = float(d_incidwk[(s, z, w)])/d_popstat[(s, z)]*10000

# export dictionary 
# with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata/zip3_incid_week_cl.txt', 'a') as f:
# 	for k,v in d_AR.iteritems():
# 		print k,v
# 		f.write(str(k[0])) # season number
# 		f.write(',')
# 		f.write(str(k[1])) # zip3
# 		f.write(',')
# 		f.write(str(k[2])) # week
# 		f.write(',')
# 		f.write(str(v)) # attack rate per 10,000
# 		f.write('\n')
# f.close() # exported on 7/24/13

# export prior to 7/23/13 #
chdatwkin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/choropleth_v7-1-13.csv','r')
chdatwk=csv.reader(chdatwkin, delimiter=',')

# d_wzILIp = {}
#
# def imp_wzILIp (csvfile, dict_wzILIp):
# 	for row in csvfile:
# 		seas, wk, zip3 = str(row[0]), str(row[1]), str(row[2])
# 		ILI, popstat = int(row[3]), int(row[4])
# 		dict_wzILIp[seas, wk, zip3] = (ILI, popstat)
#
# imp_wzILIp(chdatwk, d_wzILIp)
# print d_wzILIp.items()


# 4. dict[zip3] = (lat, long) 
llin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/Coord3digits.csv','r') # note: zip3 == "TOT" is included in this dataset
ll=csv.reader(llin, delimiter=',')

d_zll = {} # dict[zip3] = (lat, long)

def imp_ll (csvfile, dict_zll):
	ct=0
	for row in csvfile:
		if ct==0:
			ct+=1
			continue
		if (row[6] and row[6] != '0'):
			if len(row[0]) == 1: # zip3 = 00#
				key = "00" + str(row[0]) 
				dict_zll[key] = (row[6], row[7])
			elif len(row[0]) == 2: # zip3 = 0##
				key = "0" + str(row[0])
				dict_zll[key] = (row[6], row[7])
			else: # zip3 = ###
				dict_zll[str(row[0])] = (row[6], row[7])

imp_ll(ll, d_zll)
# print d_zll.items():

# with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/zip3_ll.txt', 'a') as f:
# 	for k,v in d_zll.iteritems():
# 		print k,v
# 		f.write(str(k)) # zip3
# 		f.write(',')
# 		f.write(str(v[0])) # latitude
# 		f.write(',')
# 		f.write(str(v[1])) # longitude
# 		f.write('\n')
# f.close() # exported 7/14/13





















