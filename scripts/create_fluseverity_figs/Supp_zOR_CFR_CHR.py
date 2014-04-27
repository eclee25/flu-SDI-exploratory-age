#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/27/14
###Function: plot zOR vs. CFR & proxies (supp figure)

### lab-confirmed hospitalization rates per 100,000 in US population (CDC data)
### proportion of P&I deaths of all-cause mortality vs. ILI cases of all visits (CDC data)
### proportion of P&I deaths of all-cause mortality vs. lab-confirmed hospitalization rates per 100,000 in US population (CDC data)
### Acute ILI vs non-acute ILI visits (SDI data)

###Import data: 
#### CDC_Source/Import_Data/all_cdc_source_data.csv: "uqid", "yr", "wk", "num_samples", "perc_pos", "a_H1", "a_unsub" , "a_H3", "a_2009H1N1", "a_nosub", "b", "a_H3N2", "season", "allcoz_all", "allcoz_65.", "allcoz_45.64", "allcoz_25.44", "allcoz_1.24",  "allcoz_.1", "pi_only", "ped_deaths", "hosp_0.4", "hosp_18.49", "hosp_50.64", "hosp_5.17", "hosp_65.", "hosp_tot", "ilitot",   "patients", "providers", "perc_wt_ili", "perc_unwt_ili", "ili_0.4", "ili_5.24", "ili_25.64", "ili_25.49", "ili_50.64", "ili_65."  
#### SQL_export/F1.csv (outpatient data only): 'season', 'wk', 'yr', 'wknum', 'outpatient & office ILI', 'outpatient & office anydiag', 'pop'
#### SQL_export/Supp_acuteILI_wk.csv (inpatient/ER data only): 'season', 'wk', 'yr', 'wknum', 'inpatient & ER ILI', 'inpatient & ER anydiag', 'pop'

###Command Line: python Supp_zOR_CFR_CHR.py
##############################################


### notes ###
# calculated fatality and hospitalization rates are proxy rates because the denominator is ILI and US population, respectively, rather than lab-confirmed flu cases

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions as fxn

### data structures ###
### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### data files ###
# calculate zOR by season (outpatient incidence by age group from SDI data)
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')
# calculate total CFR and CHR from CDC data using deaths, ILI, lab-confirmed hospitalization rate per 100,000
cdcin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv', 'r')
cdcin.readline() # remove header
cdc=csv.reader(cdcin, delimiter=',')
# calculate acute to non-acute ILI cases from total SDI data
outpatientSDIin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/F1.csv','r')
outpatientSDI=csv.reader(outpatientSDIin, delimiter=',')
inpatientSDIin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/Supp_acuteILI_wk.csv','r')
inpatientSDI=csv.reader(inpatientSDIin, delimiter=',')

### program ###
# import data
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
# d_CHR[seasonnum] = cumulative lab-confirmed case-hospitalization rate per 100,000 in population over the period from week 40 to week 17 during flu season
d_classifzOR = fxn.classif_zOR_processing(incid, pop, thanks)
d_CHR, d_CFR = fxn.cdc_import_CFR_CHR(cdc)

# plot values
retrozOR = [d_classifzOR[s][0] for s in ps]
CHR = [d_CHR[s] for s in ps]
CFR = [d_CFR[s] for s in ps]
print retrozOR
print CHR

# draw plots
# mean retrospective zOR vs. cumulative lab-confirmed hospitalization rate per 100,000 in population
plt.plot(CHR, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, CHR, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('Hospitalization Rate per 100,000', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0, 35])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_CFR_CHR/zOR_HospPerPop.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean retrospective zOR vs. proportion of P&I deaths of all-cause mortality divided by proportion of ILI cases from all visits
plt.plot(CFR, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, CFR, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('P&I Mortality Risk:ILI Case Proportion', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_CFR_CHR/zOR_ILIMortalityRisk.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()











