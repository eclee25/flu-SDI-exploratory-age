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

def tightSeasonRR(dict_ageILIadj_season, dict_pop, seasonnum):
	''' Calculate relative risk based off of adjusted ILI visits from weeks 50 through 12 in flu season.
	''' 
	ILI_ratio = sum(dict_ageILIadj_season[(seasonnum,'A')][10:fw-7])/sum(dict_ageILIadj_season[(seasonnum,'C')][10:fw-7])
	pop_ratio = (dict_pop[(seasonnum, 'C')])/(dict_pop[(seasonnum, 'A')])
	return ILI_ratio * pop_ratio

def nonfluSeasonRR(dict_ageILIadj_season, dict_pop, seasonnum):
	''' Calculate relative risk based off of adjusted ILI visits from weeks 21 to 39, which occurs during the summer after the flu season.
	''' 
	ILI_ratio = sum(dict_ageILIadj_season[(seasonnum,'A')][fw:])/sum(dict_ageILIadj_season[(seasonnum,'C')][fw:])
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
nonfluSeason_RR = [nonfluSeasonRR(d_ageILIadj_season, d_pop, s) for s in ps]
tightfluSeason_RR = [tightSeasonRR(d_ageILIadj_season, d_pop, s) for s in ps]


print 'entire flu season (40 to 20) corr coef', np.corrcoef(benchmark, fluSeason_RR) # 0.738
print 'non flu season corr coef', np.corrcoef(benchmark, nonfluSeason_RR) # 0.136
print 'tight flu season (50 to 12) corr coef', np.corrcoef(benchmark, tightfluSeason_RR) # 0.760


# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# flu season RR vs. benchmark index
ax1.plot(benchmark, fluSeason_RR, marker = 'o', color = 'black', linestyle = 'None')
ax1.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax1.annotate('Mild', xy=(-4.75,0.5), fontsize=fssml)
ax1.annotate('Severe', xy=(4,0.5), fontsize=fssml)
for s, x, y in zip(sl, benchmark, fluSeason_RR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel('Flu Season RR (R=0.74)', fontsize=fs) 
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-5,5])
ax1.set_ylim([0,0.6])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/seasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
# nonflu season vs. benchmark index
ax2.plot(benchmark, nonfluSeason_RR, marker = 'o', color = 'black', linestyle = 'None')
ax2.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax2.annotate('Mild', xy=(-4.75,0.5), fontsize=fssml)
ax2.annotate('Severe', xy=(4,0.5), fontsize=fssml)
for s, x, y in zip(sl, benchmark, nonfluSeason_RR):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel('Non-Flu Season RR (R=0.14)', fontsize=fs) 
ax2.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-5,5])
ax2.set_ylim([0,0.6])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/nonfluseasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
# tight flu season RR vs. benchmark index
ax3.plot(benchmark, tightfluSeason_RR, marker = 'o', color = 'black', linestyle = 'None')
ax3.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax3.annotate('Mild', xy=(-4.75,0.5), fontsize=fssml)
ax3.annotate('Severe', xy=(4,0.5), fontsize=fssml)
for s, x, y in zip(sl, benchmark, tightfluSeason_RR):
	ax3.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax3.set_ylabel('Weeks 50 to 12 RR (R=0.76)', fontsize=fs) 
ax3.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax3.tick_params(axis='both', labelsize=fssml)
ax3.set_xlim([-5,5])
ax3.set_ylim([0,0.6])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/tightseasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()