 #!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/4/14
###Function: child and adult incidence per 100,000 over time in an example mild, moderate, and severe season.
#### Compare the relative contributions of adult and child incidence during that season

###Import data: OR_allweeks_outpatient.csv, totalpop_age.csv

###Command Line: python F6_incid_time_CA_mildmodsev.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions as fxn

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
mk = 'o'
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

# d_wk[week] = seasonnum, d_incid[wk] = (child incid per 100,000, adult incid per 100,000, other incid per 100,000)
d_wk, d_incid = fxn.week_incidCA_processing(incid, pop)
# dict_incidCA_norm[seasonnum] = [norm child incid wk40, norm child incid wk41, ...], dict_incidA_norm[seasonnum] = [norm adult incid wk40, norm adult incid wk 41, ...]
d_incidC_norm, d_incidA_norm = fxn.normalize_incidCA(d_wk, d_incid)

# initialize figure
fig = plt.figure()

# initialize subplot
ax = fig.add_subplot(1,1,1) # one row, one column, first plot

for s, c, lab in zip(pltseas, cols, plt_labs):
	# wkdummy will represent list of weeks for chart in season to use as key
	# wkdummy needs to be sorted bc dict values don't have order when pulling dict values in list comprehension
	wkdummy = [key for key in sorted(d_wk) if d_wk[key] == int(s)]

	# for seasons with 53 weeks (season 5 only)
	if len(wkdummy) == 53:
		
		## incidence y-axis (one line each for child and adult AR)
		c_AR = [d_incid[wk][0] for wk in wkdummy]
		a_AR = [d_incid[wk][1] for wk in wkdummy]

	# for seasons with 52 weeks
	else: 
		c_AR = [d_incid[wk][0] for wk in wkdummy]
		a_AR = [d_incid[wk][1] for wk in wkdummy]
		avgc = (c_AR[12] + c_AR[13])/2
		avga = (a_AR[12] + a_AR[13])/2
		c_AR.insert(13, avgc)
		a_AR.insert(13, avga)

	chartwks = xrange(len(c_AR))
		
	child, = ax.plot(chartwks, c_AR, color = c, label = s_lab[s-2] + ', ' + lab, lw = lwd, ms = msz, linestyle = lnsty[0], marker = mk)
	adult, = ax.plot(chartwks, a_AR, color = c, lw = lwd, ms = msz, linestyle = lnsty[1], marker = mk)

# ## normalized version ##
# for s, c, lab in zip(pltseas, cols, plt_labs):
# 	# wkdummy will represent list of weeks for chart in season to use as key
# 	# wkdummy needs to be sorted bc dict values don't have order when pulling dict values in list comprehension
# 	wkdummy = [key for key in sorted(d_wk) if d_wk[key] == int(s)]

# 	# for seasons with 53 weeks (season 5 only)
# 	if len(wkdummy) == 53:
		
# 		## incidence y-axis (one line each for child and adult AR)
# 		c_AR = d_incidC_norm[s]
# 		a_AR = d_incidA_norm[s]

# 	# for seasons with 52 weeks
# 	else: 
# 		c_AR = d_incidC_norm[s]
# 		a_AR = d_incidA_norm[s]
# 		avgc = (c_AR[12] + c_AR[13])/2
# 		avga = (a_AR[12] + a_AR[13])/2
# 		c_AR.insert(13, avgc)
# 		a_AR.insert(13, avga)

# 	chartwks = xrange(len(c_AR))
		
# 	child, = ax.plot(chartwks, c_AR, color = c, label = s_lab[s-2] + ', ' + lab, lw = lwd, ms = msz, linestyle = lnsty[0], marker = mk)
# 	adult, = ax.plot(chartwks, a_AR, color = c, lw = lwd, ms = msz, linestyle = lnsty[1], marker = mk)

## designate legend/title labels
ax.legend(loc = 'upper left')
ax.set_ylabel('Incidence per 100,000', fontsize=fs)

## plot settings
plt.gca().xaxis.set_major_locator(plt.NullLocator()) # hide xticks and xlabels
plt.xticks(range(fw)[::5], wklab[:fw:5]) 
ax.set_xlabel('Week Number', fontsize=fs)
plt.xlim([0, fw-1])


# save figure
plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F6/F6_incidCA_nonnorm_singpanel.png' , transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()







