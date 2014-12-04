#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 11/11/14
###Function: mean peak-based retro zRR metric vs. hospitalization rate and P&I mortality perc with best fit lines (ILINet)

###Import data: Py_export/SDI_nat_classif_covCareAdj_v5_7.csv, 

###Command Line: python ILINet_zRR_hospMort_nat_v5.py
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
sevin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/ILINet_nat_classif_covCareAdj_7.csv','r')
sevin.readline() # remove header
sev = csv.reader(sevin, delimiter=',')
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
colorvec = ['#00ced1', '#d8b365', '#af8dc3'] # ILINet, hosp, pi_mort

### program ###

## import severity index ##
d_nat_classif = fxn.readNationalClassifFile(sev)
d_factors = factors_import(cdc)

# plot values
retrozOR = [d_nat_classif[s][0] for s in ps]
earlyzOR = [d_nat_classif[s][1] for s in ps]
pk_ili_prop = [d_factors[s][0]*100 for s in ps]
hosp_tot = [d_factors[s][1] for s in ps][6:]
pi_mort = [d_factors[s][2]*100for s in ps][2:]

# setup for best fit lines
Ifit = np.polyfit(retrozOR, pk_ili_prop, 1)
Hfit = np.polyfit(retrozOR[6:], hosp_tot, 1)
Pfit = np.polyfit(retrozOR[2:], pi_mort, 1)
Ifit_fn = np.poly1d(Ifit)
Hfit_fn = np.poly1d(Hfit)
Pfit_fn = np.poly1d(Pfit)
print 'ILI', Ifit_fn
print 'hosp', Hfit_fn
print 'PI mort', Pfit_fn

# draw plots
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
ax2 = ax1.twinx()
# # mean retro zOR vs. metrics
# ili, = ax1.plot(retrozOR, ili_prop, marker = 'o', color = colorvec[0], linestyle = 'None', ms=msz)
# pi, = ax1.plot(retrozOR, pi_mort, marker = 'o', color = colorvec[2], linestyle = 'None', ms=msz)
# hosp, = ax2.plot(retrozOR, hosp_tot, marker = 'o', color = colorvec[1], linestyle = 'None', ms=msz)

# best fit lines
ax1.plot(retrozOR, pk_ili_prop, 'o', retrozOR, Ifit_fn(retrozOR), '-', color = colorvec[0], lw = lwd)
ax1.plot(retrozOR[2:], pi_mort, 'o', retrozOR[2:], Pfit_fn(retrozOR[2:]), '-', color = colorvec[2], lw = lwd)
ax2.plot(retrozOR[6:], hosp_tot, 'o', retrozOR[6:], Hfit_fn(retrozOR[6:]), '-', color = colorvec[1], lw = lwd)

# ili and P&I axis
ax1.set_ylabel('Percent (%)', fontsize=fs) 
ax1.set_xlabel(fxn.gp_sigma_r, fontsize=fs)
ax1.tick_params(axis='both', labelsize=fssml)
ax1.set_xlim([-5,20])
ax1.set_ylim([0,10])
# hospitalization axis
ax2.set_ylabel('Rate Per 100,000', fontsize=fs) 
ax2.set_ylim([0,45])
ax2.tick_params(axis='both', labelsize=fssml)

# handles for legend formatting
Pformat, = ax2.plot([], [], color = colorvec[2], linestyle = '-', lw = lwd, label = 'P&I / All-Cause Mort. (%)')
Iformat, = ax2.plot([], [], color = colorvec[0], linestyle = '-', lw = lwd, label = 'Peak ILI / Visits (%)')
Hformat, = ax2.plot([], [], color = colorvec[1], linestyle = '-', lw = lwd, label = 'Cum. Hosp. Rate')

ax2.legend(loc='lower right')

plt.savefig('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/ILINet/ILINet_hospMort_zRR_nat.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()
# plt.show()

print 'ili_prop corr coef', np.corrcoef(pk_ili_prop, retrozOR) # 0.275
print 'hosp_tot corr coef', np.corrcoef(hosp_tot, retrozOR[6:]) # 0.696
print 'pi_mort corr coef', np.corrcoef(pi_mort, retrozOR[2:]) # -0.022
