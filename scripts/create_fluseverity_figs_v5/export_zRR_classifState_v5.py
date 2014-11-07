#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/1/14
###Function: Export zOR retrospective and early warning classifications into csv file format (SDI state and regional)
### Use nation-level peak-based retrospective classification for SDI region analysis

# 10/31 coverage adjustment no longer age-specific at national or state level
# 11/1 split from export_zOR_classif.py

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python export_zRR_classifState_v5.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv

## local modules ##
import functions_v5 as fxn

### data structures ###
### called/local plotting parameters ###
nw = fxn.gp_normweeks # number of normalization weeks in baseline period

### functions ###

def print_dict_to_file2(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write("season,region,mn_retro,mn_early\n")
		for key, value in dic.items():
			fwriter.write("%s,%s,%s,%s\n" % (key[0], key[1], value[0], value[1]))

def print_dict_to_file3(dic, dic_validSeasons, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write('season,state,mn_retro,mn_early,valid_normweeks\n')
		for key, value in dic.items():
			valid = dic_validSeasons[key]
			fwriter.write("%s,%s,%s,%s,%s\n" % (key[0], key[1], value[0], value[1], valid))

if fxn.pseasons == fxn.gp_plotting_seasons:

	##############################################
	# SDI STATE: state-level peak-based retrospective classification
	# import zip3 level files
	reg_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
	reg_incidin.readline()
	regincid = csv.reader(reg_incidin, delimiter=',')
	reg_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
	reg_popin.readline()
	regpop = csv.reader(reg_popin, delimiter=',')

	# import data
	d_wk, d_weekZip3_ili, d_seasZip3_pop, d_zip3_region = fxn.week_import_zip3(regincid, regpop)
	# process ILI data
	d_seasSpatialAge_iliLS, d_seasSpatial_pop = fxn.week_ILI_processing_spatial(d_wk, d_weekZip3_ili, d_seasZip3_pop, d_zip3_region, 'state')
	# adjustments, 53rd week, RR, zRR
	d_spatialTotIncid53ls, d_spatialTotIncidAdj53ls, d_spatialRR53ls, d_spatialZRR53ls, d_validDataCount = fxn.week_RR_processing_spatial(d_wk, d_seasSpatialAge_iliLS, d_seasSpatial_pop, d_zip3_region, 'state')
	# spatial keys == states
	states = list(set([d_zip3_region[k][0] for k in d_zip3_region]))
	# create dict with state-level classifications
	d_classifzRR_spatial = fxn.classif_zRR_processing_spatial(d_wk, d_spatialTotIncidAdj53ls, d_spatialZRR53ls, states)

	##############################################
	## save classifications to file ##
	fn4 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_%sst.csv' %(nw)
	print_dict_to_file3(d_classifzRR_spatial, d_validDataCount, fn4)
