#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/15/15
###Function: correlation coefficient between benchmark and zRR vs. moving 2 week window for SDI data for 7 week summer baseline

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python S_corrCoef_2wkPeriod_v5.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###
### functions ###
### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
norm = fxn.gp_normweeks
fs = 24
fssml = 16
lw = fxn.gp_linewidth
# custom xticks for window period
wk1 = range(40,54) + range(1,39)
first_wk = [('0'+str(wk))[-2:] for wk in wk1]
wk2 = range(41,54) + range(1,40)
sec_wk = [('0'+str(wk))[-2:] for wk in wk2]
window_xticks = [fir+sec for fir, sec in zip(first_wk, sec_wk)]

### program ###
# import benchmark
# d_benchmark[seasonnum] = CDC benchmark index value
d_benchmark = fxn.benchmark_import(ix, 8) # no ILINet
benchmarks = [d_benchmark[s] for s in ps]

###################################
### 7 week summer baseline ###

# dict_wk[wk] = seasonnum
# dict_totIncid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
# dict_totIncidAdj53ls[s] = [adjusted incid rate per 100000 wk 40, ...adj incid wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
# dict_RR53ls[s] = [RR wk 40,... RR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
# dict_zRR53ls[s] = [zRR wk 40,... zRR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2_altbaseline(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)

# preparation of values for Pearson R calculation
d_window_zRRma = fxn.zRR_movingAverage_windows(d_zRR53ls, 2)
# calculate Pearson's correlation coefficient between zRR moving average and benchmark for each window period
benchmark_zRRma_corr = [pearsonr(d_window_zRRma[w], benchmarks)[0] for w in sorted(d_window_zRRma)]
print [np.mean(d_zRR53ls[s][:2]) for s in ps]
print d_window_zRRma[0]
print benchmarks

fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
ax1.plot(range(52), benchmark_zRRma_corr, marker='o', color='black', linestyle='solid', linewidth=lw)
ax1.set_ylabel(r'Pearson R: $\beta$ & $\sigma(t)$ (2-wk mean)', fontsize=fs) 
ax1.set_xlabel('Window Period', fontsize=fs)
plt.xticks(range(52)[::5], window_xticks[::5])
ax1.set_xlim([0,53])
ax1.set_ylim([-0.5,1.0])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/corrCoef_window_summerBL.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

