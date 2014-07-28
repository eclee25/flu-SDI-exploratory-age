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
import numpy as np

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
## import CDC data for chr, cfr, and deaths:ili
# d_CHR[seasonnum] = cumulative lab-confirmed case-hospitalization rate per 100,000 in population over the period from week 40 to week 17 during flu season
# d_CFR[seasonnum] = P&I deaths of all flu season deaths in 122 cities/outpatient ILI cases of all flu season patient visits to outpatient offices in ILINet
# d_deaths[seasonnum] = (P&I deaths from wks 40 to 20, all cause deaths from wks to 40 to 20)
# d_ILI[seasonnum] = (ILI cases from wks 40 to 20, all patients from wks 40 to 20)
d_CHR, d_CFR, d_deaths, d_ILI = fxn.cdc_import_CFR_CHR(cdc)

## import SDI data for zOR ##
# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)
# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zOR_processing(d_wk, d_incid53ls, d_zOR53ls, thanks)

# plot values
retrozOR = [d_classifzOR[s][0] for s in ps]
CHR = [d_CHR[s] for s in ps]
CFR = [d_CFR[s] for s in ps]
dI_ratio = [d_deaths[s][0]/d_ILI[s][0] for s in ps]
print retrozOR
print CHR
print CFR
print dI_ratio
print 'retrozOR_hosprate', np.corrcoef(retrozOR, CHR)
print 'retrozOR_mortrisk', np.corrcoef(retrozOR, CFR)
print 'retrozOR_dIratio', np.corrcoef(retrozOR, dI_ratio)


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

# mean retrospective zOR vs. ratio of P&I deaths to ILI cases (two different data sources)
plt.plot(dI_ratio, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, dI_ratio, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('P&I Deaths to ILI', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_CFR_CHR/zOR_DeathILIRatio.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()









