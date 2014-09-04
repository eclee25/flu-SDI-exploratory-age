#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/4/14
###Function: plot SDI zOR vs. ILINet zOR(supp figure)

###Import data: 


###Command Line: python Supp_zOR_SDI_ILINet.py
##############################################


### notes ###

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###
### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### data files ###
# SDI classifications file 
SDIclassif_in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications.csv', 'r')
SDIclassif_in.readline() # remove header
SDIclassif = csv.reader(SDIclassif_in, delimiter=',')
# ILINet classifications file
ILINetclassif_in = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_national_classifications.csv', 'r')
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
print 'retro - SDI/ILINet', np.corrcoef(SDI_retro, ILINet_retro)
print 'early - SDI/ILINet', np.corrcoef(SDI_early, ILINet_early)

# draw plots
# SDI vs ILINet retrospective zOR
fig1 = plt.figure()
ax1 = plt.subplot(111)
ax1.plot(ILINet_retro, SDI_retro, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ILINet_retro, SDI_retro):
	ax1.annotate(s, xy=(x,y), xytext=(-25,-15), textcoords='offset points', fontsize=fssml)
ax1.vlines([-1, 1], -10, 20, colors='k', linestyles='solid')
ax1.hlines([-1, 1], -10, 20, colors='k', linestyles='solid')
ax1.fill([20, 1, 1, 20], [1, 1, 20, 20], facecolor='blue', alpha=0.4)
ax1.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax1.fill([-10, -1, -1, -10], [-1, -1, -10, -10], facecolor='red', alpha=0.4)
ax1.annotate('Mild', xy=(4,19), fontsize=fssml)
ax1.annotate('Severe', xy=(-6,-8.5), fontsize=fssml)
ax1.set_title(fxn.gp_sigma_r, fontsize=fs)
ax1.set_ylabel('SDI', fontsize=fs)
ax1.set_xlabel('ILINet', fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-10,20])
ax1.set_ylim([-10,20])
ax1.invert_yaxis()
ax1.invert_xaxis()
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_SDI_ILINet/zOR_SDI_ILINet_retro.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# SDI vs ILINet early warning zOR
fig2 = plt.figure()
ax2 = plt.subplot(111)
ax2.plot(ILINet_early, SDI_early, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ILINet_early, SDI_early):
	ax2.annotate(s, xy=(x,y), xytext=(-25,5), textcoords='offset points', fontsize=fssml)
ax2.vlines([-1, 1], -10, 20, colors='k', linestyles='solid')
ax2.hlines([-1, 1], -10, 20, colors='k', linestyles='solid')
# ax1.fill([20, 1, 1, 20], [1, 1, 20, 20], facecolor='blue', alpha=0.4)
# ax1.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
# ax1.fill([-10, -1, -1, -10], [-1, -1, -10, -10], facecolor='red', alpha=0.4)
ax2.fill([8, 1, 1, 8], [1, 1, 20, 20], facecolor='blue', alpha=0.4)
ax2.fill([-1, 1, 1, -1], [-1, -1, 1, 1], facecolor='yellow', alpha=0.4)
ax2.fill([-4, -1, -1, -4], [-1, -1, -10, -10], facecolor='red', alpha=0.4)
ax2.annotate('Mild', xy=(2.5, 7.5), fontsize=fssml)
ax2.annotate('Severe', xy=(-2.3,-3.3), fontsize=fssml)
ax2.set_title(fxn.gp_sigma_w, fontsize=fs)
ax2.set_ylabel('SDI', fontsize=fs)
ax2.set_xlabel('ILINet', fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-4,8])
ax2.set_ylim([-4,8])
ax2.invert_yaxis()
ax2.invert_xaxis()
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_SDI_ILINet/zOR_SDI_ILINet_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()




