#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14
###Function: Compare ratio of visits in S9 to visits in S# for total population, children, and adults. Check that ratio remains the same across all age groups (so that total population adjustment can be used in lieu of age-specific adjustment.)

###Import data: SQL_export/anydiag_allweeks_outpatient.csv, anydiag_allweeks_outpatient_age.csv

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
from datetime import date, datetime


## local modules ##

### data structures ###


### parameters ###

### functions ###

### import data ###
totalin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient.csv','r')
totalin.readline() # rm header
total=csv.reader(totalin, delimiter=',')
agein=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient_age.csv','r')
agein.readline() # rm header
age=csv.reader(agein, delimiter=',')

### program ###

dict_total_wk = {}
dict_wk = {}
for row in total:
	season = int(row[0])
	week = row[1]
	wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
	total = float(row[2])
	dict_wk[wk] = season
	dict_total_wk[wk] = total

dict_age_wk = {}
for row in age:
	week = row[1]
	wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
	age = str(row[2])
	visits = float(row[3])
	dict_age_wk[(wk, age)] = visits

dict_season = {}
for s in range(2,10):
	dummyweeks = [wk for wk in dict_wk if dict_wk[wk]==s]
	Tvisits_season = sum([dict_total_wk[wk] for wk in dummyweeks])
	Svisits_season = sum([dict_age_wk[(wk, age)] for wk in dummyweeks for age in ['C', 'A', 'O']])
	Cvisits_season = sum([dict_age_wk[(wk, 'C')] for wk in dummyweeks])
	Avisits_season = sum([dict_age_wk[(wk, 'A')] for wk in dummyweeks])
	dict_season[(s, 'T')] = Tvisits_season
	dict_season[(s, 'S')] = Svisits_season
	dict_season[(s, 'C')] = Cvisits_season
	dict_season[(s, 'A')] = Avisits_season

plottingT = [dict_season[(9, 'T')]/dict_season[(s, 'T')] for s in range(2,10)]
plottingS = [dict_season[(9, 'S')]/dict_season[(s, 'S')] for s in range(2, 10)]
plottingC = [dict_season[(9, 'C')]/dict_season[(s, 'C')] for s in range(2,10)]
plottingA = [dict_season[(9, 'A')]/dict_season[(s, 'A')] for s in range(2,10)]

plt.plot(range(2,10), plottingT, label='total', color='black', marker='o', linewidth=2)
plt.plot(range(2,10), plottingS, label='summed total', color='green', marker='o', linewidth=2)
plt.plot(range(2,10), plottingC, label='children', color='red', marker='o', linewidth=2)
plt.plot(range(2,10), plottingA, label='adults', color='blue', marker='o', linewidth=2)
plt.xlabel('Season')
plt.ylabel('Ratio of visits S9/S#')
plt.legend(loc='upper left')
plt.show()




