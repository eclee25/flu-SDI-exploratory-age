#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 5/13/14
###Function: Export mean zOR data for each region by season

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python choropleth_region.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###
d_classifzOR_state = {}
### functions ###
### data files ###
# regional files
reg_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
reg_incidin.readline()
regincid = csv.reader(reg_incidin, delimiter=',')
reg_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
reg_popin.readline()
regpop = csv.reader(reg_popin, delimiter=',')
# national files
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

### program ###
# d_region_state[region] = [state1 in region, state2 in region, ..]
d_region_state = fxn.region_state_dictionary()

# nation-level peak-based retrospective classification
# import data
# d_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR_reg = fxn.classif_zOR_region_processing(incid, pop, thanks, regincid, regpop, 'nation')

for key in d_classifzOR_reg:
	states = d_region_state[key[1]]
	print states
	for st in states:
		# d_classifzOR_state[(season, region, state)] = (retro_zOR, early_zOR)
		d_classifzOR_state[(key[0], key[1], st)] = d_classifzOR_reg[key]

# export data
filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/meanzOR_by_state.csv'
fwriter = open(filename, 'w+')
fwriter.write('season,region,state,retro_zOR,early_zOR\n')
for k, v in d_classifzOR_state.items():
	season, region, state = str(k[0]), str(k[1]), str(k[2])
	retro, early = str(v[0]), str(v[1])
	fwriter.write('%s,%s,%s,%s,%s\n' % (season, region, state, retro, early))
fwriter.close()
	
	
	
	
	
	
	
	
	
	