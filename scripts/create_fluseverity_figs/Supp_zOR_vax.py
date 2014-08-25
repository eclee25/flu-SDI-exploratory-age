#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 8/25/14
###Function: scatter plot zOR metrics vs. trivalent vaccine match and vaccine efficacy at national level

###Import data: Py_export/SDI_national_classifications.csv, SQL_export/subtype5.csv

###Command Line: python Supp_zOR_vax.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt


## local modules ##
import functions as fxn

### data structures ###


### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16
fw = fxn.gp_fluweeks
wklab = fxn.gp_weeklabels

### functions ###

### data files ###
zORin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_national_classifications.csv','r')
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
earlyzOR = [d_nat_classif[s][1] for s in ps]
vaxmatch = [d_vaxmatch[s]*100 for s in ps]
vaxeffic = [d_vaxeffic[s] for s in ps]

# mean retro zOR vs vaccine match
plt.plot(vaxmatch, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, vaxmatch, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Trivalent Vaccine Match (%)', fontsize=fs)
plt.xlim([0,100])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_vax/zOR_vaxmatch.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()


# mean retro zOR vs vaccine efficacy
plt.plot(vaxeffic, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, vaxeffic, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('TIV/LAIV Weighted Vaccine Efficacy (%)', fontsize=fs)
plt.xlim([0,100])
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_vax/zOR_vaxeffic.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

