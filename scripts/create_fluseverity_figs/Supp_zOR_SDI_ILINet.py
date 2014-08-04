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
plt.plot(ILINet_retro, SDI_retro, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ILINet_retro, SDI_retro):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('SDI Retrospective Severity Index', fontsize=fs)
plt.xlabel('ILINet Retrospective Severity Index', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-10,20])
plt.ylim([-10,20])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_SDI_ILINet/zOR_SDI_ILINet_retro.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# SDI vs ILINet early warning zOR
plt.plot(ILINet_early, SDI_early, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, ILINet_early, SDI_early):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('SDI Early Warning Severity Index', fontsize=fs)
plt.xlabel('ILINet Early Warning Severity Index', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([-4,8])
plt.ylim([-4,8])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_SDI_ILINet/zOR_SDI_ILINet_early.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()




