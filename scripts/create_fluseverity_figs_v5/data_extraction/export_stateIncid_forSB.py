#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/20/14
###Function: Export state incidence data for SB



###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python export_stateIncid_forSB.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import sys

## local modules ##
sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/create_fluseverity_figs_v5')
import functions_v5 as fxn

### data structures ###
### called/local plotting parameters ###
nw = fxn.gp_normweeks # number of normalization weeks in baseline period
ps = fxn.pseasons

### functions ###


def print_incid_to_file(dict_incid, filename):
	with open(filename, 'w+') as fwriter:
		for key, ls in dict_incid.items():
			fwriter.write("%s" % key[1])
			for item in ls:
				fwriter.write(",%s" % item)
			fwriter.write("\n")

if ps == fxn.gp_plotting_seasons:

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


	##############################################
	## save state-level incidence to file ##
	for s in ps:
		d_dummy = dict((key, d_spatialTotIncid53ls[key]) for key in d_spatialTotIncid53ls if key[0] == s)
		fn = '/home/elee/Downloads/stateIncid_forSB_S%s.csv' %(s)
		print_incid_to_file(d_dummy, fn)

		d_dummy2 = dict((key, d_spatialTotIncidAdj53ls[key]) for key in d_spatialTotIncidAdj53ls if key[0] == s)
		fn2 = '/home/elee/Downloads/stateIncidAdj_forSB_S%s.csv' %(s)
		print_incid_to_file(d_dummy2, fn2)

# zipped and saved 11/20/14 in Py_Export zip file stateIncid_forSB.zip
