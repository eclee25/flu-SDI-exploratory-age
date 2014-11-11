#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/4/14
###Function: plot SDI zOR vs. ILINet zOR(supp figure)
# 11/4 v5 updates

###Import data: 


###Command Line: python S_zRR_SDI_ILINet_v5.py
##############################################


### notes ###

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###
### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

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

# draw plots
# SDI vs ILINet retrospective zOR
fig1 = plt.figure()
ax1 = plt.subplot(111)
ax1.plot(ILINet_retro, SDI_retro, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ILINet_retro, SDI_retro):
	ax1.annotate(s, xy=(x,y), xytext=(-25,-15), textcoords='offset points', fontsize=fssml)
ax1.vlines([-1, 1], -30, 30, colors='k', linestyles='solid')
ax1.hlines([-1, 1], -30, 30, colors='k', linestyles='solid')
ax1.fill([30, 1, 1, 30], [1, 1, 30, 30], facecolor='red', alpha=0.4)
ax1.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax1.fill([-30, -1, -1, -30], [-1, -1, -30, -30], facecolor='blue', alpha=0.4)
ax1.annotate('Mild', xy=(-2,-3), fontsize=fssml)
ax1.annotate('Severe', xy=(3.5,13), fontsize=fssml)
ax1.set_title(fxn.gp_sigma_r, fontsize=fs)
ax1.set_ylabel('SDI', fontsize=fs)
ax1.set_xlabel('ILINet', fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-5,5])
ax1.set_ylim([-15,15])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/zRR_SDI_ILINet_retro.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# SDI vs ILINet early warning zOR
fig2 = plt.figure()
ax2 = plt.subplot(111)
ax2.plot(ILINet_early, SDI_early, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ILINet_early, SDI_early):
	ax2.annotate(s, xy=(x,y), xytext=(-25,5), textcoords='offset points', fontsize=fssml)
ax2.vlines([-1, 1], -10, 20, colors='k', linestyles='solid')
ax2.hlines([-1, 1], -10, 20, colors='k', linestyles='solid')
ax2.fill([10, 1, 1, 10], [1, 1, 20, 20], facecolor='red', alpha=0.4)
ax2.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax2.fill([-10, -1, -1, -10], [-1, -1, -10, -10], facecolor='blue', alpha=0.4)
ax2.annotate('Mild', xy=(-2,-2), fontsize=fssml)
ax2.annotate('Severe', xy=(3.5,8.5), fontsize=fssml)
ax2.set_title(fxn.gp_sigma_w, fontsize=fs)
ax2.set_ylabel('SDI', fontsize=fs)
ax2.set_xlabel('ILINet', fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-5,5])
ax2.set_ylim([-10,10])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/Supp/zRR_SDI_ILINet_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


print 'retro - SDI/ILINet', np.corrcoef(SDI_retro, ILINet_retro) # 0.728
print 'early - SDI/ILINet', np.corrcoef(SDI_early, ILINet_early) # 0.080

