#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/7/13
###Function:
## generate a script of functions that can be called from other programs with the following functions:
### imports week-level and season-level data that is normalized by the US population, 'any diagnosis' counts from the SDI data, or 'popstat' variable by zipcode from the SDI data
### generates the odds ratios in list formats that make it easy to draw charts

###Import data: R_export/zipcode_bysseas_cl.csv (cleaned from SQL_export/zipcode_bysseas.csv)

###Command Line: python 
##############################################


### notes ###
# 'USchild' and 'USadult' are taken from 2010 Census age demographics, table 2: http://www.census.gov/prod/cen2010/briefs/c2010br-03.pdf
# child = 5-19 yo, adult = 20-59 yo

### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##
### data structures ###
### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn from 2010 Census

### functions ###

#### (importer function) imports data for week-level and season-level OR charts where ILI is normalized by total child and adult US populations from 2010 Census
# must be used for week-level data (one file per season, eg. odds_c_a2_a.csv) when season does not have 52 weeks of data (has 53 weeks or not a complete season's worth of data) or season-level data (one file for all seasons, eg. odds_c_a1.csv)
# seasons where this function can be used are 2000-01 (a, not complete season), 2004-05 (e, 53 wks of data), 2009-10 (j, not complete season)
# season-level charts: importer is called once to grab all data
# week-level charts: importer must be called for each season's dataset
def importer (csvreadfile, adultlist, childlist, ilicol):
# csvreadfile is name of csv file object: season number, age group code, ... ILI counts
# adultlist is empty list to which adult attack rate will be appended
# childlist is empty list to which child attack rate will be appended
# ilicol is column number of ILI counts in import dataset

	ct=0	
	for row in csvreadfile:
		if row[1] == "A": # indicates data for adults
			adultlist.append(float(row[ilicol])/USadult) # append adult attack rate
		elif row[1] == "C": # indicates data for children
			childlist.append(float(row[ilicol])/USchild) # append child attack rate
		else: # skip data for "O" (age groups outside of adult and child age ranges)
			ct+=1


#### (avg53 function) imports data for week-level OR charts where ILI is normalized by total child and adult US populations from 2010 Census
# must be used for week-level data when season has 52 weeks of data because the two weeks around the end of the calendar year must be averaged to create a 53rd data point
# this is necessary to generate data with the same number of points for seasons with different numbers of weeks
# avg53 must be called for each season's dataset (b, c, d, f, g, h, i)
def avg53 (csvreadfile, adultlist, childlist, ilicol):
# csvreadfile is name of csv file object: season number, age group code, ... ILI counts
# adultlist is empty list to which adult attack rate will be appended
# childlist is empty list to which child attack rate will be appended
# ilicol is column number of ILI counts in import dataset
	ct=0	
	for row in csvreadfile:
		if ct == 13:
			adultlist.append(0)
			childlist.append(0)
			ct+=1
			if row[1] == "A":
				adultlist.append(float(row[ilicol])/USadult)
			elif row[1] == "C":
				childlist.append(float(row[ilicol])/USchild)
			else:
				ct+=1
		elif row[1] == "A":
			adultlist.append(float(row[ilicol])/USadult)
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/USchild)
		else:
			ct+=1
	adultlist[13] = (adultlist[12]+adultlist[14])/2
	childlist[13] = (childlist[12]+childlist[14])/2


#### (import_anydiag) imports 'any diagnosis' data needed for normalizing certain OR charts
def import_anydiag (csvreadfile, ad_dict):
# csvreadfile is name of csv file object: season number, age group code, number of any diagnosis visits (eg. anydiag.csv)
# ad_dict is empty dictionary where any diagnosis data will be stored

	for row in csvreadfile:
		ad_smarker = str(row[0])+str(row[1]) # key = season number + age group code (eg. 1A = season 1 adults)
		ad_visits = float(row[2]) # value = number of 'any diagnosis' visits made by designated age group during designated season
		ad_dict[ad_smarker] = ad_visits # assign to dictionary ad_dict


