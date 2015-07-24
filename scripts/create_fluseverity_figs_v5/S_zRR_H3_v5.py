#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: mean zRR retrospective classification vs. % H3 isolates of all subtyped isolates that season
# 7/20/15: update notation
# 7/24/15: add horizontal lines

###Import data: Py_export/SDI_nat_classif_covCareAdj_v5_7.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv, My_Bansal_Lab/Clean_Data_for_Import/NREVSS_Isolates_Season.csv

###Command Line: python S_zRR_H3_v5.py
##############################################


### notes ###
# The original source of isolate information is the CDC Flu Season Summaries, CDC surveillance system (not the WHO/NREVSS system).
# subtype5.csv: season, season yrs, subtype, subtype marker, H1 isolates, H3 isolates, B isolates, total isolates, H1 match, H3 match, B match, total match
# prominent subtype marker: 1 = H1; 2 = H1 & B; 3 = H1 & H3 & B; 4 = H3 & B; 5 = H3
# dominant subtype marker: 1 = H1 plurality; 2 = H3 plurality; 3 = B plurality
# (H1, H3, B, TOT) isolates: Number of isolates collected that season
# (H1, H3, B, TOT) match: Number of isolates collected that season that match the vaccine strains (H1, H3, B, trivalent vax in general)

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###
# d_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)

### functions ###
### data files ###
subvaxin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype5.csv', 'r')
subvax = csv.reader(subvaxin, delimiter=',')
natixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv', 'r')
natixin.readline() # remove header
natix = csv.reader(natixin, delimiter=',')
thanksin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

nrevss_subin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/NREVSS_Isolates_Season_improved.csv', 'r')
nrevss_subin.readline() # remove header
nrevss_sub = csv.reader(nrevss_subin, delimiter=',')
nrevss_thanksin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/NREVSS_Isolates_Thanksgiving.csv', 'r')
nrevss_thanksin.readline()
nrevss_thanks = csv.reader(nrevss_thanksin, delimiter=',')

benchin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/benchmark_ixT_avg_quantileThresh.csv', 'r')
benchin.readline()
bench = csv.reader(benchin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### program ###
# import data
# d_H3cdc[seasonnum] = proportion of H3 isolates of all subtyped isolates collected that season from CDC surveillance
# d_H3nrevss[seasonnum] = proportion of H3 isolates of all subtyped isolates collected that season from WHO/NREVSS surveillance
# d_H3nrevss_Thanks[season] = proportion of H3 isolates of all subtyped isolates collected during the season up to and including the week of Thanksgiving from WHO/NREVSS surveillance
d_H3cdc = fxn.season_H3perc_CDC(subvax)
d_H3nrevss = fxn.season_H3perc_NREVSS(nrevss_sub)
d_H3nrevss_Thanks = fxn.Thanksgiving_H3perc_NREVSS(nrevss_thanks)

# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.readNationalClassifFile(natix)

# dict_benchmark[seasonnum] = CDC severity index value
d_benchmark = fxn.benchmark_import(bench, 1)

# plot values
H3cdc = [d_H3cdc[s] for s in ps]
H3nrevss = [d_H3nrevss[s] for s in ps]
H3Thanks = [d_H3nrevss_Thanks[s] for s in ps]
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = [d_classifzOR[s][1] for s in ps]
benchmark = [d_benchmark[s] for s in ps]

# draw plots
###################################################
# cumulative H3 isolates for entire season
# 7/20/15: not in supplement
# # retrospective vs. H3 cdc
# plt.plot(H3cdc, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3cdc, retrozOR):
# 	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_sigma_r, fontsize=fs)
# plt.xlabel('H3 Proportion (CDC, Season)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/zRR_H3_cdc.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

# retrospective vs. H3 nrevss
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.plot(H3nrevss, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3nrevss, retrozOR):
	ax2.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
ax2.hlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax2.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax2.set_xlabel('H3 Proportion (NREVSS)', fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([0,1])
ax2.set_ylim([-15, 18])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/zRR_H3_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# 7/20/15: not in supplement
# # Benchmark index vs. H3 nrevss
# plt.plot(H3nrevss, benchmark, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3nrevss, benchmark):
# 	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_benchmark, fontsize=fs)
# plt.xlabel('H3 Proportion (NREVSS, Season)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.ylim([-1.5,1.5])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/benchmark_H3_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

###################################################
# cumulative H3 isolates to Thanksgiving
# 7/20/15: not in supplement
# # H3 total season vs. H3 Thanksgiving
# plt.plot(H3Thanks, H3nrevss, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3Thanks, H3nrevss):
# 	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel('H3 Proportion (NREVSS, Season)', fontsize=fs)
# plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/H3cum_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

# 7/20/15: not in supplement
# # retrospective vs. H3 Thanksgiving
# plt.plot(H3Thanks, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3Thanks, retrozOR):
# 	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_sigma_r, fontsize=fs)
# plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/zRR_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

# 7/20/15: not in supplement
# # early warning vs. H3 Thanksgiving
# plt.plot(H3Thanks, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3Thanks, earlyzOR):
# 	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_sigma_w, fontsize=fs)
# plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/earlyzOR_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

# 7/20/15: not in supplement
# # Benchmark index vs. H3 Thanksgiving
# plt.plot(H3Thanks, benchmark, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3Thanks, benchmark):
# 	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_benchmark, fontsize=fs)
# plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.ylim([-1.5,1.5])
# plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures/benchmark_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

###################################################
# 5/7/14 these figures weren't exactly what we are interested in
# 7/20/15: not in supplement
# # early warning vs. H3 cdc
# plt.plot(H3cdc, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3cdc, earlyzOR):
# 	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_sigma_w, fontsize=fs)
# plt.xlabel('H3 Proportion (CDC, Season)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/zRR_H3_cdc_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

# 7/20/15: not in supplement
# plt.plot(H3nrevss, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
# for s, x, y in zip(sl, H3nrevss, earlyzOR):
# 	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
# plt.ylabel(fxn.gp_sigma_w, fontsize=fs)
# plt.xlabel('H3 Proportion (NREVSS, Season)', fontsize=fs)
# plt.xticks(fontsize=fssml)
# plt.yticks(fontsize=fssml)
# plt.xlim([0,1])
# plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/zRR_H3_nrevss_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
# plt.close()

# updated 2/11/15
print 'zRR H3 NREVSS corr coef', np.corrcoef(H3nrevss, retrozOR) # 0.458
