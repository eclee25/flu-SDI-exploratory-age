#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/29/14
###Function: Draw mean retro zOR vs. region, all seasons together and stratified by mild, moderate, and severe

###Import data: R_export/OR_zip3_week_outpatient_cl.csv, R_export/allpopstat_zip3_season_cl.csv
#### These data were cleaned with data_extraction/clean_OR_hhsreg_week_outpatient.R and exported with OR_zip3_week.sql
#### allpopstat_zip3_season_cl.csv includes child, adult, and other populations; popstat_zip3_season_cl.csv includes only child and adult populations

###Command Line: python F4_zOR_region.py
##############################################


### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions as fxn

### data structures ###
### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
reg = fxn.gp_plotting_regions
reg_lab = fxn.gp_regions
mild = fxn.gp_mild  # mild season numbers
mod = fxn.gp_mod # moderate season numbers
sev = fxn.gp_sev # severe seasons numbers
sevvec = fxn.gp_severitylabels # mild, moderate, severe
sevcol = fxn.gp_severitycolors
fs = 24
fssml = 16

### functions ###
### data files ###
# regional files
reg_incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/OR_zip3_week_outpatient_cl.csv', 'r')
reg_incidin.readline()
regincid = csv.reader(reg_incidin, delimiter=',')
reg_popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export/allpopstat_zip3_season_cl.csv','r')
reg_popin.readline()
regpop = csv.reader(reg_popin, delimiter=',')
# national files
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

### program ###
# import data
# d_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR_reg = fxn.classif_zOR_region_processing(incid, pop, thanks, regincid, regpop)

# average retro zOR for all seasons
retrozOR_by_region = [[d_classifzOR_reg[(s, r)] for s in ps] for r in reg]
plt.boxplot(retrozOR_by_region)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlim([0.5, 10.5])
plt.ylim([-10, 15])
plt.xticks(xrange(1, 11), reg_lab, rotation = 'vertical', fontsize=fssml)
plt.subplots_adjust(bottom = 0.3)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F4/zOR_region.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

# average zOR and sd vs. region for mild, moderate & severe seasons
# values
avg_zOR_mild = [np.mean([d_classifzOR_reg[(s, r)] for s in mild]) for r in reg]
avg_zOR_mod = [np.mean([d_classifzOR_reg[(s, r)] for s in mod]) for r in reg]
avg_zOR_sev = [np.mean([d_classifzOR_reg[(s, r)] for s in sev]) for r in reg]
sd_zOR_mild = [np.std([d_classifzOR_reg[(s, r)] for s in mild]) for r in reg]
sd_zOR_mod = [np.std([d_classifzOR_reg[(s, r)] for s in mod]) for r in reg]
sd_zOR_sev = [np.std([d_classifzOR_reg[(s, r)] for s in sev]) for r in reg]

plt.errorbar([r-0.15 for r in reg], avg_zOR_mild, label = sevvec[0], yerr = sd_zOR_mild, color = sevcol[0], fmt = 'o')
plt.errorbar([r for r in reg], avg_zOR_mod, label = sevvec[1], yerr = sd_zOR_mild, color = sevcol[1], fmt = 'o')
plt.errorbar([r+0.15 for r in reg], avg_zOR_sev, label = sevvec[2], yerr = sd_zOR_mild, color = sevcol[2], fmt = 'o')
plt.hlines(-1, 0.5, 10.5, linestyles = 'solid')
plt.hlines(1, 0.5, 10.5, linestyles = 'solid')
plt.ylabel('Mean Retrospective z-OR', fontsize=fs)
plt.ylim([-10, 15])
plt.xlim([0.5, 10.5])
plt.xticks(reg, reg_lab, rotation = 'vertical', fontsize=fssml)
plt.legend(loc = 'upper left')
plt.subplots_adjust(bottom = 0.3)
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F4/zOR_region_stype.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


