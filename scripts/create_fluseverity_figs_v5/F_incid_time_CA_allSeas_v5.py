 #!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 2/9/15
###Function: child and adult incidence per 100,000 over time in mild, moderate, and severe seasons.
#### Compare the relative contributions of adult and child incidence during that season
### One plot for each
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
fw = 53
fs = 24
fssml = 16
lwd = 3
msz = 6
lnsty = fxn.gp_line_style
cols = fxn.gp_colors
s_lab = fxn.gp_seasonlabels
wklab = fxn.gp_weeklabels
plt_labs = fxn.gp_severitylabels

### functions ###

### import data ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

d_wk, d_ageIncidAdjust53ls = fxn.week_incidCA_processing(incid, pop)

# initialize figure
fig1 = plt.figure()
#################################
# initialize subplot
ax1 = fig1.add_subplot(1,1,1) # one row, one column, first plot

for s in mild_s:
	# adjusted incidence version
	c_incid = d_ageIncidAdjust53ls[(s, 'C')][:fw]
	a_incid = d_ageIncidAdjust53ls[(s, 'A')][:fw]
		
	child, = ax1.plot(xrange(fw), c_incid, color = cols[s-2], label = s_lab[s-2], lw = lwd, ms = msz, linestyle = lnsty[0], marker = fxn.gp_marker)
	adult, = ax1.plot(xrange(fw), a_incid, color = cols[s-2], lw = lwd, ms = msz, linestyle = lnsty[1], marker = fxn.gp_marker)

# handles for child and adult line formatting
Cformat, = ax1.plot([], [], color = 'grey', linestyle = lnsty[0], lw = lwd, ms = msz, marker = fxn.gp_marker, label = 'children')
Aformat, = ax1.plot([], [], color = 'grey', linestyle = lnsty[1], lw = lwd, ms = msz, marker = fxn.gp_marker, label = 'adults')
## designate legend/title labels
ax1.legend(loc = 'upper right')
ax1.set_ylabel(fxn.gp_adjILI, fontsize=fs)
## plot settings
plt.gca().xaxis.set_major_locator(plt.NullLocator()) # hide xticks and xlabels
ax1.set_xticks(range(fw)[::5]) 
ax1.set_xticklabels(wklab[:fw:5])
ax1.set_xlabel('Week Number', fontsize=fs)
ax1.set_xlim([0, fw-1])
ax1.set_ylim([0, 300])

# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/incidCA_nonnorm_mild.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

#################################
# initialize figure
fig2 = plt.figure()
# initialize subplot
ax2 = fig2.add_subplot(1,1,1) # one row, one column, first plot

for s in mod_s:
	# adjusted incidence version
	c_incid = d_ageIncidAdjust53ls[(s, 'C')][:fw]
	a_incid = d_ageIncidAdjust53ls[(s, 'A')][:fw]
	child, = ax2.plot(xrange(fw), c_incid, color = cols[s-2], label = s_lab[s-2], lw = lwd, ms = msz, linestyle = lnsty[0], marker = fxn.gp_marker)
	adult, = ax2.plot(xrange(fw), a_incid, color = cols[s-2], lw = lwd, ms = msz, linestyle = lnsty[1], marker = fxn.gp_marker)
## designate legend/title labels
ax2.legend(loc = 'upper right')
ax2.set_ylabel(fxn.gp_adjILI, fontsize=fs)
## plot settings
plt.gca().xaxis.set_major_locator(plt.NullLocator()) # hide xticks and xlabels
ax2.set_xticks(range(fw)[::5]) 
ax2.set_xticklabels(wklab[:fw:5])
ax2.set_xlabel('Week Number', fontsize=fs)
ax2.set_xlim([0, fw-1])
ax2.set_ylim([0, 300])

# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/incidCA_nonnorm_mod.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

#################################
# initialize figure
fig3 = plt.figure()
# initialize subplot
ax3 = fig3.add_subplot(1,1,1) # one row, one column, first plot

for s in sev_s:
	# adjusted incidence version
	c_incid = d_ageIncidAdjust53ls[(s, 'C')][:fw]
	a_incid = d_ageIncidAdjust53ls[(s, 'A')][:fw]
		
	child, = ax3.plot(xrange(fw), c_incid, color = cols[s-2], label = s_lab[s-2], lw = lwd, ms = msz, linestyle = lnsty[0], marker = fxn.gp_marker)
	adult, = ax3.plot(xrange(fw), a_incid, color = cols[s-2], lw = lwd, ms = msz, linestyle = lnsty[1], marker = fxn.gp_marker)
## designate legend/title labels
ax3.legend(loc = 'upper right')
ax3.set_ylabel(fxn.gp_adjILI, fontsize=fs)
## plot settings
plt.gca().xaxis.set_major_locator(plt.NullLocator()) # hide xticks and xlabels
ax3.set_xticks(range(fw)[::5]) 
ax3.set_xticklabels(wklab[:fw:5])
ax3.set_xlabel('Week Number', fontsize=fs)
ax3.set_xlim([0, fw-1])
ax3.set_ylim([0, 300])

# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/incidCA_nonnorm_sev.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()







