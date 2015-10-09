#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: plot SDI zOR vs. ILINet zOR(supp figure)
# 11/4 v5 updates
# 7/23/15: new notation
# 7/24/15: cdc notation added to title
# 10/8/15: rm classif, overline, color points

###Import data: 


###Command Line: python S_zRR_SDI_ILINet_v5.py
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
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
sevCol = fxn.gp_mild_severe_colors

### data files ###
# SDI classifications file 
SDIclassif_in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv', 'r')
SDIclassif_in.readline() # remove header
SDIclassif = csv.reader(SDIclassif_in, delimiter=',')
# ILINet classifications file
ILINetclassif_in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_nat_classif_covCareAdj_7.csv', 'r')
ILINetclassif_in.readline() # remove header
ILINetclassif = csv.reader(ILINetclassif_in, delimiter=',')

### program ###
# d_dataset_classif[season] = (mn_retro_zOR, mn_early_zOR)
## import SDI zOR classifications ##
d_SDI_classif = fxn.readNationalClassifFile(SDIclassif)
## import ILINet zOR classifications ##
d_ILINet_classif = fxn.readNationalClassifFile(ILINetclassif)

# plot values
SDI_retro = [d_SDI_classif[s][0] for s in ps]
ILINet_retro = [d_ILINet_classif[s][0] for s in ps] 
SDI_early = [d_SDI_classif[s][1] for s in ps]
ILINet_early = [d_ILINet_classif[s][1] for s in ps] 
vals = zip(SDI_retro, ILINet_retro, SDI_early, ILINet_early)
d_plotData = dict(zip(ps, vals))
d_plotCol = fxn.gp_CDCclassif_ix

# draw plots
# SDI vs ILINet retrospective zOR
fig1 = plt.figure()
ax1 = plt.subplot(111)
for key in d_plotCol:
	ax1.plot([d_plotData[k][1] for k in d_plotCol[key]], [d_plotData[k][0] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, ILINet_retro, SDI_retro):
	ax1.annotate(s, xy=(x,y), xytext=(-25,-15), textcoords='offset points', fontsize=fssml)
ax1.annotate('Mild', xy=(-4.8,-9), fontsize=fssml, color = sevCol[0])
ax1.annotate('Severe', xy=(3.5,15.5), fontsize=fssml, color = sevCol[1])
ax1.set_ylabel(r'medical claims ($\overline{\rho_{s,r}}$)', fontsize=fs)
ax1.set_xlabel(r'ILINet ($\overline{\rho_{s,r}^{cdc}}$)', fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-5,5])
ax1.set_ylim([-15,18])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_SDI_ILINet_retro.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# SDI vs ILINet early warning zOR
fig2 = plt.figure()
ax2 = plt.subplot(111)
for key in d_plotCol:
	ax2.plot([d_plotData[k][3] for k in d_plotCol[key]], [d_plotData[k][2] for k in d_plotCol[key]], marker = 'o', color = key, linestyle = 'None')
for s, x, y in zip(sl, ILINet_early, SDI_early):
	ax2.annotate(s, xy=(x,y), xytext=(-15,5), textcoords='offset points', fontsize=fssml)
ax2.annotate('Mild', xy=(-4.5,-9), fontsize=fssml, color = sevCol[0])
ax2.annotate('Severe', xy=(8,8.5), fontsize=fssml, color = sevCol[1])
ax2.set_ylabel(r'medical claims ($\overline{\rho_{s,w}}$)', fontsize=fs)
ax2.set_xlabel(r'ILINet ($\overline{\rho_{s,w}^{cdc}}$)', fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-5,10])
ax2.set_ylim([-10,10])
plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures/zRR_SDI_ILINet_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# updated 10/8/15 
print 'retro - SDI/ILINet', scipy.stats.pearsonr(SDI_retro, ILINet_retro) # R = 0.775, p-value = 0.024
print 'early - SDI/ILINet', scipy.stats.pearsonr(SDI_early, ILINet_early) # Nan

