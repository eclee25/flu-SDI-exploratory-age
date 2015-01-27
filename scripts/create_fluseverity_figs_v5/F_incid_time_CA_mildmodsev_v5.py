 #!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14
###Function: child and adult incidence per 100,000 over time in an example mild, moderate, and severe season.
#### Compare the relative contributions of adult and child incidence during that season
# 10/31 coverage adjustment no longer age-specific


###Import data: OR_allweeks_outpatient.csv, totalpop_age.csv

###Command Line: python F_incid_time_CA_mildmodsev_v5.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions_v5 as fxn

### data structures ###

### called/local plotting parameters ###
mild_s = fxn.gp_mild
mod_s = fxn.gp_mod
sev_s = fxn.gp_sev
fw = fxn.gp_fluweeks
fs = 24
fssml = 16
lwd = 3
msz = 6
lnsty = fxn.gp_line_style
cols = fxn.gp_severitycolors
s_lab = fxn.gp_seasonlabels
wklab = fxn.gp_weeklabels
plt_labs = fxn.gp_severitylabels

pltseas = [mild_s[0], mod_s[0], sev_s[1]] # plot only one example of each type of seasons

### functions ###

### import data ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

# d_wk[week] = seasonnum, dict_ageIncidAdjust53ls[(season, age)] = [adj incid per 100000 wk 40, ... wk 39]
d_wk, d_ageIncidAdjust53ls = fxn.week_incidCA_processing(incid, pop)

# initialize figure
fig = plt.figure()

# initialize subplot
ax = fig.add_subplot(1,1,1) # one row, one column, first plot

for s, c, lab in zip(pltseas, cols, plt_labs):
	# adjusted incidence version
	c_incid = d_ageIncidAdjust53ls[(s, 'C')][:fw]
	a_incid = d_ageIncidAdjust53ls[(s, 'A')][:fw]
		
	child, = ax.plot(xrange(fw), c_incid, color = c, label = s_lab[s-2] + ', ' + lab, lw = lwd, ms = msz, linestyle = lnsty[0], marker = fxn.gp_marker)
	adult, = ax.plot(xrange(fw), a_incid, color = c, lw = lwd, ms = msz, linestyle = lnsty[1], marker = fxn.gp_marker)

# handles for child and adult line formatting
Cformat, = ax.plot([], [], color = 'grey', linestyle = lnsty[0], lw = lwd, ms = msz, marker = fxn.gp_marker, label = 'children')
Aformat, = ax.plot([], [], color = 'grey', linestyle = lnsty[1], lw = lwd, ms = msz, marker = fxn.gp_marker, label = 'adults')

## designate legend/title labels
ax.legend(loc = 'upper left')
ax.set_ylabel(fxn.gp_adjILI, fontsize=fs)

## plot settings
plt.gca().xaxis.set_major_locator(plt.NullLocator()) # hide xticks and xlabels
plt.xticks(range(fw)[::5], wklab[:fw:5]) 
ax.set_xlabel('Week Number', fontsize=fs)
plt.xlim([0, fw-1])

# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/F2/incidCA_nonnorm_singpanel.png' , transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()







