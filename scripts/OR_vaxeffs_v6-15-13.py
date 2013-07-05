#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: June 15, 2013
###Function: 1) draw charts for OR vs weighted average of vaccine effectiveness, which was calculated from data in Table 4 in Osterholm et al.
### 2) draw charts for OR vs weighted average of vax efficacy (TIV) from Table 2 in Osterholm et al.
### 3) draw charts for OR vs weighted average of vax efficacy (LAIV) from Table 3 in Osterholm et al.
### 4) draw charts for OR vs weighted average of vax efficacy (TIV & LAIV) from Tables 2 and 3 in Osterholm et al.

### Updates from 6/3/13 version
#### call ORgenerator function instead of in-script functions
#### ORs represent means of ORs normalized by age-specific zip3 popstat instead of attack rate divided by size of child and adult US populations (as did 6/3 version); import data has changed from odds_c_a1, odds_c_a3_a, odds_c_a3_b to zipcode_bysseas datasets

###Source data: 
###Vax effectiveness and efficacy: Osterholm et al. (2012) Efficacy and effectiveness of influenza vaccines: a systematic review and meta-analysis. Lancet Infectious Diseases 12: 36-44.
###OR: SDI (see odds_c_a_v4-17-13.py)

###Import data: zipcode_bysseas_cl_v6-12-13.csv

###Command Line: python OR_vaxeffs_v6-15-13.py
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import ORgenerator_v060713 as od


## local packages ##

### data structures ###
child1, adult1, y1, z3s, snum_sdi = [],[],[],[],[] # attack rates for children and adults for all cases, odds ratios for all cases, zip3s in dataset, season number code in import dataset
avgOR1, sdOR1 = [],[] # average ORs across zip3s for each season, standard deviation of ORs for each season (dispersion of zip3 ORs around the mean)


### parameters ###
# USchild = 20348657 + 20677194 + 22040343 #US child popn
# USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805

### functions ###


### import data ###
zORin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export/zipcode_bysseas_cl_v6-12-13.csv','r') # use to calculate OR by zip3
zOR=csv.reader(zORin, delimiter=',')

### program ###

# generate weighted avg of vax effectiveness data (Seasons 2003-04 to 2008-09)
seasonnum = [4, 5, 6, 7, 8, 9] # season number according to mysql codes
vaxefv_wt = [21.0, 35.2, 21.0, 50.3, 69.3, 67.0] # weighted avg of vax effectiveness in %

# 6/15 rm code that refers to milder and severe cases
od.importer_ORzip3(zOR, adult1, child1, 3, 4, z3s, 2, snum_sdi) # 6/15 changed importer function
od.ORgen_zip3mn(y1, child1, adult1, snum_sdi, avgOR1, sdOR1) # 6/15 change OR generation mechanism

# limit avgORs and sd to values for seasons listed in snum list
avgOR1_trunc = avgOR1[3:9] # correspond to seasons 4-9
sdOR1_trunc = sdOR1[3:9]

# plot vax effectiveness
plt.errorbar(vaxefv_wt, avgOR1_trunc, yerr=sdOR1_trunc, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, vaxefv_wt, avgOR1_trunc):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Vaccine Effectiveness (Weighted Avg %)')
plt.legend(loc="upper left")
ylim([2, 7])
xlim([0,100])
plt.show()


### vax efficacy TIV and LAIV ###
# generate weighted avg vax efficacy data 
seasonnum = [1, 2, 3, 5, 6, 7, 8, 9]
vaxeffT_wt = [69.1, 54.6, 64.0, 61.5, 28.1, 57.8, 60.5, 76.0]
avgOR1_effall = list(avgOR1)
del avgOR1_effall[3]
del avgOR1_effall[8]
sdOR1_effall = list(sdOR1)
del sdOR1_effall[3]
del sdOR1_effall[8]

# plot vax efficacy for weighted avg of TIV and LAIV
plt.errorbar(vaxeffT_wt, avgOR1_effall, yerr=sdOR1_effall, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, vaxeffT_wt, avgOR1_effall):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Vaccine Efficacy, TIV and LAIV (Weighted Avg %)')
plt.legend(loc="upper left")
ylim([2, 7])
xlim([0,100])
plt.show()


### vax efficacy TIV ###
seasonnum = [1, 5, 6, 7, 8, 9]
vaxefftri_wt = [-7.0, 75.0, 30.3, 57.8, 63.7, 76.0]
avgOR1_tri = list(avgOR1)
del avgOR1_tri[1:4]
del avgOR1_tri[6]
sdOR1_tri = list(sdOR1)
del sdOR1_tri[1:4]
del sdOR1_tri[6]

# plot vaccine efficacy for TIV data only
plt.errorbar(vaxefftri_wt, avgOR1_tri, yerr=sdOR1_tri, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, vaxefftri_wt, avgOR1_tri):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Vaccine Efficacy, TIV (Weighted Avg %)')
plt.legend(loc="upper left")
ylim([2, 7])
xlim([0,100])
plt.show()


### vax efficacy LAIV ###
seasonnum = [1, 2, 3, 5, 6, 8]
vaxeffLAIV_wt = [73.3, 54.6, 64.0, 48.0, 8.0, 36.0]
avgOR1_LAIV = list(avgOR1)
del avgOR1_LAIV[3]
del avgOR1_LAIV[5]
del avgOR1_LAIV[6:]
sdOR1_LAIV = list(sdOR1)
del sdOR1_LAIV[3]
del sdOR1_LAIV[5]
del sdOR1_LAIV[6:]

# plot vaccine efficacy for LAIV data only
plt.errorbar(vaxeffLAIV_wt, avgOR1_LAIV, yerr=sdOR1_LAIV, marker='o', color = 'black', label= "all cases", linestyle='None')
for num, perc, OR in zip(seasonnum, vaxeffLAIV_wt, avgOR1_LAIV):
	plt.annotate(num, xy = (perc, OR), xytext = (0,0), textcoords = 'offset points')
plt.ylabel('Odds ratio of attack rate, child:adult (zip3 popstat normalized)')
plt.xlabel('Vaccine Efficacy, LAIV (Weighted Avg %)')
plt.legend(loc="upper left")
xlim([0,100])
ylim([2, 7])
plt.show()


