#### (importer2 function) imports data for week-level OR charts where ILI is normalized by number of "any diagnosis" counts, which are exported from the SDI mysql database
# importer2 must be called for each season's data file
def importer2 (csvreadfile, adultlist, childlist, ilicol, seasonnum, ad_dict):
# csvreadfile is name of csv file object: season number, age group code, ... ILI counts
# adultlist is empty list to which adult attack rate will be appended
# childlist is empty list to which child attack rate will be appended
# ilicol is column number of ILI counts in import dataset
# seasonnum is season number code indicated in SDI mysql database (eg. 1 = 2000-01 flu season, 2 = 2001-02 flu season, etc.)
# ad_dict is dictionary created from import_anydiag function

	for row in csvreadfile:
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/float(ad_dict[str(seasonnum)+"A"]))
			#print float(row[ilicol]), float(ad_dict[str(seasonnum)+"A"])
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/float(ad_dict[str(seasonnum)+"C"]))
			#print float(row[ilicol]), float(ad_dict[str(seasonnum)+"C"])


#### (importer3 function) imports data for season-level OR charts where ILI is normalized by number of "any diagnosis" counts
# importer3 is called once to grab data for each season
def importer3 (csvreadfile, adultlist, childlist, ilicol, ad_dict):
# csvreadfile is name of csv file object: season number, age group code, ... ILI counts
# adultlist is empty list to which adult attack rate will be appended
# childlist is empty list to which child attack rate will be appended
# ilicol is column number of ILI counts in import dataset
# seasonnum is season number code indicated in SDI mysql database (eg. 1 = 2000-01 flu season, 2 = 2001-02 flu season, etc.)
# ad_dict is dictionary created from import_anydiag function

	for row in csvreadfile:
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/float(ad_dict[str(row[0])+"A"]))
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/float(ad_dict[str(row[0])+"C"]))


#### (ORgen function) generate odds ratios at the season-level or week-level for a given list of attack rates for children and adults
def ORgen (ylist, childlist, adultlist):
# ylist is empty list to which the newly generated odds ratios will be generated
# adultlist is list of adult attack rates generated from one of the import functions (importer, importer2, importer3, or avg53)
# childlist is list of child attack rates generated from one of the import functions (importer, importer2, importer3, or avg53)

	ct=0
	for i in range(0,len(childlist)):
		if adultlist[i] == 0.0 or childlist[i] ==0.0:
			print "values for childlist, adultlist when adultlist[i] or childlist[i]==0:"
			print childlist[i], adultlist[i]
			print "adultlist==0 or childlist==0 index:",ct
			ct+=1
		else:
			ylist.append((childlist[i]/(1-childlist[i]))/(adultlist[i]/(1-adultlist[i])))
			ct+=1
	#print childlist[i], 1-childlist[i], adultlist[i], 1-adultlist[i] # this is a check


#### (importer_zip3 function) imports data for season-level OR urban-rural charts, where each point is a zipcode-season
def importer_zip3 (csvreadfile, adultlist, childlist,  ilicol, popstatcol, zippref, zipcol, snum, dictname, ru_code):
# csvreadfile is name of csv file object: season number, age group code, ... ILI counts
# adultlist is empty list to which adult attack rate will be appended
# childlist is empty list to which child attack rate will be appended
# ilicol is column number of ILI counts in import dataset
# popstatcol is column number of popstat data in import dataset (estimated population of age group in that zipcode prefix); this data may be incomplete if certain age groups are missing in a dataset for a whole season; it is unknown why data for age groups may be missing. it is possible that that individuals of that age group do not live in the zipcode prefix, but that seems unlikely. unless this unlikely case is true, the denominator will be an under-estimate of the population, meaning that the attack rates are over-estimations. ; for data that is complete for all age groups, use data dated on or after 6-12-13
# zippref is empty list to which zipcode prefixes (zip3s) are appended
# zipcol is column number of zipcode prefix
# snum is empty list to which season number code in import dataset will be appended
# dictname is dictionary that has zip3s as keys and their RUCC_mn bin as value
# ru_code is empty list to which rural-urban code average bin will be appended; this parameter will help create x-axis for OR vs urban rural plot 
	ct=0
	for row in csvreadfile:
		if ct==0: # skip header (variable names)
			ct+=1
			continue
		snum.append(int(row[0]))
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/float(row[popstatcol]))
			zippref.append(str(row[zipcol]))
			val=str(row[zipcol])
			ru_code.append(dictname[val])
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/float(row[popstatcol]))
		else:
			ct+=1
	print "number of skipped rows:", ct # should be number of "O" (other age group code) values in the dataset plus 1 for header row, plus number of rows where ILI = 0, which may easily be checked in R (if O data is included in the original dataset)


