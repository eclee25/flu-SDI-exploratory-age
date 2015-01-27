#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/20/15
###Function: relative risk of adult ILI to child ILI visits for the entire season vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index. 

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv, SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python S_seasonRR_benchmark_v5.py
##############################################

### notes ###

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###

### local functions ###
def entireSeasonRR(dict_ageILIadj_season, dict_pop, seasonnum):
	''' Calculate relative risk based off of adjusted ILI visits from weeks 40 through 20 in flu season.
	''' 
	ILI_ratio = sum(dict_ageILIadj_season[(seasonnum,'A')][:fw])/sum(dict_ageILIadj_season[(seasonnum,'C')][:fw])
	pop_ratio = (dict_pop[(seasonnum, 'C')])/(dict_pop[(seasonnum, 'A')])
	return ILI_ratio * pop_ratio

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
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
fw = fxn.gp_fluweeks

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_benchmark = fxn.benchmark_import(ix, 8) # no ILINet

# dict_wk[wk] = seasonnum
# dict_totIncid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
# dict_totIncidAdj53ls[s] = [adjusted incid rate per 100000 wk 40, ...adj incid wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
# dict_ageILIadj_season[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]
# dict_RR53ls[s] = [RR wk 40,... RR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
# dict_zRR53ls[s] = [zRR wk 40,... zRR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zRR_processing(d_wk, d_totIncidAdj53ls, d_zRR53ls)

# plot values
benchmark = [d_benchmark[s] for s in ps]
fluSeason_RR = [entireSeasonRR(d_ageILIadj_season, d_pop, s) for s in ps]

print 'entire season corr coef', np.corrcoef(benchmark, fluSeason_RR) # 0.738

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# mean retro zOR vs. benchmark index
ax1.plot(benchmark, fluSeason_RR, marker = 'o', color = 'black', linestyle = 'None')
ax1.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax1.annotate('Mild', xy=(-4.75,0.9), fontsize=fssml)
ax1.annotate('Severe', xy=(4,0.9), fontsize=fssml)
for s, x, y in zip(sl, benchmark, fluSeason_RR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel('Flu Season RR', fontsize=fs) 
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-5,5])
ax1.set_ylim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/seasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()


