#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/6/14
###Function: metric vs. CDC benchmark index, where sensitivity of baseline is examined. Given that 7 week fall baseline is what we used in our study, the 7 week summer baseline, 10 week fall baseline, and 10 week summer baseline plots are examined.

# 7/20/15: update benchmark
# 7/24/15: update benchmark with qualitative classif thresholds
# 10/8/15: rm classif, overline, Severe label, p-values

###Import data: CDC_Source/Import_Data/cdc_severity_index.csv, Py_export/SDI_national_classifications_summer-7.csv, Py_export/SDI_national_classifications_10.csv, Py_export/SDI_national_classifications_summer-10.csv

###Command Line: python Supp_zRR_benchmark_altbaseline.py
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

### functions ###
### data files ###
# benchmark data
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')
ix2in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ix2in.readline()
ix2 = csv.reader(ix2in, delimiter=',')
# 10 week fall BL index
f10in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_10.csv','r')
f10in.readline()
f10 = csv.reader(f10in, delimiter=',')
# 7 week summer BL index
s7in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_summer7.csv','r')
s7in.readline()
s7 = csv.reader(s7in, delimiter=',')
# 10 week summer BL index
s10in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_summer10.csv','r')
s10in.readline()
s10 = csv.reader(s10in, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
bench_ix, q_ix = 1, 7
sevCol = fxn.gp_mild_severe_colors

### program ###

## import data ##
# d_benchmark[seasonnum] = CDC benchmark index value
d_benchmark = fxn.benchmark_import(ix, bench_ix)
d_qual_classif = fxn.benchmark_import(ix2, q_ix)
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_f10 = fxn.readNationalClassifFile(f10)
d_s7 = fxn.readNationalClassifFile(s7)
d_s10 = fxn.readNationalClassifFile(s10)

## plot values ##
benchmark = [d_benchmark[s] for s in ps]
f10r = [d_f10[s][0] for s in ps]
s7r = [d_s7[s][0] for s in ps]
s10r = [d_s10[s][0] for s in ps]
vals = zip(benchmark, f10r, s7r, s10r)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# 10 week fall BL mean retro zOR vs. benchmark index
for key in d_plotCol:
	ax1.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][1] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax1.annotate('Mild', xy=(-1.4,-14), fontsize=fssml, color = sevCol[0])
ax1.annotate('Severe', xy=(1.1,12), fontsize=fssml, color = sevCol[1])
ax1.annotate('10 week fall baseline', xy=(-1.4,13), fontsize=fssml)
for s, x, y in zip(sl, benchmark, f10r):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-1.5,1.5])
ax1.set_ylim([-15,15])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR-fall10_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
# 7 week summer BL mean retro zOR vs. benchmark index
for key in d_plotCol:
	ax2.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][2] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax2.annotate('Mild', xy=(-1.4,-14), fontsize=fssml, color = sevCol[0])
ax2.annotate('Severe', xy=(1.1,12), fontsize=fssml, color = sevCol[1])
ax2.annotate('7 week summer baseline', xy=(-1.4,13), fontsize=fssml)
for s, x, y in zip(sl, benchmark, s7r):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax2.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-1.5,1.5])
ax2.set_ylim([-15,15])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR-summer7_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
# 10 week summer BL mean retro zOR vs. benchmark index
for key in d_plotCol:
	ax3.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][3] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax3.annotate('Mild', xy=(-1.4,-14), fontsize=fssml, color = sevCol[0])
ax3.annotate('Severe', xy=(1.1,12), fontsize=fssml, color = sevCol[1])
ax3.annotate('10 week summer baseline', xy=(-1.4,13), fontsize=fssml)
for s, x, y in zip(sl, benchmark, s10r):
	ax3.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax3.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax3.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax3.tick_params(axis='both', labelsize=fssml)
ax3.set_xlim([-1.5,1.5])
ax3.set_ylim([-15,15])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR-summer10_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# updated 7/24/15
print '10 week fall corr coef', scipy.stats.pearsonr(benchmark, f10r) # R = 0.745, p-value = 0.034
print '7 week summer corr coef', scipy.stats.pearsonr(benchmark, s7r) # R = 0.665, p-value = 0.072
print '10 week summer corr coef', scipy.stats.pearsonr(benchmark, s10r) # R = 0.703, p-value = 0.052
