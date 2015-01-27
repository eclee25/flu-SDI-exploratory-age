#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/9/15
###Function: mean peak-based retro zRR metric vs. hospitalization rate and P&I mortality perc with best fit lines at state level

###Import data: Py_export/SDI_st_classif_covCareAdj_v5_7.csv, Census/state_abbreviations.csv

###Command Line: python F_zRR_excessMort_st_v5.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np

## local modules ##
import functions_v5 as fxn

### data structures ###

### functions ###

### data files ###
stixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_7st.csv', 'r')
stixin.readline() # remove header
stix = csv.reader(stixin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fw = fxn.gp_fluweeks
fs = 24
fssml = 16
lwd = fxn.gp_linewidth
msz = 6
colorvec = ['#60178b'] # excess pi_mort (darker purple than pi_mort at nat level)
mild_seas = fxn.gp_mild
mod_seas = fxn.gp_mod
sev_seas = fxn.gp_sev
seas_col = fxn.gp_colors

### program ###

## import severity index ##
d_st_classif = fxn.readStateClassifFile(stix)
# grab list of unique keys in dataset
plot_keys = [key for key in sorted(d_st_classif)]
## import excess P&I mortality rates ##
d_st_excessPI = fxn.excessPI_state_import()

for s in ps:
	mask_keys = [key for key in sorted(d_st_classif) if not np.isnan(d_st_classif[key][0]) and key[0] == s] # rm nan

	# plot values
	retrozOR = [d_st_classif[key][0] for key in mask_keys]
	earlyzOR = [d_st_classif[key][1] for key in mask_keys]
	excessPI = [d_st_excessPI[key][0] for key in mask_keys]
	excessPI_detrended = [d_st_excessPI[key][1] for key in mask_keys]

	print 'excess PI corr coef', np.corrcoef(excessPI, retrozOR) # 
	print 'detrended excess PI corr coef', np.corrcoef(excessPI_detrended, retrozOR) # 

	# setup for best fit line
	Efit = np.polyfit(retrozOR, excessPI, 1)
	Efit_fn = np.poly1d(Efit)
	print 'excess PI mort rate', Efit_fn

	# draw plots
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(1,1,1)
	# best fit line
	ax1.plot(retrozOR, excessPI, 'o', retrozOR, Efit_fn(retrozOR), '-', color = seas_col[s-2], lw = lwd)

	# handles for legend formatting
	Eformat, = ax1.plot([], [], color = seas_col[s-2], linestyle = '-', lw = lwd, label = 'Season %s' %(s))

	ax1.legend(loc=2)
	# delineate mild, moderate severe
	ax1.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
	# ax1.fill([-15, -1, -1, -15], [0, 0, 10, 10], facecolor='blue', alpha=0.4)
	# ax1.fill([-1, 1, 1, -1], [0, 0, 10, 10], facecolor='yellow', alpha=0.4)
	# ax1.fill([1, 15, 15, 1], [0, 0, 10, 10], facecolor='red', alpha=0.4)
	ax1.annotate('Mild', xy=(-14.5,0.25), fontsize=fssml)
	ax1.annotate('Severe', xy=(11,15), fontsize=fssml)

	# ili and P&I axis
	ax1.set_ylabel('Rate per 100,000', fontsize=fs) 
	ax1.set_xlabel(fxn.gp_sigma_r, fontsize=fs)
	ax1.tick_params(axis='both', labelsize=fssml)
	ax1.set_xlim([-15,15])
	ax1.set_ylim([-5, 16])

	plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/F5_eMort_zRR_st_allSeas_S%s.png' %(s), transparent=False, bbox_inches='tight', pad_inches=0)
	plt.close()
# plt.show()



