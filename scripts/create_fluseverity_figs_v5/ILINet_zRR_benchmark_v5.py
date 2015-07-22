#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: mean peak-based retro zOR metric vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index
# 11/4 convert to v5: covCare adjustment, RR, a:c
# 7/21/15: update beta, notation
# 7/22/15: qualitative beta thresholds

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index_long.csv, CDC_Source/Import_Data/all_cdc_source_data.csv, Census/Import_Data/totalpop_age_Census_98-14.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python ILINet_zRR_benchmark_v5.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season
# 2013-14 ILINet data is normalized by estimated population size from December 2013 because 2014 estimates are not available at this time
# 2009-10 data is removed from cdc_severity_index_long.csv

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###

### functions ###
### data files ###
sevin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_nat_classif_covCareAdj_7.csv','r')
sevin.readline() # remove header
sev = csv.reader(sevin, delimiter=',')
ixqin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ixqin.readline()
ixq = csv.reader(ixqin, delimiter=',')
ixq2in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ixq2in.readline()
ixq2 = csv.reader(ixq2in, delimiter=',')

## normalization schemes
combo, bench_ix, q_ix = "", 1, 7
# combo, bench_ix, q_ix = "_norm1", 2, 8
# combo, bench_ix, q_ix = "_norm2", 3, 9

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_ILINet_seasonlabels
fs = 24
fssml = 16

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
# d_qual_classif[seasonnum] = qualitative severity code (-1=mild, 0=mod, 1=sev)
d_benchmark = fxn.benchmark_import(ixq, bench_ix) # norm0=1, norm1=2, norm2=3
d_classifzOR = fxn.readNationalClassifFile(sev)
d_qual_classif = fxn.benchmark_import(ixq2, q_ix) # norm0=7, norm1=8, norm2=9

# plot values
benchmark = [d_benchmark[s] for s in ps]
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = np.ma.masked_invalid([d_classifzOR[s][1] for s in ps])
print d_benchmark
print d_qual_classif

# grab beta threshold values
mildThresh, sevThresh = fxn.return_benchmark_thresholds(d_benchmark, d_qual_classif)

for s, i, j in zip(ps, benchmark, retrozOR):
	print s, i, j # to determine number of matches

# draw plots
# mean retro zOR vs. benchmark index
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
ax1.plot(benchmark, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
ax1.vlines([mildThresh, sevThresh], -20, 30, colors='k', linestyles='solid')
ax1.hlines([-1, 1], -20, 30, colors='k', linestyles='solid')
ax1.fill([-6, mildThresh, mildThresh, -6], [-1, -1, -20, -20], facecolor='blue', alpha=0.4)
ax1.fill([mildThresh, sevThresh, sevThresh, mildThresh], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax1.fill([sevThresh, 10, 10, sevThresh], [1, 1, 30, 30], facecolor='red', alpha=0.4)
ax1.annotate('Mild', xy=(-1.4,-8), fontsize=fssml)
ax1.annotate('Severe', xy=(1.1,3), fontsize=fssml)
for s, x, y in zip(sl, benchmark, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-15,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both',labelsize=fssml)
ax1.set_xlim([-1.5,1.5])
ax1.set_ylim([-10,30])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/ILINet_zRR_benchmark%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean early warning zOR vs. benchmark index
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.plot(benchmark, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
ax2.vlines([mildThresh, sevThresh], -20, 20, colors='k', linestyles='solid')
ax2.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax2.fill([-6, mildThresh, mildThresh, -6], [-1, -1, -20, -20], facecolor='blue', alpha=0.4)
ax2.fill([mildThresh, sevThresh, sevThresh, mildThresh], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax2.fill([sevThresh, 10, 10, sevThresh], [1, 1, 20, 20], facecolor='red', alpha=0.4)
ax2.annotate('Mild', xy=(-1.4,-4.5), fontsize=fssml)
ax2.annotate('Severe', xy=(1.1,11), fontsize=fssml)
for s, x, y in zip(sl, benchmark, earlyzOR):
	ax2.annotate(s, xy=(x,y), xytext=(-15,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_w, fontsize=fs)
ax2.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-1.5,1.5])
ax2.set_ylim([-5,10])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/ILINet_zRR_benchmark_early%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# updated 2/13/15 reported: initial, norm2, norm1
print 'retro corr coef', np.corrcoef(benchmark, retrozOR) 
# 2/13/15: 0.701, 0.366, 0.399
# 7/21/15: 0.637, 0.302, 0.374
mask_bench = np.ma.array(benchmark, mask=np.ma.getmask(earlyzOR))
print 'early corr coef', np.corrcoef(mask_bench.compressed(), earlyzOR.compressed()) 
# 2/13/15: -.261, , 
# 7/21/15: -0.165, 0.092, 0.041