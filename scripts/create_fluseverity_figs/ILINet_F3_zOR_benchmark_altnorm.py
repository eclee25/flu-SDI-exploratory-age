#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/19/14
###Function: mean peak-based retro zOR metric vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index_long.csv, CDC_Source/Import_Data/all_cdc_source_data.csv, Census/Import_Data/totalpop_age_Census_98-14.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python ILINet_F3_zOR_benchmark.py
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
import functions as fxn

### data structures ###

### functions ###
### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/all_cdc_source_data.csv','r')
incidin.readline() # remove header
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data/totalpop_age_Census_98-14.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')
# normalization scheme: pre-pandemic and post-pandemic (1997-98 through 2008-09, 2010-11 through 2013-14)
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index_long_norm1.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')
# normalization scheme: 1997-98 through 2002-03, 2003-04 through 2008-09, 2010-11 through 2013-14
ixin2 = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index_long_norm2.csv','r')
ixin2.readline()
ix2 = csv.reader(ixin2, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_ILINet_seasonlabels
fs = 24
fssml = 16

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
d_benchmark1 = fxn.benchmark_import(ix, 8) # no ILINet, norm scheme 1
d_benchmark2 = fxn.benchmark_import(ix2, 8) # no ILINet, norm scheme 2
# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.ILINet_week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)
# dict_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zOR_processing(d_wk, d_incid53ls, d_zOR53ls, thanks)

# plot values
benchmark1 = [d_benchmark1[s] for s in ps]
benchmark2 = [d_benchmark2[s] for s in ps]
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = [d_classifzOR[s][1] for s in ps]
print min(benchmark1), max(benchmark1)
print min(benchmark2), max(benchmark2)


print 'retro corr coef, norm 1', np.corrcoef(benchmark1, retrozOR)
print 'early corr coef, norm 1', np.corrcoef(benchmark1, earlyzOR)
print 'retro corr coef, norm 2', np.corrcoef(benchmark2, retrozOR)
print 'early corr coef, norm 2', np.corrcoef(benchmark2, earlyzOR)

# normalization scheme 1: plots
# mean retro zOR vs. benchmark index
plt.plot(benchmark1, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
plt.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
plt.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
for s, x, y in zip(sl, benchmark1, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('Benchmark Index', fontsize=fs)
plt.title('Pre and Post-pandemic normalization scheme', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-6,10])
plt.ylim([-20,20])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/ILINet/zOR_benchmark_norm1.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean early warning zOR vs. benchmark index
plt.plot(benchmark1, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
plt.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
plt.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
for s, x, y in zip(sl, benchmark1, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Early Warning zOR', fontsize=fs)
plt.xlabel('Benchmark Index', fontsize=fs)
plt.title('Pre and Post-pandemic norm scheme', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-6,10])
plt.ylim([-8,8])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/ILINet/zOR_benchmark_early_norm1.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# normalization scheme 2: plots
# mean retro zOR vs. benchmark index
plt.plot(benchmark2, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
plt.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
plt.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
for s, x, y in zip(sl, benchmark2, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('Benchmark Index', fontsize=fs)
plt.title('97-03, 03-09, 10-14 norm scheme', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-6,10])
plt.ylim([-20,20])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/ILINet/zOR_benchmark_norm2.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean early warning zOR vs. benchmark index
plt.plot(benchmark2, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
plt.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
plt.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
for s, x, y in zip(sl, benchmark2, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Early Warning zOR', fontsize=fs)
plt.xlabel('Benchmark Index', fontsize=fs)
plt.title('97-03, 03-09, 10-14 normalization scheme', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-6,10])
plt.ylim([-8,8])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/ILINet/zOR_benchmark_early_norm2.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()