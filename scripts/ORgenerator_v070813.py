#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/8/13

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
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from datetime import date

## local packages ##
### data structures ###
### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn from 2010 Census

### functions ###

#### (import_d function) import ILI data into a dictionary where season number and agegroup are the key and ILI count is the value
# dict_data = empty dictionary where imported data will be stored, seascol = column number for season; agecol = column number for age group marker ('A', C', 'O'); ilicol = column number for ILI counts
# length of dictionary should equal number of rows in csvfile
def import_d (csvfile, dict_data, seascol, agecol, ilicol):
	for row in csvfile:
		dict_data[(int(row[seascol]), str(row[agecol]))] = float(row[ilicol])
	print "Length of dict_data: %d" % len(dict_data)

#### (ORgen_seas function) generate odds ratios at the season-level for a given list of attack rates for children and adults
# dict_data = completed dictionary with (season number, age group) as key and ILI count as value; dict_OR = empty dictionary where ORs will be stored; timelist = list of season numbers for which ORs will be calculated
def ORgen_seas (dict_data, dict_OR, timelist):
	for t in timelist:
		c_attack = dict_data[(t,'C')]/USchild # calculate child attack rate
		a_attack = dict_data[(t,'A')]/USadult # calculate adult attack rate
		OR = (c_attack/(1-c_attack))/(a_attack/(1-a_attack)) # calculate odds ratio
# 		print OR
		dict_OR[t] = float(OR) # create dictionary for odds ratios
	print "Length of dict_OR: %d" % len(dict_OR)

#### (import_dwk function) import ILI data into a dictionary where season number and agegroup are the key and ILI count is the value
# dict_data = empty dictionary where imported data will be stored, seascol = column number for season; agecol = column number for age group marker ('A', C', 'O'); ilicol = column number for ILI counts; wklist = empty list where unique weeks will be appended
# length of dictionary should equal number of rows in csvfile
def import_dwk (csvfile, dict_data, dict_wk, seascol, wkcol, agecol, ilicol, wklist):
	for row in csvfile:
		week = row[wkcol]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		wklist.append(wk)
		dict_data[(wk, str(row[agecol]))] = float(row[ilicol])
		dict_wk[wk] = int(row[seascol])
	print "Length of dict_data: %d" % len(dict_data)
	wklist = set(wklist)


#### (ORgen_wk function) generate odds ratios at the season-level for a given list of attack rates for children and adults
# dict_data = completed dictionary with (season number, age group) as key and ILI count as value; dict_OR = empty dictionary where ORs will be stored; timelist = list of season numbers for which ORs will be calculated; 
def ORgen_wk (dict_data, dict_OR, wklist):
	for w in set(wklist):
		c_attack = dict_data[(w, 'C')]/USchild # calculate child attack rate
		a_attack = dict_data[(w, 'A')]/USadult # calculate adult attack rate
		OR = (c_attack/(1-c_attack))/(a_attack/(1-a_attack)) # calculate odds ratio
		dict_OR[w] = float(OR) # create dictionary for odds ratios
	print "Length of dict_OR: %d" % len(dict_OR)



#### (import_gen_d function) generically import data into a dictionary
# kcol = column for keys; vcol = column for dicitonary values; dict_gen = empty dictionary where data will be stored
def import_gen_d (csvfile, dict_gen, kcol, vcol):
	for row in csvfile:
		dict_gen[int(row[kcol])] = str(row[vcol])
	print "Length of new dict: %d" % len(dict_gen)


