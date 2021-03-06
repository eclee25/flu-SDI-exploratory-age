#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/22/14
###Function: Export zOR retrospective and early warning classifications into csv file format (SDI and ILINet, national and regional for SDI)
### Use nation-level peak-based retrospective classification for SDI region analysis

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python export_zOR_classif.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv

## local modules ##
import functions_v4 as fxn

### data structures ###
### called/local plotting parameters ###
nw = fxn.gp_normweeks # number of normalization weeks in baseline period

### functions ###
def print_dict_to_file(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write("season,mn_retro,mn_early\n")
		for key, value in dic.items():
			fwriter.write("%s,%s,%s\n" % (key, value[0], value[1]))

def print_dict_to_file2(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write("season,region,mn_retro,mn_early\n")
		for key, value in dic.items():
			fwriter.write("%s,%s,%s,%s\n" % (key[0], key[1], value[0], value[1]))

def print_dict_to_file3(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write('season,state,mn_retro,mn_early\n')
		for key, value in dic.items():
			fwriter.write("%s,%s,%s,%s\n" % (key[0], key[1], value[0], value[1]))

if fxn.pseasons == fxn.gp_plotting_seasons:
	##############################################
	# SDI NATIONAL
	# national files
	incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
	incid = csv.reader(incidin, delimiter=',')
	popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
	pop = csv.reader(popin, delimiter=',')
	thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
	thanksin.readline() # remove header
	thanks=csv.reader(thanksin, delimiter=',')

	d_wk, d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_OR_processing(incid, pop)
	# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
	d_classifzOR = fxn.classif_zOR_processing(d_wk, d_totIncidAdj53ls, d_zRR53ls, thanks)

	##############################################
	# SDI REGION: region-level peak-based retrospective classification
	# import zip3-level files
	reg_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
	reg_incidin.readline()
	regincid = csv.reader(reg_incidin, delimiter=',')
	reg_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
	reg_popin.readline()
	regpop = csv.reader(reg_popin, delimiter=',')
	# import Thanksgiving data
	thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
	thanksin.readline() # remove header
	thanks=csv.reader(thanksin, delimiter=',')

	# import data
	d_wk, d_weekZip3_ili, d_seasZip3_pop, d_zip3_region = fxn.week_import_zip3(regincid, regpop)
	# process ILI data
	d_seasSpatialAge_iliLS, d_seasSpatial_pop = fxn.week_ILI_processing_spatial(d_wk, d_weekZip3_ili, d_seasZip3_pop, d_zip3_region, 'region')
	# adjustments, 53rd week, RR, zRR
	d_spatialTotIncid53ls, d_spatialTotIncidAdj53ls, d_spatialRR53ls, d_spatialZRR53ls = fxn.week_RR_processing_spatial(d_wk, d_seasSpatialAge_iliLS, dict_seasSpatial_pop, dict_zip3_region, 'region')

	# spatial keys == regions
	regions = list(set([dict_zip3_region[k][1] for k in dict_zip3_region]))
	# create dict with state-level classifications
	d_classifzRR_spatial = fxn.classif_zRR_processing_spatial(d_wk, d_spatialTotIncidAdj53ls, d_spatialZRR53ls, thanks, regions)

	##############################################
	# SDI STATE: state-level peak-based retrospective classification
	# import zip3 level files
	reg_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
	reg_incidin.readline()
	regincid = csv.reader(reg_incidin, delimiter=',')
	reg_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
	reg_popin.readline()
	regpop = csv.reader(reg_popin, delimiter=',')
	# import Thanksgiving data
	thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
	thanksin.readline() # remove header
	thanks=csv.reader(thanksin, delimiter=',')

	# import data
	d_wk, d_weekZip3_ili, d_seasZip3_pop, d_zip3_region = fxn.week_import_zip3(regincid, regpop)
	# process ILI data
	d_seasSpatialAge_iliLS, d_seasSpatial_pop = fxn.week_ILI_processing_spatial(d_wk, d_weekZip3_ili, d_seasZip3_pop, d_zip3_region, 'state')
	# adjustments, 53rd week, RR, zRR
	d_spatialTotIncid53ls, d_spatialTotIncidAdj53ls, d_spatialRR53ls, d_spatialZRR53ls = fxn.week_RR_processing_spatial(d_wk, d_seasSpatialAge_iliLS, dict_seasSpatial_pop, dict_zip3_region, 'state')
	# spatial keys == states
	states = list(set([dict_zip3_region[k][0] for k in dict_zip3_region]))
	# create dict with state-level classifications
	d_classifzRR_spatial = fxn.classif_zRR_processing_spatial(d_wk, d_spatialTotIncidAdj53ls, d_spatialZRR53ls, thanks, states)

	##############################################
	## save classifications to file ##
	fn1 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_%s.csv' %(nw)
	print_dict_to_file(d_classifzOR, fn1)
	fn3 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_reg_classif_covCareAdj_%sreg.csv' %(nw)
	print_dict_to_file2(d_classifzOR_reg, fn3)
	fn4 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_%sst.csv' %(nw)
	print_dict_to_file3(d_classifzOR_state, fn4)

# elif fxn.pseasons == fxn.gp_ILINet_plotting_seasons
	# ##############################################
	# # ILINet NATIONAL
	# # national files
	# incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv','r')
	# incidin.readline() # remove header
	# incid = csv.reader(incidin, delimiter=',')
	# popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data/totalpop_age_Census_98-14.csv', 'r')
	# pop = csv.reader(popin, delimiter=',')
	# thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
	# thanksin.readline() # remove header
	# thanks=csv.reader(thanksin, delimiter=',')

	# # dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
	# d_wk, d_incid, d_OR = fxn.ILINet_week_OR_processing(incid, pop)
	# d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
	# # d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	# d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)
	# # d_ILINet_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
	# d_ILINet_classifzOR = fxn.classif_zOR_processing(d_wk, d_incid53ls, d_zOR53ls, thanks)

	# fn2 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_nat_classif_careAdj_%s.csv' %(nw)
	# print_dict_to_file(d_ILINet_classifzOR, fn2)