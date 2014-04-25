#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/24/14
###Function: mean zOR retrospective classification vs. % H3 isolates of all subtyped isolates that season

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/subtype5.csv, SQL_export/totalpop.csv

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
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

nrevss_subin = open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/NREVSS_Isolates_Season.csv', 'r')
nrevss_subin.readline() # remove header
nrevss_sub = csv.reader(nrevss_subin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.gp_plotting_seasons
sl = fxn.gp_seasonlabels
fs = 24
fssml = 16

### program ###
# import data
# d_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
# d_classifzOR[seasonnum] =  (mean retrospective zOR, mean early warning zOR)
d_H3cdc = fxn.season_H3perc_CDC(subvax)
d_H3nrevss = fxn.season_H3perc_NREVSS(nrevss_sub)
d_classifzOR = fxn.classif_zOR_processing(incid, pop, thanks)

# plot values
H3cdc = [d_H3cdc[s] for s in ps]
H3nrevss = [d_H3nrevss[s] for s in ps]
classifzOR = [d_classifzOR[s][0] for s in ps]

# draw plots
# figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

plt.plot(H3cdc, classifzOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3cdc, classifzOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('H3 Proportion of Subtyped Isolates (CDC)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3_cdc.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

plt.plot(H3nrevss, classifzOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, H3nrevss, classifzOR):
	plt.annotate(s, xy=(x,y), xytext=(-20,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs)
plt.xlabel('H3 Proportion of Subtyped Isolates (NREVSS)', fontsize=fs)
plt.xticks(fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.xlim([0,1])
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/zOR_H3_nrevss.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


