#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/24/14
###Function: mean zOR retrospective classification vs. % H3 isolates of all subtyped isolates that season

###Import data: SQL_export/OR_allweeks_outpatient.csv, SQL_export/subtype5.csv, SQL_export/totalpop.csv

###Command Line: python Supp_zOR_H3.py
##############################################


### notes ###
# subtype5.csv: season, season yrs, subtype, subtype marker, H1 isolates, H3 isolates, B isolates, total isolates, H1 match, H3 match, B match, total match
# prominent subtype marker: 1 = H1; 2 = H1 & B; 3 = H1 & H3 & B; 4 = H3 & B; 5 = H3
# dominant subtype marker: 1 = H1 plurality; 2 = H3 plurality; 3 = B plurality
# (H1, H3, B, TOT) isolates: Number of isolates collected that season
# (H1, H3, B, TOT) match: Number of isolates collected that season that match the vaccine strains (H1, H3, B, trivalent vax in general)

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##
import functions as fxn

### data structures ###


# d_retrozOR[seasonnum] = mean zOR during relative classification period
# d_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
d_zOR = {}


### functions ###






### import data ###
incidin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks_outpatient.csv','r')
incid = csv.reader(incidin, delimiter=',')

popin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/totalpop_age.csv', 'r')
pop = csv.reader(popin, delimiter=',')

subvaxin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype5.csv', 'r')
subvax = csv.reader(subvaxin, delimiter=',')



### plotting parameters ###
snums = xrange(2, 11)

### program ###
# import data
d_H3 = fxn.season_H3perc(subvax)






# draw plots
sevix = [d_ix[s] for s in snums]
sevix_veff = [d_ix[s] for s in vaxeffT_seas]

# CDC index vs. trivalent vax strain match 
trivax = [d_vaxmatch[s][3] for s in snums]
plt.plot(trivax, sevix, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(snums, trivax, sevix):
	plt.annotate(s, xy=(x, y), xytext=(-7,5), textcoords='offset points', fontsize=16)
plt.ylabel('Benchmark index', fontsize=24)
plt.xlabel('Trivalent vaccine strain match (%)', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlim([0, 100])
plt.show()






















