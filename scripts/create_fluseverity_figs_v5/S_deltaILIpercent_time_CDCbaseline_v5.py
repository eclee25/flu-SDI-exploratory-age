#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/25/15
###Function: time series difference in ILI percentage from CDC-based ILI baseline calculation

###Import data: SQL_export/OR_allweeks_outpatient.csv, anydiag_allweeks_outpatient.csv

###Command Line: python S_deltaILIpercent_time_CDCbaseline_v5.py
##############################################

### notes ###
# Baseline is mean percentage of patient ILI visits during non-flu weeks for the previous 3 seasons plus 2 standard deviations. A non-flu week is a period of 2+ consecutive weeks where flu was <2% of the total number of specimens lab-confirmed for flu. (cdc.gov/flu/weekly/overview.htm)


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
code = 'cdc'
d_cdcILIpercent53ls = fxn.ILIpercent_processing_CDCbaseline(d_wk, d_ILIpercent)

# plot delta ILI percent time series
for s in ps:
	plt.plot(xrange(53), d_cdcILIpercent53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.hlines([0], 0, 55, colors='k', linestyles='solid', linewidth=3)
plt.xlim([0, 52])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('delta ILI perc (ref %s)' % (code), fontsize=fs)
plt.legend(loc='upper right', prop={'size':10})
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/new_baseline_definition/deltaILIpercent_time_ref%s.png' %(code), transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()
