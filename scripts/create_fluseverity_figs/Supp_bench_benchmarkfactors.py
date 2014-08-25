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
plt.plot(pos_iso, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, pos_iso, index):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Benchmark Index', fontsize=fs) 
plt.xlabel('Positive Flu Isolates (%)', fontsize=fs)
plt.xlim([0,20])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_posiso.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. P&I mortality of total mortality (%)
plt.plot(pi_mort, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, pi_mort, index):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Benchmark Index', fontsize=fs) 
plt.xlabel('Proportion of Mortality due to P&I (%)', fontsize=fs)
plt.xlim([6, 8])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_pimort.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs. number of pediatric deaths
plt.plot(ped_dea, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ped_dea, index):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Benchmark Index', fontsize=fs) 
plt.xlabel('Pediatric Deaths', fontsize=fs)
plt.xlim([40,100])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_peddea.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark index vs. child hosp rate
plt.plot(c_hos, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, c_hos, index):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Benchmark Index', fontsize=fs) 
plt.xlabel('Child Hosp. Rate (per 100,000)', fontsize=fs)
plt.xlim([0,10])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_benchmarkfactors/bench_chos.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# benchmark index vs. adult hosp rate
plt.plot(a_hos, index, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, a_hos, index):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Benchmark Index', fontsize=fs) 
plt.xlabel('Adult Hosp. Rate (per 100,000)', fontsize=fs)
plt.xlim([0,10])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
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

