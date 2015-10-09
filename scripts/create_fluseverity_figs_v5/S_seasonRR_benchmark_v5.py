#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/20/15
###Function: relative risk of adult ILI to child ILI visits for the entire season vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index. 
# 7/20/15: update beta
# 10/8/15: rm lines, color points, add p-values

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv, SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python S_seasonRR_benchmark_v5.py
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
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')
ix2in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixTavg_altnorm_comparisons.csv','r')
ix2in.readline()
ix2 = csv.reader(ix2in, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
fw = fxn.gp_fluweeks
bench_ix, q_ix = 1, 7

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_benchmark = fxn.benchmark_import(ix, bench_ix)
d_qual_classif = fxn.benchmark_import(ix2, q_ix)

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
vals = zip(benchmark, fluSeason_RR, nonfluSeason_RR, tightfluSeason_RR)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# updated 10/8/15
print 'entire flu season (40 to 20) corr coef', scipy.stats.pearsonr(benchmark, fluSeason_RR) # R = 0.789, p-value = 0.020
print 'non flu season corr coef', scipy.stats.pearsonr(benchmark, nonfluSeason_RR) # R = 0.217, p-value = 0.606
print 'tight flu season (50 to 12) corr coef', scipy.stats.pearsonr(benchmark, tightfluSeason_RR) # R = 0.825, p-value = 0.012


# draw plots
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(1,1,1)
# # flu season RR vs. benchmark index
# for key in d_plotCol:
# 	ax1.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][1] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
# ax1.annotate('Mild', xy=(-1.4,0.1), fontsize=fssml)
# ax1.annotate('Severe', xy=(1.1,0.5), fontsize=fssml)
# for s, x, y in zip(sl, benchmark, fluSeason_RR):
# 	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
# ax1.set_ylabel('Flu Season RR (R=0.79)', fontsize=fs) 
# ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
# ax1.tick_params(axis='both', labelsize=fssml)
# ax1.set_xlim([-1.5,1.5])
# ax1.set_ylim([0,0.6])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/seasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()
# # plt.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
# nonflu season vs. benchmark index
for key in d_plotCol:
	ax2.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][2] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax2.annotate('Mild', xy=(-1.4,0.1), fontsize=fssml)
ax2.annotate('Severe', xy=(1.1,0.5), fontsize=fssml)
for s, x, y in zip(sl, benchmark, nonfluSeason_RR):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel('Weeks 21 to 39 RR, adult:child', fontsize=fs) 
ax2.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-1.5,1.5])
ax2.set_ylim([0,0.6])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/nonfluseasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
# tight flu season RR vs. benchmark index
for key in d_plotCol:
	ax3.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][3] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax3.annotate('Mild', xy=(-1.4,0.1), fontsize=fssml)
ax3.annotate('Severe', xy=(1.1,0.5), fontsize=fssml)
for s, x, y in zip(sl, benchmark, tightfluSeason_RR):
	ax3.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax3.set_ylabel('Weeks 50 to 12 RR, adult:child', fontsize=fs) 
ax3.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax3.tick_params(axis='both', labelsize=fssml)
ax3.set_xlim([-1.5,1.5])
ax3.set_ylim([0,0.6])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/tightseasonRR_benchmark.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()