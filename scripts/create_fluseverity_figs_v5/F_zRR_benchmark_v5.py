#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14
###Function: mean peak-based retro zOR metric vs. CDC benchmark index, mean Thanksgiving-based early zOR metric vs. CDC benchmark index. 
# 10/14/14 OR age flip.
# 10/15 ILI incidence ratio (obsolete)
# 10/19 incidence rate adjusted by any diagnosis visits (coverage adj = visits S9/visits S#) and ILI care-seeking behavior; change to relative risk
# 10/31 coverage adjustment no longer age-specific
# 7/20/15: new beta
# 7/21/15: pearson's r with scipy.stats, adds p-value
# 7/22/15: beta threshold based on qualitative coding
# 10/5/15: remove all thresholds

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv, SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python F3_zRR_benchmark_v5.py
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

### functions ###
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
sevCol = fxn.gp_mild_severe_colors

## normalization schemes
combo, bench_ix, q_ix = "", 1, 7
# combo, bench_ix, q_ix = "_norm1", 2, 8 # pre-post pandemic
# combo, bench_ix, q_ix = "_norm2", 3, 9 # antigenic cluster

### program ###
# import data
# d_benchmark[seasonnum] = CDC benchmark index value
# d_qual_classif[seasonnum] = qualitative severity code (-1=mild, 0=mod, 1=sev)
d_benchmark = fxn.benchmark_import(ix, bench_ix)
d_qual_classif = fxn.benchmark_import(ix2, q_ix)

# dict_wk[wk] = seasonnum
# dict_totIncid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
# dict_totIncidAdj53ls[s] = [adjusted incid rate per 100000 wk 40, ...adj incid wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
# dict_RR53ls[s] = [RR wk 40,... RR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
# dict_zRR53ls[s] = [zRR wk 40,... zRR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zRR_processing(d_wk, d_totIncidAdj53ls, d_zRR53ls)

# plot values
benchmark = [d_benchmark[s] for s in ps]
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = [d_classifzOR[s][1] for s in ps]
vals = zip(benchmark, retrozOR, earlyzOR)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix
print d_plotCol


# correlation values
mask_earlyzOR = np.ma.masked_invalid(earlyzOR)
mask_benchmark = np.ma.array(benchmark, mask=np.ma.getmask(mask_earlyzOR))
compMask_earlyzOR = np.ma.compressed(mask_earlyzOR)
compMask_benchmark = np.ma.compressed(mask_benchmark)


# print 'retro corr coef', np.corrcoef(benchmark, retrozOR) # 7/20/15: 0.707
# print 'early corr coef', np.corrcoef(compMask_benchmark, compMask_earlyzOR) # 7/20/15: 0.594
print 'retro pearsonr', scipy.stats.pearsonr(benchmark, retrozOR) 
# norm0: R = 0.707, p-value = 0.05
# norm1: R = 0.765, p-value = 0.027
# norm2: R = 0.755, p-value = 0.030
print 'early pearsonr', scipy.stats.pearsonr(compMask_benchmark, compMask_earlyzOR) 
# norm0: R = 0.594, p-value = 0.16
# norm1: R = 0.713, p-value = 0.072
# norm2: R = 0.666, p-value = 0.102

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
# mean retro zOR vs. benchmark index
for key in d_plotCol:
	ax1.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][1] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax1.annotate('Mild', xy=(-1.4,-14), fontsize=fssml, color = sevCol[0])
ax1.annotate('Severe', xy=(1.1,15.5), fontsize=fssml, color = sevCol[1])
for s, x, y in zip(sl, benchmark, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax1.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-1.5,1.5])
ax1.set_ylim([-15,18])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/MainFigures/zRR_benchmark%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()


fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
# mean early warning zOR vs. benchmark index
for key in d_plotCol:
	ax2.plot([d_plotData[k][0] for k in d_plotCol[key]], [d_plotData[k][2] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
ax2.annotate('Mild', xy=(-1.4,-9.5), fontsize=fssml, color = sevCol[0])
ax2.annotate('Severe', xy=(1.1,8.5), fontsize=fssml, color = sevCol[1])
for s, x, y in zip(sl, benchmark, earlyzOR):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_w, fontsize=fs) 
ax2.set_xlabel(fxn.gp_benchmark, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-1.5,1.5])
ax2.set_ylim([-10,10])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/MainFigures/zRR_benchmark_early%s.png' %(combo), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()
