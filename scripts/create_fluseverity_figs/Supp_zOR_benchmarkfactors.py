#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/25/14
###Function: scatter plot zOR metrics vs. benchmark index contributing factors at national level

###Import data: Py_export/SDI_national_classifications.csv, CDC_Source/Import_Data/cdc_severity_data_cleaned.csv

###Command Line: python Supp_zOR_benchmarkfactors.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###


### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### functions ###

### data files ###
zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications.csv','r')
zORin.readline() # rm header
zOR = csv.reader(zORin, delimiter=',')
factorsin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_data_cleaned.csv', 'r')
factorsin.readline() # rm header
factors = csv.reader(factorsin, delimiter=',')

## read national zOR data ##
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_nat_classif = fxn.readNationalClassifFile(zOR)
## read benchmark data ##
# dict_benchfactors[season] = (percent positive isolates, proportion of total mortality due to P&I, number of pediatric deaths, child hospitalization rate, adult hospitalization rate)
d_benchfactors = fxn.benchmark_factors_import(factors)

# plot values
retrozOR = [d_nat_classif[s][0] for s in ps]
pos_iso = [d_benchfactors[s][0] for s in ps]
pi_mort = [d_benchfactors[s][1]*100 for s in ps]
ped_dea = [d_benchfactors[s][2] for s in ps]
c_hos = [d_benchfactors[s][3] for s in ps]
a_hos = [d_benchfactors[s][4] for s in ps]

# mean retro zOR vs. positive isolates
plt.plot(pos_iso, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, pos_iso, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Positive Flu Isolates (%)', fontsize=fs)
plt.xlim([0,20])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_benchmarkfactors/zOR_posiso.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. P&I mortality of total mortality (%)
plt.plot(pi_mort, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, pi_mort, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Proportion of Mortality due to P&I (%)', fontsize=fs)
plt.xlim([6, 8])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_benchmarkfactors/zOR_pimort.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. number of pediatric deaths
plt.plot(ped_dea, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ped_dea, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Pediatric Deaths', fontsize=fs)
plt.xlim([40,100])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_benchmarkfactors/zOR_peddea.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. child hosp rate
plt.plot(c_hos, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, c_hos, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Child Hosp. Rate (per 100,000)', fontsize=fs)
plt.xlim([0,10])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_benchmarkfactors/zOR_chos.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. adult hosp rate
plt.plot(a_hos, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, a_hos, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Adult Hosp. Rate (per 100,000)', fontsize=fs)
plt.xlim([0,10])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_benchmarkfactors/zOR_ahos.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

## correlation coefficients ##
cor_pos = np.corrcoef(retrozOR, pos_iso)
cor_pi = np.corrcoef(retrozOR, pi_mort)
cor_ped = np.corrcoef(retrozOR, ped_dea)
cor_chos = np.corrcoef(retrozOR, c_hos)
cor_ahos = np.corrcoef(retrozOR, a_hos)

print cor_pos
print cor_pi
print cor_ped
print cor_chos
print cor_ahos

