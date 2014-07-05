#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/18/14
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
import functions as fxn

### data structures ###
### called/local plotting parameters ###

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

# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zOR_processing(incid, pop, thanks)

##############################################
# ILINet NATIONAL
# national files
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv','r')
incidin.readline() # remove header
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data/totalpop_age_Census_98-14.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

# d_ILINet_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_ILINet_classifzOR = fxn.ILINet_classif_zOR_processing(incid, pop, thanks)

##############################################
# SDI REGION: nation-level peak-basesd retrospective classification
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

# d_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR_reg = fxn.classif_zOR_region_processing(incid, pop, thanks, regincid, regpop, 'nation')

##############################################
# SDI STATE: nation-level peak-basesd retrospective classification
# import same files as regional files
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

# d_classifzOR_state[(seasonnum, state)] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR_state = fxn.classif_zOR_state_processing(incid, pop, thanks, regincid, regpop, 'nation')

##############################################
print d_classifzOR
print d_ILINet_classifzOR
print d_classifzOR_reg

fn1 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications.csv'
print_dict_to_file(d_classifzOR, fn1)
fn2 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_national_classifications.csv'
print_dict_to_file(d_ILINet_classifzOR, fn2)
fn3 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_regional_classifications.csv'
print_dict_to_file2(d_classifzOR_reg, fn3)
fn4 = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classifications.csv'
print_dict_to_file3(d_classifzOR_state, fn4)