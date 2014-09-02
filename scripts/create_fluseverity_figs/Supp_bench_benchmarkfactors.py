#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/25/14
###Function: scatter plot benchmark index vs. benchmark index contributing factors at national level

###Import data: CDC_Source/Import_Data/cdc_severity_data_cleaned.csv

###Command Line: python Supp_bench_benchmarkfactors.py
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
benchin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv','r')
benchin.readline() # rm header
bench = csv.reader(benchin, delimiter=',')
factorsin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_data_cleaned.csv', 'r')
factorsin.readline() # rm header
factors = csv.reader(factorsin, delimiter=',')

## read benchmark index data ##
# d_benchmark[season] = index value
d_benchmark = fxn.benchmark_import(bench, 8)
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

# mean retro zOR vs. positive isolates
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
ax1.plot(pos_iso, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, pos_iso, index):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax1.set_xlabel('Positive Flu Isolates (%)', fontsize=fs)
ax1.set_xlim([0,20])
ax1.set_ylim([-5,5])
ax1.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_posiso.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. P&I mortality of total mortality (%)
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.plot(pi_mort, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, pi_mort, index):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax2.set_xlabel('All-Cause Mortality due to P&I (%)', fontsize=fs)
ax2.set_xlim([6, 8])
ax2.set_ylim([-5,5])
ax2.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_pimort.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. number of pediatric deaths
fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
ax3.plot(ped_dea, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ped_dea, index):
	ax3.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax3.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax3.set_xlabel('Pediatric Deaths', fontsize=fs)
ax3.set_xlim([40,100])
ax3.set_ylim([-5,5])
ax3.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_peddea.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark index vs. child hosp rate
fig4 = plt.figure()
ax4 = fig4.add_subplot(1,1,1)
ax4.plot(c_hos, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, c_hos, index):
	ax4.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax4.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax4.set_xlabel('Child Hosp. Rate (per 100,000)', fontsize=fs)
ax4.set_xlim([0,10])
ax4.set_ylim([-5,5])
ax4.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_chos.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark index vs. adult hosp rate
fig5 = plt.figure()
ax5 = fig5.add_subplot(1,1,1)
ax5.plot(a_hos, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, a_hos, index):
	ax5.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax5.set_ylabel(fxn.gp_benchmark, fontsize=fs) 
ax5.set_xlabel('Adult Hosp. Rate (per 100,000)', fontsize=fs)
ax5.set_xlim([0,10])
ax5.set_ylim([-5,5])
ax5.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_ahos.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

## correlation coefficients ##
cor_pos = np.corrcoef(index, pos_iso)
cor_pi = np.corrcoef(index, pi_mort)
cor_ped = np.corrcoef(index, ped_dea)
cor_chos = np.corrcoef(index, c_hos)
cor_ahos = np.corrcoef(index, a_hos)

print cor_pos
print cor_pi
print cor_ped
print cor_chos
print cor_ahos

