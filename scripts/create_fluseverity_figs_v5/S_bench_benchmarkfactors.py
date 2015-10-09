#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/25/14
###Function: scatter plot benchmark index vs. benchmark index contributing factors at national level
# 7/20/15: update benchmark
# 7/23/15: add benchmark thresholds

###Import data: CDC_Source/Import_Data/cdc_severity_data_cleaned.csv

###Command Line: python Supp_bench_benchmarkfactors.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

## local modules ##
import functions_v5 as fxn
### data structures ###

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### functions ###

### data files ###
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')
ix2in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ix2in.readline()
ix2 = csv.reader(ix2in, delimiter=',')
factorsin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_data_cleaned.csv', 'r')
factorsin.readline() # rm header
factors = csv.reader(factorsin, delimiter=',')

## normalization schemes
combo, bench_ix, q_ix = "", 1, 7
# combo, bench_ix, q_ix = "_norm1", 2, 8
# combo, bench_ix, q_ix = "_norm2", 3, 9

## read benchmark index data ##
# d_benchmark[season] = index value
d_benchmark = fxn.benchmark_import(ix, bench_ix)
d_qual_classif = fxn.benchmark_import(ix2, q_ix)
# grab beta thresholds
mildThresh, sevThresh = fxn.return_benchmark_thresholds(d_benchmark, d_qual_classif)

## read benchmark data ##
# dict_benchfactors[season] = (percent positive isolates, proportion of total mortality due to P&I, number of pediatric deaths, child hospitalization rate, adult hospitalization rate)
d_benchfactors = fxn.benchmark_factors_import(factors)

# plot values
index = [d_benchmark[s] for s in ps]
pos_iso = [d_benchfactors[s][0] for s in ps]
pi_mort = [d_benchfactors[s][1]*100 for s in ps]
ped_dea = [d_benchfactors[s][2] for s in ps]
c_hos = [d_benchfactors[s][3] for s in ps]
a_hos = [d_benchfactors[s][4] for s in ps]
vals = zip(index, pos_iso, pi_mort, ped_dea, c_hos, a_hos)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# benchmark vs. positive isolates
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
for key in d_plotCol:
	ax1.plot([d_plotData[k][1] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, pos_iso, index):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax1.set_xlabel('Positive Flu Isolates (%)', fontsize=fs)
ax1.set_xlim([0,20])
ax1.set_ylim([-1.5,1.5])
ax1.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/bench_posiso%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark vs. P&I mortality of total mortality (%)
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
for key in d_plotCol:
	ax2.plot([d_plotData[k][2] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, pi_mort, index):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax2.set_xlabel('All-Cause Mortality due to P&I (%)', fontsize=fs)
ax2.set_xlim([6, 8])
ax2.set_ylim([-1.5,1.5])
ax2.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/bench_pimort%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark vs. number of pediatric deaths
fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
for key in d_plotCol:
	ax3.plot([d_plotData[k][3] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, ped_dea, index):
	ax3.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax3.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax3.set_xlabel('Pediatric Deaths', fontsize=fs)
ax3.set_xlim([40,100])
ax3.set_ylim([-1.5,1.5])
ax3.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/bench_peddea%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark vs. child hosp rate
fig4 = plt.figure()
ax4 = fig4.add_subplot(1,1,1)
for key in d_plotCol:
	ax4.plot([d_plotData[k][4] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, c_hos, index):
	ax4.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax4.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax4.set_xlabel('5-17 Years Hosp. Rate (per 100,000)', fontsize=fs)
ax4.set_xlim([0,10])
ax4.set_ylim([-1.5,1.5])
ax4.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/bench_chos%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark vs. adult hosp rate
fig5 = plt.figure()
ax5 = fig5.add_subplot(1,1,1)
for key in d_plotCol:
	ax5.plot([d_plotData[k][5] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, a_hos, index):
	ax5.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax5.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax5.set_xlabel('18-49 Years Hosp. Rate (per 100,000)', fontsize=fs)
ax5.set_xlim([0,10])
ax5.set_ylim([-1.5,1.5])
ax5.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/bench_ahos%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

## correlation coefficients ##
cor_pos = scipy.stats.pearsonr(index, pos_iso)
cor_pi = scipy.stats.pearsonr(index, pi_mort)
cor_ped = np.corrcoef(index, ped_dea)
cor_chos = np.corrcoef(index, c_hos)
cor_ahos = np.corrcoef(index, a_hos)

# updated 10/8/15
print cor_pos # R = 0.911, p- value: 0.0016
print cor_pi # R = 0.837, p-value: 0.0096
print cor_ped # nan
print cor_chos # nan
print cor_ahos # nan

