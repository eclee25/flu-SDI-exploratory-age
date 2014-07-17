#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/17/14
###Function: Return the cumulative percentage of incidence that has accrued by the retrospective and early warning severity classification periods for each season. The average percentage (or something like this) will be used to select the simulation tsteps that compose the retrospective OR classifications for the simulations. Effectively, we are scaling the simulation epidemics to the empirical epidemics.

###Import data: 

###Command Line: python cum_incid_classif_periods.py
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

## local modules ##
sys.path.append('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/create_fluseverity_figs')
import functions as fxn

### data structures ###


### parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks

### functions ###

### import data ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')
thanksin=open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
thanksin.readline() # remove header
thanks=csv.reader(thanksin, delimiter=',')

### program ###

# dict_wk[week] = seasonnum, dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
d_wk, d_incid, d_OR = fxn.week_OR_processing(incid, pop)
d_zOR = fxn.week_zOR_processing(d_wk, d_OR)
# d_incid53ls[seasonnum] = [ILI wk 40 per 100000, ILI wk 41 per 100000,...], d_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], d_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
d_incid53ls, d_OR53ls, d_zOR53ls = fxn.week_plotting_dicts(d_wk, d_incid, d_OR, d_zOR)

# d_cum_incid_retro[snum] = [% of infections accumulated by 1st wk of retro period, ..2nd wk of retro period]
d_cum_incid_retro, d_cum_incid_early = defaultdict(list), defaultdict(list)

d_Thanksgiving = fxn.Thanksgiving_import(thanks)

for s in ps:
	d_cum_incid_retro[s], d_cum_incid_early[s] = fxn.cum_incid_at_classif(d_wk, d_incid53ls, d_Thanksgiving, s)

	print 'retro', s, d_cum_incid_retro[s]
	print 'early', s, d_cum_incid_early[s]

# return average start and end cumulative incidence percentages for the retrospective period weeks (~39-45%)
print np.mean([d_cum_incid_retro[s][0] for s in ps])
print np.mean([d_cum_incid_retro[s][1] for s in ps])