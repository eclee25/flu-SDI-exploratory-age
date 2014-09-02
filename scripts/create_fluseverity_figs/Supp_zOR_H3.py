#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/24/14
###Function: mean zOR retrospective classification vs. % H3 isolates of all subtyped isolates that season

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/subtype5.csv, SQL_export/totalpop.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv, My_Bansal_Lab/Clean_Data_for_Import/NREVSS_Isolates_Season.csv

###Command Line: python Supp_zOR_H3.py
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

## local modules ##
import functions as fxn

### data structures ###
# d_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)

### functions ###
### data files ###
subvaxin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype5.csv', 'r')
subvax = csv.reader(subvaxin, delimiter=',')
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

nrevss_subin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/NREVSS_Isolates_Season_improved.csv', 'r')
nrevss_subin.readline() # remove header
nrevss_sub = csv.reader(nrevss_subin, delimiter=',')
nrevss_thanksin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/NREVSS_Isolates_Thanksgiving.csv', 'r')
nrevss_thanksin.readline()
nrevss_thanks = csv.reader(nrevss_thanksin, delimiter=',')

benchin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv', 'r')
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
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_H3cdc = fxn.season_H3perc_CDC(subvax)
d_H3nrevss = fxn.season_H3perc_NREVSS(nrevss_sub)
d_H3nrevss_Thanks = fxn.Thanksgiving_H3perc_NREVSS(nrevss_thanks)
# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)
# dict_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zOR_processing(d_wk, d_incid53ls, d_zOR53ls, thanks)
# dict_benchmark[seasonnum] = CDC severity index value
d_benchmark = fxn.benchmark_import(bench, 8)

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
# retrospective vs. H3 cdc
plt.plot(H3cdc, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3cdc, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_sigma_r, fontsize=fs)
plt.xlabel('H3 Proportion (CDC, Season)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/zOR_H3_cdc.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# retrospective vs. H3 nrevss
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.plot(H3nrevss, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3nrevss, retrozOR):
	ax2.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_r, fontsize=fs)
ax2.set_xlabel('H3 Proportion (NREVSS)', fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([0,1])
ax2.invert_yaxis()
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/zOR_H3_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# Benchmark index vs. H3 nrevss
plt.plot(H3nrevss, benchmark, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3nrevss, benchmark):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_benchmark, fontsize=fs)
plt.xlabel('H3 Proportion (NREVSS, Season)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.ylim([-5,5])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/benchmark_H3_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

###################################################
# cumulative H3 isolates to Thanksgiving
# H3 total season vs. H3 Thanksgiving
plt.plot(H3Thanks, H3nrevss, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3Thanks, H3nrevss):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('H3 Proportion (NREVSS, Season)', fontsize=fs)
plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/H3cum_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# retrospective vs. H3 Thanksgiving
plt.plot(H3Thanks, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3Thanks, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_sigma_r, fontsize=fs)
plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/zOR_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# early warning vs. H3 Thanksgiving
plt.plot(H3Thanks, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3Thanks, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_sigma_w, fontsize=fs)
plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/earlyzOR_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# Benchmark index vs. H3 Thanksgiving
plt.plot(H3Thanks, benchmark, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3Thanks, benchmark):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_benchmark, fontsize=fs)
plt.xlabel('H3 Proportion (NREVSS, to Thanksgiving)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.ylim([-5,5])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/benchmark_H3thx_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

###################################################
# 5/7/14 these figures weren't exactly what we are interested in
# early warning vs. H3 cdc
plt.plot(H3cdc, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3cdc, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_sigma_w, fontsize=fs)
plt.xlabel('H3 Proportion (CDC, Season)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/zOR_H3_cdc_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

plt.plot(H3nrevss, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3nrevss, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel(fxn.gp_sigma_w, fontsize=fs)
plt.xlabel('H3 Proportion (NREVSS, Season)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3/zOR_H3_nrevss_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

