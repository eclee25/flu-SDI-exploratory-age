#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 5/13/14
###Function: Export mean zOR data for each region by season
## plot choropleth by individual states, where each state in a single region has the same value

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python exctract_meanzOR_by_region.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
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

## region level peak based retrospective classification ##

## national-level data ##
# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)

## regional-level data ##
_, d_zip3_reg, d_incid_reg, d_OR_reg = fxn.week_OR_processing_region(regincid, regpop)
# dict_zOR_reg[(week, hhsreg)] = zOR
d_zOR_reg = fxn.week_zOR_processing_region(d_wk, d_OR_reg)
# dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls_reg, d_OR53ls_reg, d_zOR53ls_reg = fxn.week_plotting_dicts_region(d_wk, d_incid_reg, d_OR_reg, d_zOR_reg)
# dict_classifindex[seasonnum] = (index of first retro period week, index of first early warning period week)
d_classifindex = fxn.classif_zOR_index(d_wk, d_incid53ls, d_incid53ls_reg, 'region', thanks)
# d_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR_reg = fxn.classif_zOR_region_processing(d_classifindex, d_wk, d_zOR53ls_reg)

for key in d_classifzOR_reg:
	states = d_region_state[key[1]]
	print states
	# 6/24/14: unique values for each season-region combination, state is listed only for the choropleth plotting, which must be done at the state level
	for st in states:
		# d_classifzOR_state[(season, region, state)] = (retro_zOR, early_zOR)
		d_classifzOR_state[(key[0], key[1], st)] = d_classifzOR_reg[key]

# export data
filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/meanzOR_by_region_reglvl.csv' # renamed 6/24/14
fwriter = open(filename, 'w+')
fwriter.write('season,region,state,retro_zOR,early_zOR\n')
for k, v in d_classifzOR_state.items():
	season, region, state = str(k[0]), str(k[1]), str(k[2])
	retro, early = str(v[0]), str(v[1])
	fwriter.write('%s,%s,%s,%s,%s\n' % (season, region, state, retro, early))
fwriter.close()
	
	
	
	
	
	
	
	
	
	