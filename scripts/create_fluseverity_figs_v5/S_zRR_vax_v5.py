#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: scatter plot zOR metrics vs. trivalent vaccine match and vaccine efficacy at national level
# 7/20/15: new notation
# 7/24/15: add horizontal line
# 10/8/15: rm classif, overline, color points, p-values

###Import data: Py_export/SDI_nat_classif_covCareAdj_v5_7.csv, SQL_export/subtype5.csv

###Command Line: python S_zRR_vax_v5.py
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


### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### functions ###

### data files ###
zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv','r')
zORin.readline() # rm header
zOR = csv.reader(zORin, delimiter=',')
subin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype5.csv','r')
# SEASON_NUM | SEASON_YRS | SUBTYPE     | SUBTYPE_marker | H1_ISOLATES | H3_ISOLATES | B_ISOLATES | TOT_ISOLATES | H1_MATCH | H3_MATCH | B_MATCH | TOT_MATCH | # variable names
sub = csv.reader(subin, delimiter=',')

## read national zOR data ##
# d_nat_classif[season] = (mean retro zOR, mean early zOR)
d_nat_classif = fxn.readNationalClassifFile(zOR)
## read vaxmatch data ##
d_vaxmatch = fxn.season_vaxmatch(sub)
### vax efficacy TIV and LAIV ###
# source = Osterholm2012 & USfluvaxdata_June13.ods #
seasonnum = [1, 2, 3, 4, 5, 6, 7, 8, 9]
vaxeff_wt = [69.1, 54.6, 64.0, float('nan'), 61.5, 28.1, 57.8, 60.5, 76.0]
d_vaxeffic = dict(zip(seasonnum, vaxeff_wt))

# plot values
retrozOR = [d_nat_classif[s][0] for s in ps]
vaxmatch = [d_vaxmatch[s]*100 for s in ps]
vaxeffic = [d_vaxeffic[s] for s in ps]
vals = zip(retrozOR, vaxmatch, vaxeffic)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# mean retro zOR vs vaccine match
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
for key in d_plotCol:
	ax1.plot([d_plotData[k][1] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, vaxmatch, retrozOR):
	ax1.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax1.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax1.set_xlabel('Trivalent Vaccine Match (%)', fontsize=fs)
ax1.set_xlim([0,100])
ax1.set_ylim([-15,18])
ax1.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_vaxmatch.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# mean retro zOR vs vaccine efficacy
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
for key in d_plotCol:
	ax2.plot([d_plotData[k][2] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, vaxeffic, retrozOR):
	ax2.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
ax2.set_ylabel(fxn.gp_sigma_r, fontsize=fs) 
ax2.set_xlabel('TIV/LAIV Weighted Vaccine Efficacy (%)', fontsize=fs)
ax2.set_xlim([0,100])
ax2.set_ylim([-15,18])
ax2.tick_params(axis='both', labelsize=fssml)
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_vaxeffic.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# updated 7/24/15
print 'vaxmatch corr coef', scipy.stats.pearsonr(vaxmatch, retrozOR) # R = -0.797, p-value = 0.018
print 'vaxeffic corr coef', scipy.stats.pearsonr(vaxeffic, retrozOR) # nan