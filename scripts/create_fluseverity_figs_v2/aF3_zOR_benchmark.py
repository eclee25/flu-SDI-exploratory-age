#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/14/14
###Function: mean peak-based retro zOR metric vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index. 10/14/14 OR age flip.

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv, SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python aF3_zOR_benchmark.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v2 as fxn

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
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_benchmark = fxn.benchmark_import(ix, 8) # no ILINet

# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)
# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zOR_processing(d_wk, d_incid53ls, d_zOR53ls, thanks)

# plot values
benchmark = [d_benchmark[s] for s in ps]
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = [d_classifzOR[s][1] for s in ps]

print 'retro corr coef', np.corrcoef(benchmark, retrozOR)
print 'early corr coef', np.corrcoef(benchmark, earlyzOR)

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# mean retro zOR vs. benchmark index
ax1.plot(benchmark, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
ax1.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax1.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax1.fill([-5, -1, -1, -5], [-1, -1, -15, -15], facecolor='blue', alpha=0.4)
ax1.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax1.fill([1, 5, 5, 1], [1, 1, 15, 15], facecolor='red', alpha=0.4)
ax1.annotate('Mild', xy=(-4.75,-14), fontsize=fssml)
ax1.annotate('Severe', xy=(1.25,13), fontsize=fssml)
for s, x, y in zip(sl, benchmark, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-5,5])
ax1.set_ylim([-15,15])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v2/F3/zOR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
# mean early warning zOR vs. benchmark index
ax2.plot(benchmark, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
ax2.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax2.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax2.fill([-5, -1, -1, -5], [-1, -1, -15, -15], facecolor='blue', alpha=0.4)
ax2.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax2.fill([1, 5, 5, 1], [1, 1, 15, 15], facecolor='red', alpha=0.4)
ax2.annotate('Mild', xy=(-4.75,-9.5), fontsize=fssml)
ax2.annotate('Severe', xy=(1.25,8.5), fontsize=fssml)
for s, x, y in zip(sl, benchmark, earlyzOR):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_w, fontsize=fs) 
ax2.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-5,5])
ax2.set_ylim([-10,10])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v2/F3/zOR_benchmark_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()
