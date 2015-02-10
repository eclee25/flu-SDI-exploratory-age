#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/11/14
###Function: Any diagnosis per 100,000 population vs. week number for flu weeks (wks 40-20). Population size is from the calendar year of the week of calculation.

###Import data: SQL_export/anydiag_outpatient_allweeks.csv
### branch from v2/Supp_anydiag_time.py

###Command Line: python WIPS_anydiag_time.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v5 as fxn

### data structures ###

### functions ###
### data files ###
anydiagin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient.csv','r')
anydiagin.readline() # rm header
anydiag = csv.reader(anydiagin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
fs = 24
fssml = 16

### program ###

# dict_wk[week] = seasonnum, dict_any[week] = visits per 100,000 in US population in calendar year of week,d_any53ls[seasonnum] = [anydiag wk 40 per 100000, anydiag wk 41 per 100000,...]
d_wk, d_any, d_any53ls = fxn.week_anydiag_processing(anydiag)

# plot values
for s in ps:
	plt.plot(xrange(53), d_any53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.fill([7, 8, 8, 7], [0, 0, 4000, 4000], facecolor='grey', alpha=0.4)
plt.fill([12, 14, 14, 12], [0, 0, 4000, 4000], facecolor='grey', alpha=0.4)
plt.xlim([0, fw-1])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.ylim([0, 4000])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('Outpatient Visit per 100,000', fontsize=fs)
plt.legend(loc='upper right')
plt.savefig('/home/elee/Dropbox/Department/Presentations/2015_WIPS/Figures/anydiag_time.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()




