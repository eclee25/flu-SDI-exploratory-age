#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/27/13

### Update from v070813
## Purpose: Return values from functions

### Update from v060713
## Purpose: Change data import mechanism from lists to dictionaries

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
from datetime import date

## local packages ##
### data structures ###
### parameters ###
USchild = 20348657 + 20677194 + 22040343 # US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 # US adult popn from 2010 Census
USpop = 308745538 # US total popn from 2010 Census

### functions ###

##############################################
#### (import_d function) dict_data = store imported data, seascol = column number for season; agecol = column number for age group marker ('A', C', 'O'); ilicol = column number for ILI counts
# length of dictionary should equal number of rows in csvfile
def import_d (csvfile, seascol, agecol, ilicol):
	''' Import season-level ILI data into a dictionary where season number and agegroup are the key and ILI count is the value.
	'''

	dict_data = {}
	for row in csvfile:
		dict_data[(int(row[seascol]), str(row[agecol]))] = float(row[ilicol])
	print "Length of dict_data: %d" % len(dict_data)
	return dict_data

##############################################
#### (ORgen_seas function) dict_data = completed dictionary with (season number, age group) as key and ILI count as value; dict_OR = store ORs; timelist = list of season numbers for which ORs will be calculated
def ORgen_seas (dict_data, timelist):
	''' Generate a dictionary of season-level odds ratios for a given list of attack rates for children and adults, where the key is the season number and the value is the odds ratio.
	'''

	dict_OR = {}
	for t in timelist:
		c_attack = dict_data[(t,'C')]/USchild # calculate child attack rate
		a_attack = dict_data[(t,'A')]/USadult # calculate adult attack rate
		OR = (c_attack/(1-c_attack))/(a_attack/(1-a_attack)) # calculate odds ratio
# 		print OR
		dict_OR[t] = float(OR) # create dictionary for odds ratios
	print "Length of dict_OR: %d" % len(dict_OR)
	return dict_OR

##############################################
#### (ARdict_seas function) 
def ARdict_seas (dict_data, timelist):
	''' Generate dictionaries of season-level attack rates for the total US population, US children, and US adults. The key is the season number for both dicts. For one dict, the value is the total attack rate. For the second dict, the value is a tuple of the child and adult attack rates.
	'''

	dict_AR_ca, dict_AR_tot = {}, {}
	for t in timelist:
		# child attack rate
		c_attack = dict_data[(t,'C')]/USchild*1000 
		# adult attack rate
		a_attack = dict_data[(t,'A')]/USadult*1000 
		# total attack rate
		tot_attack = (dict_data[(t, 'C')] + dict_data[(t, 'A')] + dict_data[(t, 'O')]) / USpop * 100000 
		dict_AR_ca[t] = (c_attack, a_attack)
		dict_AR_tot[t] = tot_attack
	return dict_AR_ca, dict_AR_tot

##############################################
#### (import_dwk function) dict_data = store imported data; dict_wk = empty dictionary where week and season numbers are keys and  seascol = column number for season; wkcol = column number for week; agecol = column number for age group marker ('A', C', 'O'); ilicol = column number for ILI counts; wklist = list where unique weeks will be appended
# length of dictionary should equal number of rows in csvfile
def import_dwk (csvfile, seascol, wkcol, agecol, ilicol):
	''' Import ILI data into a dictionary where a tuple of week and age group are the keys and the values are the number of ILI cases. Create a second dictionary where week is the key and associated season number is the value. In addition, return a unique list of weeks in the file, which will be used to call the values in these two dictionaries in the main code.
	'''

	dict_data, dict_wk, wklist = {}, {}, []
	for row in csvfile:
		week = row[wkcol]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		wklist.append(wk)
		dict_data[(wk, str(row[agecol]))] = float(row[ilicol])
		dict_wk[wk] = int(row[seascol])
	print "Length of dict_data: %d" % len(dict_data)
	wklist = set(wklist)
	return dict_data, dict_wk, wklist

##############################################
#### (ORgen_wk function) dict_data = completed dictionary with (week, age group) as key and ILI count as value; dict_OR = store ORs in dict; timelist = list of season numbers for which ORs will be calculated; 
def ORgen_wk (dict_data, wklist):
	''' Generate odds ratios at the week-level. Create one dictionary where key is the week and value is the OR. Create a second dictionary where key is the week and value is the total attack rate by 10,000 for the week. 
	'''
	
	dict_OR, dict_AR = {},{}
	for w in set(wklist):
		c_attack = dict_data[(w, 'C')]/USchild # calculate child attack rate
		a_attack = dict_data[(w, 'A')]/USadult # calculate adult attack rate
		OR = (c_attack/(1-c_attack))/(a_attack/(1-a_attack)) # calculate odds ratio
		dict_OR[w] = float(OR) # create dictionary for odds ratios
		tot_AR = (dict_data[(w, 'C')] + dict_data[(w, 'A')] + dict_data[(w, 'O')]) / USpop * 10000
		dict_AR[w] = tot_AR
	print "Length of dict_OR: %d" % len(dict_OR)
	return dict_OR, dict_AR

##############################################
#### (import_gen_d function) kcol = column for keys; vcol = column for dicitonary values; dict_gen = empty dictionary where data will be stored
def import_gen_d (csvfile, kcol, vcol):
	''' Generic function for importing data into a dictionary. 
	'''
	
	dict_gen = {}
	for row in csvfile:
		dict_gen[int(row[kcol])] = str(row[vcol])
	print "Length of new dict: %d" % len(dict_gen)
	return dict_gen

##############################################
#### (import_cdc function) dict_data = empty dictionary where imported data will be stored, wkcol = column number for wknum, childcol = column number for child ILI cases, adultcol = column number for adult ILI cases, wklist = empty list where unique weeks will be appended
# length of dictionary should equal number of rows in csvfile
def import_cdc (csvfile, wkcol, childcol, adultcol):
	''' Import ILI data into a dictionary where the key is a tuple of the week number and age group and the value is the ILI count. This function was used to import CDC data, where the definitions of children and adults do not exactly match the definitions we are using.
	'''
	
	dict_data, wklist = {}, []
	for row in csvfile:
		wknum = row[wkcol]
		wklist.append(wknum)
		dict_data[(wknum, 'C')] = float(row[childcol]) # cdc data is 5-24 for children
		dict_data[(wknum, 'A')] = float(row[adultcol]) # cdc data is 25-64 for adults
	print "Length of dict_data: %d" % len(dict_data)
	return dict_data, wklist

##############################################
def import_z3_ll(fname):
	''' Import dataset with zip3, latitude, and longitude into a dictionary where the key is the zip3 and the value is a tuple of the latitude and longitude.'''
	
	dict_z3_ll = {}
	lines = fname.readlines()
	fname.close()
	for line in lines:
		fields = line.split(',')
		# dict_z3_ll[zip3] = (latitude, longitude)
		dict_z3_ll[fields[0]] = (float(fields[1]), float(fields[2]))
	return dict_z3_ll

##############################################
def import_z3_OR_season(fname):
	''' Import dataset with season, zip3, and odds ratio into a dictionary where the key is a tuple of the season and zip3 and the value is the OR.
	'''
	
	dict_z3_OR_season = {}
	lines = fname.readlines()
	fname.close()
	for line in lines:
		fields = line.split(',')
		# dict_z3_OR_season[(season, zip3)] = OR
		dict_z3_OR_season[(int(fields[0]), fields[1])] = float(fields[2])
	return dict_z3_OR_season



