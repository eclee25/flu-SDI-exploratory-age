#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/6/14
###Function: Export zOR retrospective and early warning classifications into csv file format (SDI and ILINet national). Use alternative baselines (7 weeks in summer, 10 weeks in summer, 10 weeks in fall)
# Change to summer baseline option in week_OR_processing when running this code!

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python export_zRR_classifNat_altbaseline_v5.py
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
def print_dict_to_file(dic, filename):
	with open(filename, 'w+') as fwriter:
		fwriter.write("season,mn_retro,mn_early\n")
		for key, value in dic.items():
			fwriter.write("%s,%s,%s\n" % (key, value[0], value[1]))

if fxn.pseasons == fxn.gp_plotting_seasons:
	##############################################
	# SDI NATIONAL
	# national files
	incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
	incid = csv.reader(incidin, delimiter=',')
	popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
	pop = csv.reader(popin, delimiter=',')

	d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
	d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2_altbaseline(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
	# d_classifzRR[seasonnum] = (mean retrospective zRR, mean early warning zRR)
	d_classifzRR = fxn.classif_zRR_processing(d_wk, d_totIncidAdj53ls, d_zRR53ls)

	##############################################
	## save classifications to file ##
	fn1 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_summer%s.csv' %(nw)
	print_dict_to_file(d_classifzRR, fn1)

elif fxn.pseasons == fxn.gp_ILINet_plotting_seasons:
	##############################################
	# ILINet NATIONAL
	# national files
	incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv','r')
	incidin.readline() # remove header
	incid = csv.reader(incidin, delimiter=',')
	popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data/totalpop_age_Census_98-14.csv', 'r')
	pop = csv.reader(popin, delimiter=',')

	d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.ILINet_week_RR_processing(incid, pop)
	d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
	# d_classifzRR[seasonnum] = (mean retrospective zRR, mean early warning zRR)
	d_classifzRR = fxn.classif_zRR_processing(d_wk, d_totIncidAdj53ls, d_zRR53ls)

	fn2 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_nat_classif_covCareAdj_summer%s.csv' %(nw)
	print_dict_to_file(d_classifzRR, fn2)