#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/11/14
###Function: mean peak-based retro zRR metric vs. hospitalization rate, P&I mortality perc, and excess mortality rate with best fit lines
# 1/13/15 add excess mortality rates
# 7/20/15: update notation
# 10/8/15: rm vert lines, p-values

###Import data: Py_export/SDI_nat_classif_covCareAdj_v5_7.csv, 

###Command Line: python F_zRR_hospMort_nat_v5.py
##############################################


### notes ###


### packages/modules ###
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

## local modules ##
import functions_v5 as fxn

### functions ###
def factors_import(csvreadfile):
	''' Import CDC_Source/Import_Data/cdc_severity_measures_hospMort_nat.csv, which includes the raw data used to create the benchmark index that pairs with the SDI severity index and some additional components.
	dict_factors[season] = (proportion of patients with ILI during peak week, cumulative season hospitalization rate, proportion of total mortality due to P&I across the season)
	Modified from "benchmark_factors_import"
	'''

	dict_factors = {}
	for row in csvreadfile:
		row2 = [float('nan') if item == 'NA' else item for item in row]
		season = int(row2[0])
		# 12/4/14: changed to peak ILI week proportion
		pi_mort, pk_ili_prop, hosp_tot = float(row2[2]), float(row2[9]), float(row2[7])
		dict_factors[season] = (pk_ili_prop, hosp_tot, pi_mort)

	return dict_factors

### data files ###
natixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_nat_classif_covCareAdj_v5_7.csv', 'r')
natixin.readline() # remove header
natix = csv.reader(natixin, delimiter=',')
cdcin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_measures_hospMort_nat.csv', 'r')
cdcin.readline() # rm header
cdc = csv.reader(cdcin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
sl = fxn.gp_seasonlabels
fw = fxn.gp_fluweeks
fs = 24
fssml = 16
lwd = fxn.gp_linewidth
msz = 6
colorvec = ['#00ced1', '#d8b365', '#af8dc3', '#60178b'] # ILINet, hosp, pi_mort, ex_pi_mort

### program ###

# import severity index
d_nat_classif = fxn.readNationalClassifFile(natix)
# import hosp rate, peak ili proportion, total p&i mortality
d_factors = factors_import(cdc)
# import state-level excess p&i mortality
d_st_excessPI, d_st_pop = fxn.excessPI_state_import()
# take the weighted average of state-level excess p&i to get the national level data
d_nat_excessPI = fxn.weightAvg_excessPI_state(d_st_excessPI, d_st_pop)

# plot values
retrozOR = [d_nat_classif[s][0] for s in ps]
earlyzOR = [d_nat_classif[s][1] for s in ps]
pk_ili_prop = [d_factors[s][0]*100 for s in ps]
hosp_tot = [d_factors[s][1] for s in ps][2:]
pi_mort = [d_factors[s][2]*100 for s in ps]
ex_pi_mort = [d_nat_excessPI[s][0] for s in ps]

# setup for best fit lines
Ifit = np.polyfit(retrozOR, pk_ili_prop, 1)
Hfit = np.polyfit(retrozOR[2:], hosp_tot, 1)
Pfit = np.polyfit(retrozOR, pi_mort, 1)
Efit = np.polyfit(retrozOR, ex_pi_mort, 1)
Ifit_fn = np.poly1d(Ifit)
Hfit_fn = np.poly1d(Hfit)
Pfit_fn = np.poly1d(Pfit)
Efit_fn = np.poly1d(Efit)
print 'ILI', Ifit_fn
print 'hosp', Hfit_fn
print 'PI mort', Pfit_fn
print 'Excess PI mort', Efit_fn

# draw plots
fig1 = plt.figure()
ax2 = fig1.add_subplot(1,1,1)
ax1 = ax2.twinx()

# best fit lines
ax1.plot(retrozOR, pk_ili_prop, 'o', retrozOR, Ifit_fn(retrozOR), '-', color = colorvec[0], lw = lwd)
# ax1.plot(retrozOR, pi_mort, 'o', retrozOR, Pfit_fn(retrozOR), '-', color = colorvec[2], lw = lwd)
ax2.plot(retrozOR[2:], hosp_tot, 'o', retrozOR[2:], Hfit_fn(retrozOR[2:]), '-', color = colorvec[1], lw = lwd)
ax2.plot(retrozOR, ex_pi_mort, 'o', retrozOR, Efit_fn(retrozOR), '-', color = colorvec[3], lw = lwd)
ax1.annotate('Mild', xy=(-14.5,0.25), fontsize=fssml)
ax1.annotate('Severe', xy=(11,6.5), fontsize=fssml)

# ili and P&I axis
ax1.set_ylabel('Percent (%)', fontsize=fs) 
ax2.set_xlabel(fxn.gp_sigma_r, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-15,18])
ax1.set_ylim([0,7])
# hospitalization axis
ax2.set_ylabel('Rate per 100,000', fontsize=fs) 
ax2.set_ylim([0,45])
ax2.tick_params(axis='both', labelsize=fssml)

# handles for legend formatting
# Pformat, = ax2.plot([],[], color = colorvec[2], linestyle = '-', lw = lwd, label = 'P&I / All-Cause Mort. (%)')
Iformat, = ax2.plot([],[], color = colorvec[0], linestyle = '-', lw = lwd, label = 'Peak ILI / Visits (%)')
Hformat, = ax2.plot([],[], color = colorvec[1], linestyle = '-', lw = lwd, label = 'Cum. Hosp. Rate')
Eformat, = ax2.plot([],[], color = colorvec[3], linestyle = '-', lw = lwd, label = 'Excess P&I Mort. Rate')

ax2.legend(loc=2, prop={'size':12})

plt.savefig('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/MainFigures/hospMort_zRR_nat.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

# updated 10/8/15
print 'pk_ili_prop corr coef', scipy.stats.pearsonr(pk_ili_prop, retrozOR) # R = 0.681, p-value = 0.063
print 'hosp_tot corr coef', scipy.stats.pearsonr(hosp_tot, retrozOR[2:]) # R = 0.591 w/o first two seasons, p-value = 0.217
print 'pi_mort corr coef', scipy.stats.pearsonr(pi_mort, retrozOR) # R = 0.573, p-value = 0.137
print 'ex_pi_mort corr coef', scipy.stats.pearsonr(ex_pi_mort, retrozOR) # R = 0.535 (weightAvg_excessPI_state), p-value = 0.172
