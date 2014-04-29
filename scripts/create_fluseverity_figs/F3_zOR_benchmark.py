#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/26/14
###Function: mean peak-based retro zOR metric vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv, SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python F3_zOR_benchmark.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###

### functions ###
### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_benchmark = fxn.benchmark_import(ix)
d_classifzOR = fxn.classif_zOR_processing(incid, pop, thanks)

# plot values
benchmark = [d_benchmark[s] for s in ps]
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = [d_classifzOR[s][1] for s in ps]

print 'retro corr coef', np.corrcoef(benchmark, retrozOR)
print 'early corr coef', np.corrcoef(benchmark, earlyzOR)

# draw plots
# mean retro zOR vs. benchmark index
plt.plot(benchmark, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
plt.vlines([-1, 1], -10, 20, colors='k', linestyles='solid')
plt.hlines([-1, 1], -10, 20, colors='k', linestyles='solid')
for s, x, y in zip(sl, benchmark, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('Benchmark Index', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-5,5])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3/zOR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# mean early warning zOR vs. benchmark index
plt.plot(benchmark, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
plt.vlines([-1, 1], -10, 20, colors='k', linestyles='solid')
plt.hlines([-1, 1], -10, 20, colors='k', linestyles='solid')
for s, x, y in zip(sl, benchmark, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Early Warning zOR', fontsize=fs)
plt.xlabel('Benchmark Index', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-5,5])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3/zOR_benchmark_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

