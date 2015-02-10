#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14
###Function: OR of incidence in adults to incidence in children vs. week number. Incidence in children and adults is normalized by the size of the child and adult populations in the second calendar year of the flu season. 
# 10/14/14 OR age flip.
# 10/15/14 ILI incidence ratio incorporates any diagnosis visits (obsolete)
# 10/19 incidence rate adjusted by any diagnosis visits (coverage adj = visits S9/visits S#) and ILI care-seeking behavior; change to relative risk
# 10/31 coverage adjustment no longer age-specific

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/totalpop_age.csv

###Command Line: python F_RR_time_v6.py
##############################################

### notes ###
# Incidence per 100,000 is normalized by total population by second calendar year of the flu season
### packages/modules ###
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
## local modules ##
import functions_v5 as fxn

### data structures ###
### functions ###
def week_RR_processing_otherAges(dict_pop, dict_totILI53ls, dict_totILIadj53ls, dict_ageILIadj_season):
	dict_totIncid53ls, dict_totIncidAdj53ls, dict_other_child_RR53ls, dict_adult_other_RR53ls = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
	age_keys = ['C', 'A', 'O']
	# generate adjusted incidence per 100,000 in US population, OR, and zOR at the weekly level
	for s in range(2,10):
		# total population in the season
		tot_pop = sum([dict_pop[(s, ak)] for ak in age_keys])
		# totIncid53ls dict
		dict_totIncid53ls[s] = [ili/tot_pop*100000 for ili in dict_totILI53ls[s]]
		# totIncidAdj53ls
		dict_totIncidAdj53ls[s] = [iliAdj/tot_pop*100000 for iliAdj in dict_totILIadj53ls[s]]
		# RR53ls dict
		child_attack = [adjILI/dict_pop[(s, 'C')] for adjILI in dict_ageILIadj_season[(s, 'C')]]
		adult_attack = [adjILI/dict_pop[(s, 'A')] for adjILI in dict_ageILIadj_season[(s, 'A')]]
		other_attack = [adjILI/dict_pop[(s, 'O')] for adjILI in dict_ageILIadj_season[(s, 'O')]]
		# 10/19/14: RR should not be evaluated if child or adult incidence is zero
		# 10/16/14 change OR to relative risk
		ocRR = [o/c if o and c else float('nan') for o, c in zip(other_attack, child_attack)] 
		aoRR = [a/o if a and o else float('nan') for a, o in zip(adult_attack, other_attack)] 
		dict_other_child_RR53ls[s] = ocRR
		dict_adult_other_RR53ls[s] = aoRR
	
	return dict_other_child_RR53ls, dict_adult_other_RR53ls

### data files ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')
popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

### called/local plotting parameters ###
ps = fxn.pseasons
fw = fxn.gp_fluweeks
sl = fxn.gp_seasonlabels
colvec = fxn.gp_colors
wklab = fxn.gp_weeklabels
fs = 24
fssml = 16

### program ###

d_wk, d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season = fxn.week_OR_processing(incid, pop)
d_totIncid53ls, d_totIncidAdj53ls, d_RR53ls, d_zRR53ls = fxn.week_RR_processing_part2(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)
d_ocRR53ls, d_aoRR53ls = week_RR_processing_otherAges(d_pop, d_totILI53ls, d_totILIadj53ls, d_ageILIadj_season)

# plot values
for s in ps:
	plt.plot(d_RR53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.fill([7, 8, 8, 7], [-5, -5, 5, 5], facecolor='grey', alpha=0.4)
plt.fill([12, 14, 14, 12], [-5, -5, 5, 5], facecolor='grey', alpha=0.4)
plt.xlim([0, fw])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.ylim([0,1])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('<-- child : adult -->', fontsize=fs)
plt.legend(loc='upper right', prop={'size':10})
plt.savefig('/home/elee/Dropbox/Department/Presentations/2015_WIPS/Figures/RR_time_ac.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

for s in ps:
	plt.plot(d_ocRR53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.fill([7, 8, 8, 7], [-5, -5, 5, 5], facecolor='grey', alpha=0.4)
plt.fill([12, 14, 14, 12], [-5, -5, 5, 5], facecolor='grey', alpha=0.4)
plt.xlim([0, fw])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.ylim([0.2,2.5])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('<-- child : high-risk -->', fontsize=fs)
plt.legend(loc='upper right', prop={'size':10})
plt.savefig('/home/elee/Dropbox/Department/Presentations/2015_WIPS/Figures/RR_time_oc.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()

for s in ps:
	plt.plot(d_aoRR53ls[s], marker = fxn.gp_marker, color = colvec[s-2], label = sl[s-2], linewidth = fxn.gp_linewidth)
plt.fill([7, 8, 8, 7], [-5, -5, 5, 5], facecolor='grey', alpha=0.4)
plt.fill([12, 14, 14, 12], [-5, -5, 5, 5], facecolor='grey', alpha=0.4)
plt.xlim([0, fw])
plt.xticks(range(53)[::5], wklab[::5]) 
plt.ylim([0,1])
plt.xlabel('Week Number', fontsize=fs)
plt.ylabel('<-- high-risk : adult -->', fontsize=fs)
plt.legend(loc='upper right', prop={'size':10})
plt.savefig('/home/elee/Dropbox/Department/Presentations/2015_WIPS/Figures/RR_time_ao.png', transparent=False, bbox_inches='tight', pad_inches=0)
plt.close()