#### (importer_ORzip3 function) imports data for season-level OR charts where ILI is divided by popstat for each zip3 and then averaged across all zip3s; one point per season and each point is the average of all zip3s
# this extra level of normalization (instead of simply using US pop normalization) will allow the generation of error bars for the OR value
def importer_ORzip3 (csvreadfile, adultlist, childlist,  ilicol, popstatcol, zippref, zipcol, snum):
# csvreadfile is name of csv file object: season number, age group code, ... ILI counts
# adultlist is empty list to which adult attack rate will be appended
# childlist is empty list to which child attack rate will be appended
# ilicol is column number of ILI counts in import dataset
# popstatcol is column number of popstat data in import dataset (estimated population of age group in that zipcode prefix); this data may be incomplete if certain age groups are missing in a dataset for a whole season; it is unknown why data for age groups may be missing. it is possible that that individuals of that age group do not live in the zipcode prefix, but that seems unlikely. unless this unlikely case is true, the denominator will be an under-estimate of the population, meaning that the attack rates are over-estimations.; for data that is complete for all age groups, use data dated on or after 6-12-13
# zippref is empty list to which zipcode prefixes (zip3s) are appended
# zipcol is column number of zipcode prefix
# snum is empty list to which season number code in import dataset will be appended; only count for adultlist values because there are two rows for each OR that will be generated

	ct=0
	for row in csvreadfile:
		if ct==0: # skip header (variable names)
			ct+=1
			continue
		if row[1] == "A":
			adultlist.append(float(row[ilicol])/float(row[popstatcol]))
			zippref.append(str(row[zipcol]))
			snum.append(int(row[0]))
		elif row[1] == "C":
			childlist.append(float(row[ilicol])/float(row[popstatcol]))
		else:
			ct+=1
	print "number of skipped rows:", ct # should be number of "O" (other age group code) values in the dataset plus 1 for header row, plus number of rows where ILI = 0, which may easily be checked in R (if O data is included in the original dataset)
	

#### generates season-level ORs -- ORs are calculated for each zipcode prefix (zip3) and then averaged across the zipcodes for each season 
# sd for the OR of each season will also be gathered
def ORgen_zip3mn (ylist, childlist, adultlist, snum, avgORlist, sdORlist):
# ylist is empty list to which the newly generated odds ratios will be generated
# adultlist is list of adult attack rates generated from importer_zip3 function
# childlist is list of child attack rates generated from importer_zip3 function
# snum is list of season number codes that corresponds to childlist and adultlist values, used to indicate which data belong to which season
# avgORlist is empty list to which average ORs across zip3s for each season should be 
	
	for r in range(0, len(childlist)):
		ct=0
		if adultlist[r] == 0: # ct tells you how many values of adultlist are equal to 0 (which would give a "0" attack rate) # these should have been removed in the data cleaning but this is a check
			ct+=1
		else:
			ylist.append((childlist[r]/(1-childlist[r]))/(adultlist[r]/(1-adultlist[r]))) # generate OR for each zip3 and season
	print "Count of adultlist = 0:", ct
	print "Length of ylist:", len(ylist)
	print "Length of snum:", len(snum)
	for i in range(1, len(set(snum))+1): # len(set(snum)) = number of seasons of data imported
		index = [a for a,b in enumerate(snum) if b == i] # indices for season number as defined by range function in for loop
		print "length of index:", len(index)
		ysubset = [ylist[val] for val in index]
		print "length of ylist subset:", len(ysubset)
		avgOR = np.mean(ysubset) # mean OR for season i+1
		print "avg OR for season", i, avgOR
		sdOR = np.std(ysubset) # sd of OR for season i+1
		avgORlist.append(avgOR)
		sdORlist.append(sdOR)
	print "Length of OR avgs:", len(avgORlist) # length should be equal to len(set(snum)) minus number of values dropped bc division by zero
	print "Len(OR avgs) should equal:", len(set(snum))-ct
	print "avgORlist:", avgORlist
	print "sdORlist:", sdORlist 

















