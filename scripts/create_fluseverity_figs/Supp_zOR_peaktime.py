#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/31/14
###Function: scatter plot zOR metrics vs. peak week at national level

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv, My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv

###Command Line: python Supp_zOR_peaktime.py
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
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

### program ###
# import data
# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)
# d_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
d_classifzOR = fxn.classif_zOR_processing(d_wk, d_incid53ls, d_zOR53ls, thanks)

# plot values
retrozOR = [d_classifzOR[s][0] for s in ps]
earlyzOR = [d_classifzOR[s][1] for s in ps]
peakweek = [fxn.peak_flu_week_index(d_incid53ls[s]) for s in ps]
print peakweek

# mean retro zOR vs peak timing
plt.plot(peakweek, retrozOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, peakweek, retrozOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Retrospective zOR', fontsize=fs) 
plt.xlabel('Peak Week', fontsize=fs)
plt.xticks(range(fw)[::5], wklab[:fw:5], fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.show()


# mean retro zOR vs peak timing
plt.plot(peakweek, earlyzOR, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(sl, peakweek, earlyzOR):
	plt.annotate(s, xy=(x,y), xytext=(-10,5), textcoords='offset points', fontsize=fssml)
plt.ylabel('Mean Early Warning zOR', fontsize=fs) 
plt.xlabel('Peak Week', fontsize=fs)
plt.xticks(range(fw)[::5], wklab[:fw:5], fontsize=fssml)
plt.yticks(fontsize=fssml)
plt.show()

