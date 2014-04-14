#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 3/25/14
###Function: scatterplots of CDC severity index vs. prominent strain, vax match, vax coverage, and vax efficacy

###Import data: /home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv

###Command Line: python 
##############################################


### notes ###
# subtype5.csv: season, season yrs, subtype, subtype marker, H1 isolates, H3 isolates, B isolates, total isolates, H1 match, H3 match, B match, total match
# prominent subtype marker: 1 = H1; 2 = H1 & B; 3 = H1 & H3 & B; 4 = H3 & B; 5 = H3
# dominant subtype marker: 1 = H1 plurality; 2 = H3 plurality; 3 = B plurality
# (H1, H3, B, TOT) isolates: Number of isolates collected that season
# (H1, H3, B, TOT) match: Number of isolates collected that season that match the vaccine strains (H1, H3, B, trivalent vax in general)

# vaxmatch2.csv: season, season yrs, subtype, subtype marker, H1 match, H3 match, B match, tot match, match level, match level marker
# prominent subtype marker (different than subtype5.csv): 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B
# H1 match: percent of H1 virus isolates that were characterized as antigenically similar to the H1 component of the season's Northern Hemisphere trivalent flu vaccine, rounded to the nearest whole percent. 
# H3 match: same as H1_MATCH with H3 virus isolates
# B match: same as H1_MATCH with B virus isolates across both Yamagata and Victoria lineages. M
# tot match: percent of all virus isolates that were characterized as antigenically similar to any of the trivalent vaccine strains, rounded to the nearest whole percent. These levels are not the same to those used by the CDC website to categorize vaccine strain match.
# match level: qualitative code that represents level of vaccine strain match with strains circulating during the season. This is calculated as percent of virus isolates that match one vaccine strain in the trivalent vaccine out of the total number of virus isolates collected that season. These are the codes we have defined: very low = 0-20%; low = 21-40%; medium = 41-60%; high = 61-80%; very high = 81-100%
# match level marker: match level marker for plotting 1 = very low; 2 = low; 3 = medium; 4 = high; 5 = very high

### packages/modules ###
import csv
import matplotlib.pyplot as plt

## local modules ##

### data structures ###
# dict_ix[seasonnum] = CDC severity index value
# dict_subvax[seasonnum] = (prominent subtype marker, dominant subtype marker)
# dict_vaxmatch[seasonnum] = (H1 match perc, H3 match perc, B match perc, total trivalent match perc, vaccine match level marker)
d_ix, d_subvax, d_vaxmatch = {},{},{}


### functions ###
def ix_import (csvreadfile):
	''' Import CDC_Source/Import_Data/cdc_severity_index.csv data, which includes z-normalized contributors to CDC severity index. These data include: percent of positive flu lab tests, proportion of mortality due to P&I, pediatric deaths, proportion of ILI, 5-17 years hospitalization rate, and 18-49 years hospitalization rate. Data are not available for all 10 seasons.
	'''
	season, index = [],[]
	for row in csvreadfile:
		season.append(int(row[0]))
		index.append(float(row[7]))
	# dict_ix[seasonnum] = CDC severity index value
	dict_ix = dict(zip(season, index))
	
	return dict_ix

def subvax_import (csvreadfile):
	''' Import SQL_EXPORT/subtype5.csv data, which includes information on prominent subtype, subtypes of isolates that were identified, and isolates that match with the vaccine strains.
	'''
	season, s_marker, ds_marker = [],[],[]
	for row in csvreadfile:
		H1i, H3i, Bi, TOTi = float(row[4]), float(row[5]), float(row[6]), float(row[7])
		season.append(int(row[0])) # season number
		s_marker.append(int(row[3])) # subtype value for plotting
		if H1i>H3i and H1i>Bi:
			ds_marker.append(1) # plurality of H1 isolates
		elif H3i>H1i and H3i>Bi:
			ds_marker.append(2) # plurality of H3 isolates
		else:
			ds_marker.append(3) # plurality of B isolates
	# dict_subvax[seasonnum] = (prominent subtype marker, dominant subtype marker)
	dict_subvax = dict(zip(season, zip(s_marker, ds_marker)))
	
	return dict_subvax

def vaxmatch_import (csvreadfile):
	''' Import SQL_EXPORT/vaxmatch2.csv data, which includes information on prominent subtype, and vaccine match percentage for each subtype and the sum total for the trivalent vaccine.
	'''
	season, match1, match3, matchb, matcht, mlvl_marker = [],[],[],[],[],[]
	for row in csvreadfile:
		season.append(int(row[0]))
		match1.append(float(row[4]))
		match3.append(float(row[5]))
		matchb.append(float(row[6]))
		matcht.append(float(row[7]))
		mlvl_marker.append(int(row[9]))
	# dict_vaxmatch[seasonnum] = (H1 match perc, H3 match perc, B match perc, total trivalent match perc, vaccine match level marker)
	dict_vaxmatch = dict(zip(season, zip(match1, match3, matchb, matcht, mlvl_marker)))
	
	return dict_vaxmatch

### import data ###
ixin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data/cdc_severity_index.csv','r')
ixin.readline()
ix = csv.reader(ixin, delimiter=',')
subvaxin = open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/subtype5.csv', 'r')
subvax = csv.reader(subvaxin, delimiter=',')
vaxmatchin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/vaxmatch2.csv','r')
vaxmatch=csv.reader(vaxmatchin, delimiter=',')


### plotting parameters ###
promsublab = ['','H1','H1 & B','H1 & H3 & B','H3 & B','H3','']
snums = xrange(2, 11)

### program ###
# import data
d_ix = ix_import(ix)
d_subvax = subvax_import(subvax)
d_vaxmatch = vaxmatch_import(vaxmatch)

# vax efficacy TIV and LAIV (OR_vaxeffs_v6-15-13.py) #
# generate weighted avg vax efficacy data 
vaxeffT_seas = [1, 2, 3, 5, 6, 7, 8, 9]
# see USfluvaxdata_June13.ods
vaxeffT_wt = [69.1, 54.6, 64.0, 61.5, 28.1, 57.8, 60.5, 76.0] 
d_vaxefftot = dict(zip(vaxeffT_seas, vaxeffT_wt))


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

# CDC index vs. prominent subtype (>=20% isolate = prominent)
subtype = [d_subvax[s][0] for s in snums]
plt.plot(subtype, sevix, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(snums, subtype, sevix):
	plt.annotate(s, xy = (x, y), xytext = (-7,5), textcoords = 'offset points', fontsize=16)
plt.ylabel('Benchmark index', fontsize=24)
plt.xlabel('Prominent subtypes', fontsize=24)
plt.xticks(xrange(7), promsublab, fontsize=16)
plt.yticks(fontsize=16)
plt.show()

# CDC index vs. vax efficacy TIV & LAIV
print d_vaxefftot
vaxeff = [d_vaxefftot[s] for s in vaxeffT_seas]
plt.plot(vaxeff, sevix_veff, marker = 'o', color = 'black', linestyle = 'None')
for s, x, y in zip(vaxeffT_seas, vaxeff, sevix_veff):
	plt.annotate(s, xy = (x, y), xytext = (-7,5), textcoords = 'offset points', fontsize=16)
plt.ylabel('Benchmark index', fontsize=24)
plt.xlabel('Vaccine efficacy (TIV & LAIV)', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlim([0, 100])
plt.show()





















