#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 1/9/15
###Function: mean peak-based retro zRR metric vs. excess P&I mortality rate with best fit lines at state level for good "sentinel" states, severe states, and mildish states

###Import data: Py_export/SDI_st_classif_covCareAdj_v5_7.csv

###Command Line: python S_zRR_excessMort_st_sentinels_v5.py
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
colorvec = fxn.gp_colors
sentinels = ['LA', 'IL']
severes = ['PA', 'MD', 'VA', 'NC', 'SC', 'FL']
mildishs = ['CA', 'OR', 'WA']

### program ###

## import severity index ##
d_st_classif = fxn.readStateClassifFile(stix)
# grab list of unique keys in dataset
plot_keys = [key for key in sorted(d_st_classif) if not np.isnan(d_st_classif[key][0])] # rm nan

## import excess P&I mortality rates ##
d_st_excessPI = fxn.excessPI_state_import()

## plot sentinels ##
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
for st, col in zip(sentinels, colorvec[:len(sentinels)]):
	mask_keys = [key for key in plot_keys if key[1] == st]
	retrozOR = [d_st_classif[key][0] for key in mask_keys]
	excessPI = [d_st_excessPI[key][0] for key in mask_keys]
	excessPI_detrended = [d_st_excessPI[key][1] for key in mask_keys]

	print '%s excess PI corr coef' %(st), np.corrcoef(excessPI, retrozOR) # LA=0.41, IL=0.41
	print '%s detrended excess PI corr coef' %(st), np.corrcoef(excessPI_detrended, retrozOR) # LA=0.45, IL=0.45

	# setup for best fit line
	Efit = np.polyfit(retrozOR, excessPI, 1)
	Efit_fn = np.poly1d(Efit)
	print '%s excess PI mort rate' %(st), Efit_fn

	# best fit line
	ax1.plot(retrozOR, excessPI, 'o', retrozOR, Efit_fn(retrozOR), '-', color=col, lw=lwd)
	ax1.plot([],[], color=col, linestyle='-', lw=lwd, label=st)

# delineate mild, moderate severe
ax1.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax1.annotate('Mild', xy=(-14.5,0.25), fontsize=fssml)
ax1.annotate('Severe', xy=(11,15), fontsize=fssml)

# ili and P&I axis
ax1.set_ylabel('Excess P&I Mort. per 100,000', fontsize=fs) 
ax1.set_xlabel(fxn.gp_sigma_r, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-15,15])
ax1.set_ylim([-2, 16])

ax1.legend(loc=2)

plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/S_eMort_zRR_sentinels.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

##############################
## plot severes ##
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
for st, col in zip(severes, colorvec[:len(severes)]):
	mask_keys = [key for key in plot_keys if key[1] == st]
	retrozOR = [d_st_classif[key][0] for key in mask_keys]
	excessPI = [d_st_excessPI[key][0] for key in mask_keys]
	excessPI_detrended = [d_st_excessPI[key][1] for key in mask_keys]

	print '%s excess PI corr coef' %(st), np.corrcoef(excessPI, retrozOR) # 
	print '%s detrended excess PI corr coef' %(st), np.corrcoef(excessPI_detrended, retrozOR) # 

	# setup for best fit line
	Efit = np.polyfit(retrozOR, excessPI, 1)
	Efit_fn = np.poly1d(Efit)
	print '%s excess PI mort rate' %(st), Efit_fn

	# best fit line
	ax2.plot(retrozOR, excessPI, 'o', retrozOR, Efit_fn(retrozOR), '-', color=col, lw=lwd)
	ax2.plot([],[], color=col, linestyle='-', lw=lwd, label=st)

# delineate mild, moderate severe
ax2.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax2.annotate('Mild', xy=(-14.5,0.25), fontsize=fssml)
ax2.annotate('Severe', xy=(11,15), fontsize=fssml)

# ili and P&I axis
ax2.set_ylabel('Excess P&I Mort. per 100,000', fontsize=fs) 
ax2.set_xlabel(fxn.gp_sigma_r, fontsize=fs)
ax2.tick_params(axis='both', labelsize=fssml)
ax2.set_xlim([-15,15])
ax2.set_ylim([-2, 16])

ax2.legend(loc=2)

plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/S_eMort_zRR_severes.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

##############################
## plot milds ##
fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)
for st, col in zip(mildishs, colorvec[:len(mildishs)]):
	mask_keys = [key for key in plot_keys if key[1] == st]
	retrozOR = [d_st_classif[key][0] for key in mask_keys]
	excessPI = [d_st_excessPI[key][0] for key in mask_keys]
	excessPI_detrended = [d_st_excessPI[key][1] for key in mask_keys]

	print '%s excess PI corr coef' %(st), np.corrcoef(excessPI, retrozOR) # 
	print '%s detrended excess PI corr coef' %(st), np.corrcoef(excessPI_detrended, retrozOR) # 

	# setup for best fit line
	Efit = np.polyfit(retrozOR, excessPI, 1)
	Efit_fn = np.poly1d(Efit)
	print '%s excess PI mort rate' %(st), Efit_fn

	# best fit line
	ax3.plot(retrozOR, excessPI, 'o', retrozOR, Efit_fn(retrozOR), '-', color=col, lw=lwd)
	ax3.plot([],[], color=col, linestyle='-', lw=lwd, label=st)

# delineate mild, moderate severe
ax3.vlines([-1, 1], -20, 20, colors='k', linestyles='solid')
ax3.annotate('Mild', xy=(-14.5,0.25), fontsize=fssml)
ax3.annotate('Severe', xy=(11,15), fontsize=fssml)

# ili and P&I axis
ax3.set_ylabel('Excess P&I Mort. per 100,000', fontsize=fs) 
ax3.set_xlabel(fxn.gp_sigma_r, fontsize=fs)
ax3.tick_params(axis='both', labelsize=fssml)
ax3.set_xlim([-15,15])
ax3.set_ylim([-2, 16])

ax3.legend(loc=2)

plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/exploratory/S_eMort_zRR_mildishs.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()