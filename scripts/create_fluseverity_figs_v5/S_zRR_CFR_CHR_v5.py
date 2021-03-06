#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: plot zOR vs. CFR & proxies (supp figure)

### lab-confirmed hospitalization rates per 100,000 in US population (CDC data)
### proportion of P&I deaths of all-cause mortality vs. ILI cases of all visits (CDC data)
### proportion of P&I deaths of all-cause mortality vs. lab-confirmed hospitalization rates per 100,000 in US population (CDC data)
### Acute ILI vs non-acute ILI visits (SDI data)
### Acute ILI (inpatient) attack rate

# 11/4 v5 adjustments
# 7/20/15: updated notation
# 10/8/15: rm vert lines, color points, p-values

###Import data: 
#### CDC_Source/Import_Data/all_cdc_source_data.csv: "uqid", "yr", "wk", "num_samples", "perc_pos", "a_H1", "a_unsub" , "a_H3", "a_2009H1N1", "a_nosub", "b", "a_H3N2", "season", "allcoz_all", "allcoz_65.", "allcoz_45.64", "allcoz_25.44", "allcoz_1.24",  "allcoz_.1", "pi_only", "ped_deaths", "hosp_0.4", "hosp_18.49", "hosp_50.64", "hosp_5.17", "hosp_65.", "hosp_tot", "ilitot",   "patients", "providers", "perc_wt_ili", "perc_unwt_ili", "ili_0.4", "ili_5.24", "ili_25.64", "ili_25.49", "ili_50.64", "ili_65."  
#### SQL_export/F1.csv (outpatient data only): 'season', 'wk', 'yr', 'wknum', 'outpatient & office ILI', 'outpatient & office anydiag', 'pop'
#### SQL_export/Supp_acuteILI_wk.csv (inpatient/ER data only): 'season', 'wk', 'yr', 'wknum', 'inpatient & ER ILI', 'inpatient & ER anydiag', 'pop'

###Command Line: python S_zRR_CFR_CHR_v5.py
##############################################


### notes ###
# calculated fatality and hospitalization rates are proxy rates because the denominator is ILI and US population, respectively, rather than lab-confirmed flu cases

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

## local modules ##
import functions_v5 as fxn

### data structures ###
### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### data files ###
sevin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv','r')
sevin.readline() # remove header
sev = csv.reader(sevin, delimiter=',')
# calculate total CFR and CHR from CDC data using deaths, ILI, lab-confirmed hospitalization rate per 100,000
cdcin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv', 'r')
cdcin.readline() # remove header
cdc=csv.reader(cdcin, delimiter=',')
# calculate acute to non-acute ILI cases from total SDI data
outpatientSDIin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/F1.csv','r')
outpatientSDI=csv.reader(outpatientSDIin, delimiter=',')
inpatientSDIin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/Supp_acuteILI_wk.csv','r')
inpatientSDI=csv.reader(inpatientSDIin, delimiter=',')
# calculate acute ILI (inpatient) attack rate
inpatientin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/Supp_acuteILI_wk.csv','r')
inpatient=csv.reader(inpatientin, delimiter=',')

### program ###
## import CDC data for chr, cfr, and deaths:ili
# d_CHR[seasonnum] = cumulative lab-confirmed case-hospitalization rate per 100,000 in population over the period from week 40 to week 17 during flu season
# d_CFR[seasonnum] = P&I deaths of all flu season deaths in 122 cities/outpatient ILI cases of all flu season patient visits to outpatient offices in ILINet
# d_deaths[seasonnum] = (P&I deaths from wks 40 to 20, all cause deaths from wks to 40 to 20)
# d_ILI[seasonnum] = (ILI cases from wks 40 to 20, all patients from wks 40 to 20)
d_CHR, d_CFR, d_deaths, d_ILI = fxn.cdc_import_CFR_CHR(cdc)

## import ILI proportion of outpatient and inpatient cases
# d_ILI_anydiag_outp/inp[seasonnum] = ILI outp or inp cases/ outp or inp any diagnosis cases
d_ILI_anydiag_outp = fxn.proportion_ILI_anydiag(outpatientSDI)
d_ILI_anydiag_inp = fxn.proportion_ILI_anydiag(inpatientSDI)

## import season level attack rate for inpatient ILI cases
# d_inpatientAR[seasonnum] = ILI AR in inpatient facilities per 100,000 population
d_inpatientAR = fxn.ILI_AR(inpatient)

# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.readNationalClassifFile(sev)

# plot values
retrozOR = [d_classifzOR[s][0] for s in ps]
CHR = [d_CHR[s] for s in ps] # missing data for s2 & 3
CFR = [d_CFR[s] for s in ps] # missing data for s2
dI_ratio = [d_deaths[s][0]/d_ILI[s][0] for s in ps] # missing data for s2
inp_outp = [d_ILI_anydiag_inp[s]/d_ILI_anydiag_outp[s] for s in ps]
inpAR = [d_inpatientAR[s] for s in ps]
vals = zip(retrozOR, CHR, CFR, dI_ratio, inp_outp, inpAR)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# draw plots
# mean retrospective zOR vs. cumulative lab-confirmed hospitalization rate per 100,000 in population
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
for key in d_plotCol:
	ax1.plot([d_plotData[k][1] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, CHR, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax1.set_xlabel('Hospitalization Rate per 100,000', fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([0, 35])
ax1.set_ylim([-15, 18])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_HospPerPop.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean retrospective zOR vs. proportion of P&I deaths of all-cause mortality divided by proportion of ILI cases from all visits
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
for key in d_plotCol:
	ax2.plot([d_plotData[k][2] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, CFR, retrozOR):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax2.set_xlabel('P&I Mortality Risk:ILI Case Proportion', fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_ylim([-15, 18])
ax2.set_xlim([0.057, 0.063])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_ILIMortalityRisk.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean retrospective zOR vs. ratio of P&I deaths to ILI cases (two different data sources)
fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
for key in d_plotCol:
	ax3.plot([d_plotData[k][3] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, dI_ratio, retrozOR):
	ax3.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax3.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax3.set_xlabel('P&I Deaths to ILI', fontsize=fs)
ax3.tick_params(axis='both', labelsize=fssml)
ax3.set_ylim([-15, 18])
ax3.set_xlim([0, 1.5])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_DeathILIRatio.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean retrospective zOR vs. inpatient ILI attack rate per 100,000 population
fig5 = plt.figure()
ax5 = fig5.add_subplot(1,1,1)
for key in d_plotCol:
	ax5.plot([d_plotData[k][5] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, inpAR, retrozOR):
	ax5.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax5.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax5.set_xlabel('Inpatient ILI Visits per 100,000', fontsize=fs)
ax5.tick_params(axis='both', labelsize=fssml)
ax5.set_xlim([0,140])
ax5.set_ylim([-15, 18])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_InpatientAR.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# updated 10/8/15
print 'retrozOR_hosprate', scipy.stats.pearsonr(retrozOR, CHR) # nan
print 'retrozOR_mortrisk', scipy.stats.pearsonr(retrozOR, CFR) # nan
print 'retrozOR_dIratio', scipy.stats.pearsonr(retrozOR, dI_ratio) # nan
print 'retrozOR_inpoutp', scipy.stats.pearsonr(retrozOR, inp_outp) # R = 0.416, p-value = 0.305
print 'retrozOR_inpatientAR', scipy.stats.pearsonr(retrozOR, inpAR) # R = 0.442, p-value = 0.273


