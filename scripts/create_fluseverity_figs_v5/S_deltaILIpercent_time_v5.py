#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/23/15
###Function: time series difference and cumulative difference in ILI percentage from week 40, week 36, mid-summer, and lowest summer ILI percentage vs. time

###Import data: SQL_export/OR_allweeks_outpatient.csv, anydiag_allweeks_outpatient.csv

###Command Line: python S_deltaILIpercent_time_v5.py
##############################################

### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v5 as fxn

### data structures ###
### functions ###

### data files ###
ILIin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
ILIfile = csv.reader(ILIin, delimiter=',')
visitin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient.csv', 'r')
visitin.readline() # rm header
visitfile = csv.reader(visitin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
fs = 24
fssml = 16

### program ###
# dict_wk[wk] = seasonnum
# dict_ILIpercent[Thu date of week] = ILI as percent of total visits in that week (not a cumulative measure)
# dict_deltaILIpercent53ls[s] = [deltaILI percent wk 40, wk 41, ...wk 39
# dict_refWeek[s] = date of reference week for that season
d_wk, d_ILIpercent = fxn.week_ILIpercent_processing(ILIfile, visitfile)
code = 'week40'
d_deltaILIpercent53ls, d_refWeek = fxn.deltaILIpercent_processing(d_wk, d_ILIpercent, refWeek_keyword=code)
d_cumDeltaILIpercent53ls = fxn.cumulativeDeltaILIpercent(d_wk, d_ILIpercent, d_deltaILIpercent53ls, d_refWeek)

# plot delta ILI percent time series
for s in ps:
	plt.plot(xrange(53), d_deltaILIpercent53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.xlim([0, 52])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('delta ILI perc (ref %s)' % (code), fontsize=fs)
plt.legend(loc='upper right', prop={'size':10})
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/new_baseline_definition/deltaILIpercent_time_ref%s.png' %(code), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# plot cumulative delta ILI percent time series
for s in ps:
	plt.plot(xrange(53), d_cumDeltaILIpercent53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.xlim([0, 52])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('cum delta ILI perc (ref %s)' % (code), fontsize=fs)
plt.legend(loc='lower right', prop={'size':10})
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/new_baseline_definition/cumDeltaILIpercent_time_ref%s.png' %(code), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()
