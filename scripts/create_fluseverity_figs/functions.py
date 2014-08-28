#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 4/24/14

## Purpose: script of functions for data cleaning and processing to draw flu severity figures; supports figures in create_fluseverity_figs


###Command Line: would not be called from command line directly 
##############################################

##############################################
# header
from collections import defaultdict
from datetime import date, datetime
from itertools import product
import numpy as np
import matplotlib.cm as cm
import bisect

##############################################
# global parameters - methods

## SDI data ##
gp_normweeks = 7 # number of weeks in baseline normalization period
gp_fluweeks = 34 # number of weeks in flu season (weeks 40-20)
gp_retro_duration = 2 # duration of retrospective period in weeks
gp_begin_retro_week = 3 # number of weeks before the peak incidence week that the retrospective period should begin (that season only)
gp_early_duration = 2 # duration of the early warning period in weeks
gp_begin_early_week = 2 # number of weeks after the week with Thanksgiving that the early warning period should begin (that season only)
gp_plotting_seasons = range(2,10) # season numbers for which data will be plotted (eg. Season 2 = 2001-02)
gp_plotting_regions = range(1, 11) # region numbers
gp_mild =[3, 6, 7, 9] # seasons 3, 6, 7, 9
gp_mod = [2, 5] # seasons 2, 5
gp_sev = [4, 8] # seasons 4, 8, 10 (pandemic)

## ILINet data ## 
gp_ILINet_plotting_seasons = range(-2, 10) + range(11,15) # remove 2009-10 data

## pandemic analyses only ## 
gp_pandemic_plotting_seasons = range(9,11) # 2008-09 and 2009-10 data only
gp_pandemicbaseline = ['between pandemic waves', 'last season baseline', 'after pandemic']


##############################################
# global parameters - plotting

## SDI data ##
gp_seasonlabels = ['01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09']
gp_colors_1_10 = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
# gp_colors = ['black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet']
gp_colors = ["#e41a1c", "#4daf4a", "#377eb8", "#ff7f00", "#984ea3", "#ffff33", "#a65628", "#f781bf"]
gp_regions = ['Boston (R1)', 'New York (R2)', 'Philadelphia (R3)', 'Atlanta (R4)', 'Chicago (R5)', 'Dallas (R6)', 'Kansas City (R7)', 'Denver (R8)', 'San Francisco (R9)', 'Seattle (R10)']
gp_weeklabels = range(40,54) # week number labels for plots vs. time
gp_weeklabels.extend(range(1,40))
gp_severitylabels = ['Mild', 'Moderate', 'Severe']
gp_severitycolors = ['b', 'y', 'r']
gp_line_style = ['-', ':']
gp_barwidth = 0.35
gp_agelabels = ['Child', 'Adult', 'Other Ages']
gp_agecolors = ['orange', 'grey', 'green']
gp_mild_severe_colors = ['blue', 'red']
gp_plot_titles = ['Mild Season', 'Severe Season']

## ILINet data ##
gp_ILINet_seasonlabels = ['97-98', '98-99', '99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '10-11', '11-12', '12-13', '13-14']
gp_ILINet_colors = cm.rainbow(np.linspace(0, 1, len(gp_ILINet_seasonlabels)))

##############################################
## call parameters ##
# set these parameters every time a plot is run

pseasons = gp_plotting_seasons


##############################################
def anydiag_baseline_comparison(csvreadfile):
	''' Number of any diagnosis visits across all
	ages, service places, and zip3s for fall baseline (weeks 40-46) and summer baseline (weeks 33-39 in previous 'season').
	dict_anydiag[season] = (# anydiag fall BL, # anydiag summer BL)
	'''
	main(anydiag_baseline_comparison)

	dict_wk = {}
	dict_dummyany = {}
	# import data
	for row in csvreadfile:
		season, weeknum = int(row[0]), int(row[3])
		anydiag = float(row[4])
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		dict_wk[(wk, weeknum)] = season
		dict_dummyany[(wk, weeknum)] = anydiag

	dict_anydiag = {}
	for season in pseasons:
		# keys for wks 40-46 of season
		fallBL_weeks = [key for key in dict_wk if dict_wk[key] == season and key[1] > 39]
		# keys for wks 33-39 of season-1
		summerBL_weeks = [key for key in dict_wk if dict_wk[key] == season-1 and key[1] < 40]
		# total number of diagnoses # divide by #weeks?
		fallBL = sum([dict_dummyany[key] for key in fallBL_weeks])#/float(len(fallBL_weeks))
		summerBL = sum([dict_dummyany[key] for key in summerBL_weeks])#/float(len(summerBL_weeks))
		dict_anydiag[season] = (fallBL, summerBL)

	return dict_anydiag

##############################################
def benchmark_factors_import(csvreadfile):
	''' Import CDC_Source/Import_Data/cdc_severity_data_cleaned.csv, which includes the raw data used to create the benchmark index that pairs with the SDI severity index.
	dict_benchfactors[season] = (percent positive isolates, proportion of total mortality due to P&I, number of pediatric deaths, child hospitalization rate, adult hospitalization rate)
	'''
	main(benchmark_factors_import)

	dict_benchfactors = {}
	for row in csvreadfile:
		row2 = [float('nan') if item == 'NA' else item for item in row]
		season = int(row2[0])
		perc_pos, pi_mort, ped = float(row2[1]), float(row2[2]), float(row2[3])
		c_hos, a_hos = float(row2[5]), float(row2[6])
		dict_benchfactors[season] = (perc_pos, pi_mort, ped, c_hos, a_hos)

	return dict_benchfactors

##############################################
def benchmark_import (csv_cdcseverity, index_col):
	''' Import CDC_Source/Import_Data/cdc_severity_index.csv data, which includes z-normalized contributors to CDC severity index. These data include: percent of positive flu lab tests, proportion of mortality due to P&I, pediatric deaths, 5-17 years hospitalization rate, and 18-49 years hospitalization rate. Outpatient ILI is included in the index in the 7th column. The index in the 8th column does not include outpatient ILI. All data sources are not available for every season. Flu season includes weeks 40 to 17 (instead of the standard weeks 40 to 20) because Return dictionary with season to benchmark index value.
	dict_benchmark[seasonnum] = CDC benchmark index value
	'''
	main(benchmark_import)
	
	season, index = [],[]
	for row in csv_cdcseverity:
		season.append(int(row[0]))
		index.append(float(row[index_col]))
	# dict_benchmark[seasonnum] = CDC severity index value
	dict_benchmark = dict(zip(season, index))
	
	return dict_benchmark

##############################################
def cdc_import_CFR_CHR (csv_allcdc):
	''' Import CDC_Source/Import_Data/all_cdc_source_data.csv, which includes weekly CDC source data from multiple surveillance systems from October 1997 to December 2013. Export season-level case fatality proxy and flu hospitalization rate using P&I deaths, lab-confirmed hospitalization rates per 100,000, and ILI cases as numerators, numerators, and denominators, respectively. Return dictionaries with season to hospitalization rate across entire season (lab-confirmed flu), season to . Note: These are not the same as case-hospitalization or case-fatality rates.
	dict_CHR[seasonnum] = cumulative lab-confirmed case-hospitalization rate over the period from week 40 to week 17 during flu season
	
	'''
	main(cdc_import_CFR_CHR)
	
	dict_deaths_ILI_counts, dict_CHR = {}, {}
	for row in csv_allcdc:
		year, week, season = str(row[1][2:]), str(row[2]), str(row[12])
		dummyvals = [row[19], row[13], row[27], row[28]] # PI_deaths, allcoz_deaths, ILI, allpatients # 7/28/14 corrected indexing typo
		PI_deaths, allcoz_deaths, ILI, allpatients = [float('nan') if val == 'NA' else float(val) for val in dummyvals] # 7/28/14 convert NA string to NaNs
		CHR = str(row[26])
		
		if week == 'NA':
			continue
		# reassign year and week as integers after skipping NAs
		year, week = int(year), int(week)
		if int(season) in pseasons:
			# dict_deaths_ILI_counts[(seasonnum, weeknum)] = (P&I deaths, all deaths, ILI cases, total patients)
			dict_deaths_ILI_counts[(int(season), week)] = (PI_deaths, allcoz_deaths, ILI, allpatients)
		
		# grab cumulative hospitalization rate at week 17 in each plotting season
		if year in pseasons and week == 17:
			# for seasons prior to 2003-04, CHR should be float('nan')
			if CHR == 'NA':
				CHR = float('nan')
			# dict_CHR[seasonnum] = cumulative lab-confirmed case-hospitalization rate per 100,000 individuals in population over the period from week 40 to week 17 during flu season
			dict_CHR[year] = float(CHR)
		
	# subset dict_deaths_ILI_counts for weeks that will contribute to each season's P&I mortality and ILI proportion rates (weeks 40 to 20)
	dict_deaths_ILI_counts_fluwks = dict([(k, dict_deaths_ILI_counts[k]) for k in dict_deaths_ILI_counts if k[1]>20 and k[1]<40])
	
	# sum PI_deaths, allcoz_deaths, ILI, allpatients for each season 
	dict_deaths, dict_ILI, dict_CFR = {}, {}, {}
	for s in pseasons:
		
		# dict_deaths[seasonnum] = (P&I deaths from wks 40 to 20, all cause deaths from wks to 40 to 20)
		dict_deaths[s] = (sum([float(dict_deaths_ILI_counts_fluwks[k][0]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]), sum([float(dict_deaths_ILI_counts_fluwks[k][1]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]))
		
		# dict_ILI[seasonnum] = (ILI cases from wks 40 to 20, all patients from wks 40 to 20)
		dict_ILI[s] = (sum([float(dict_deaths_ILI_counts_fluwks[k][2]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]), sum([float(dict_deaths_ILI_counts_fluwks[k][2]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]))
		
		# dict_CFR[seasonnum] = P&I deaths of all flu season deaths in 122 cities/outpatient ILI cases of all flu season patient visits to outpatient offices in ILINet
		dict_CFR[s] = (dict_deaths[s][0]/dict_deaths[s][1])/(dict_ILI[s][0]/dict_ILI[s][1])
	
	return dict_CHR, dict_CFR, dict_deaths, dict_ILI

##############################################
def classif_zOR_index(dict_wk, dict_incid53ls, dict_incid53ls_reg, retro_level_string, csv_Thanksgiving):
	''' Find the retrospective and early warning period start weeks by season. The retrospective period may be designated in two manners -- relative to the national peak incidence week or regional peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving. This function returns a dictionary that can be used by classif_zOR_region_processing to set the classification periods for each region to that which was defined at the national level.
	The week plotting dicts (national and regional) must be run before this function. The Thanksgiving_import function is nested within this function. Return dictionary for season to (index of first retro period week, index of first early warning period week).
	dict_classifindex[seasonnum] = (index of first retro period week, index of first early warning period week)
	'''
	main(classif_zOR_index)

	# for nation-level peak-based retrospective classification
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]

	# for region-level peak-based retrospective classification
	# (don't want to call dict_wk twice), dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
		
	dict_classifindex = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)

	for s, r in product(pseasons, gp_plotting_regions):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		
		# nation-lvl peak-based retrospective classification
		if retro_level_string == 'nation':
			peak_index = peak_flu_week_index(dict_incid53ls[s]) # 7/31/14 - max among flu weeks
			begin_retro = peak_index - gp_begin_retro_week
		
		# region-lvl peak-based retrospective classif
		elif retro_level_string == 'region':
			peak_index = peak_flu_week_index(dict_incid53ls_reg[(s, r)]) # 7/31/14 - max among flu weeks
			begin_retro = peak_index - gp_begin_retro_week
		
		else:
			print 'retro_level_string error'
			break
		
		# Thanksgiving-based early warning classification
		Thx_index = weekdummy.index(dict_Thanksgiving[s])
		begin_early = Thx_index + gp_begin_early_week
		
		# dict_classifindex[(seasonnum, region)] = (index of first retro period week, index of first early warning period week)
		dict_classifindex[(s, r)] = (begin_retro, begin_early)
		
	return dict_classifindex
	
##############################################
def classif_zOR_index_state(dict_wk, dict_incid53ls, dict_incid53ls_state, retro_level_string, csv_Thanksgiving):
	''' Find the retrospective and early warning period start weeks by season. The retrospective period may be designated in two manners -- relative to the national peak incidence week or regional peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving. This function returns a dictionary that can be used by classif_zOR_region_processing to set the classification periods for each region to that which was defined at the national level.
	The week_plotting_dicts (national and state) function should be run before this function. The Thanksgiving_import function is nested within this function. Return dictionary for season to (index of first retro period week, index of first early warning period week).
	dict_classifindex[seasonnum] = (index of first retro period week, index of first early warning period week)
	'''
	main(classif_zOR_index_state)

	# for nation-level peak-based retrospective classification
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]

	# for region-level peak-based retrospective classification
	# (don't want to call dict_wk twice), dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_state[(seasonnum, state)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
		
	dict_classifindex = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)

	# states in state-level analysis
	state_keys = list(set([k[1] for k in dict_incid53ls_state]))
	
	for s, state in product(pseasons, state_keys):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		ILINet_week_OR_processing
		# nation-lvl peak-based retrospective classification
		if retro_level_string == 'nation':
			peak_index = peak_flu_week_index(dict_incid53ls[s]) # 7/31/14 - max among flu weeks
			begin_retro = peak_index - gp_begin_retro_week
		
		# state-lvl peak-based retrospective classif
		elif retro_level_string == 'state':
			peak_index = peak_flu_week_index(dict_incid53ls_state[(s, state)]) # 7/31/14 - max among flu weeks
			begin_retro = peak_index - gp_begin_retro_week
		
		else:
			print 'retro_level_string error'
			break
		
		# Thanksgiving-based early warning classification
		Thx_index = weekdummy.index(dict_Thanksgiving[s])
		begin_early = Thx_index + gp_begin_early_week
		
		# dict_classifindex[(seasonnum, state)] = (index of first retro period week, index of first early warning period week)
		dict_classifindex[(s, state)] = (begin_retro, begin_early)
		
	return dict_classifindex

##############################################
def classif_zOR_processing(dict_wk, dict_incid53ls, dict_zOR53ls, csv_Thanksgiving):
	''' Calculate retrospective and early warning zOR classification values for each season, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period is designated relative to the peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The week_plotting_dicts function must be run before this function. The Thanksgiving_import function is nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR.
	dict_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zOR_processing)
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	
	dict_classifzOR = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)
	
	for s in pseasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		
		# peak-based retrospective classification
		peak_index = peak_flu_week_index(dict_incid53ls[s]) # 7/31/14 - max among flu weeks
		begin_retro = peak_index - gp_begin_retro_week
		# list of week indices in retrospective period
		retro_indices = xrange(begin_retro, begin_retro+gp_retro_duration)
		mean_retro_zOR = np.mean([dict_zOR53ls[s][i] for i in retro_indices])
		
		# Thanksgiving-based early warning classification
		Thx_index = weekdummy.index(dict_Thanksgiving[s])
		begin_early = Thx_index + gp_begin_early_week
		# list of week indices in early warning period
		early_indices = xrange(begin_early, begin_early+gp_early_duration)
		mean_early_zOR = np.mean([dict_zOR53ls[s][i] for i in early_indices])
	
		# dict_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
		dict_classifzOR[s] = (mean_retro_zOR, mean_early_zOR)
		
	return dict_classifzOR

##############################################
def classif_zOR_region_processing(dict_classifindex, dict_wk, dict_zOR53ls_reg):
	''' Calculate retrospective and early warning zOR classification values for each season and region combination, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period may be designated in two manners -- relative to the national peak incidence week or regional peak incidence week in the flu season.The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The classif_zOR_index function must be run before this function. The Thanksgiving_import function is nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR.
	dict_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zOR_region_processing)

	# dict_classifindex[(seasonnum, region)] = (index of first retro period week, index of first early warning period week), dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...], dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
	
	dict_classifzOR_reg = {}
	
	for s, r in product(pseasons, gp_plotting_regions):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		begin_retro, begin_early = dict_classifindex[(s, r)]
		
		# peak-based retrospective classification
		# list of week indices in retrospective period
		retro_indices = xrange(begin_retro, begin_retro+gp_retro_duration)
		mean_retro_zOR = np.mean([dict_zOR53ls_reg[(s, r)][i] for i in retro_indices])
		
		# Thanksgiving-based early warning classification
		# list of week indices in early warning period
		early_indices = xrange(begin_early, begin_early+gp_early_duration)
		mean_early_zOR = np.mean([dict_zOR53ls_reg[(s, r)][i] for i in early_indices])
	
		# dict_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
		dict_classifzOR_reg[(s, r)] = (mean_retro_zOR, mean_early_zOR)
		
	return dict_classifzOR_reg

##############################################
def classif_zOR_state_processing(dict_classifindex, dict_wk, dict_zOR53ls_state):
	''' Calculate retrospective and early warning zOR classification values for each season and state combination, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period may be designated in two manners -- relative to the national peak incidence week or state peak incidence week in the flu season.The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The week_plotting_dicts_state and classif_zOR_index_state functions must be run before this function. The Thanksgiving_import function is nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR.
	dict_classifzOR_state[(seasonnum, state)] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zOR_state_processing)
	
	# dict_classifindex[(seasonnum, state)] = (index of first retro period week, index of first early warning period week), dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...], dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_state[(seasonnum, stat)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
	
	dict_classifzOR_state = {}
	
	# states in state-level analysis
	state_keys = list(set([k[1] for k in dict_zOR53ls_state]))

	for s, state in product(pseasons, state_keys):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		begin_retro, begin_early = dict_classifindex[(s, state)]
		
		# peak-based retrospective classification
		# list of week indices in retrospective period
		retro_indices = xrange(begin_retro, begin_retro+gp_retro_duration)
		mean_retro_zOR = np.mean([dict_zOR53ls_state[(s, state)][i] for i in retro_indices])
		
		# Thanksgiving-based early warning classification
		# list of week indices in early warning period
		early_indices = xrange(begin_early, begin_early+gp_early_duration)
		mean_early_zOR = np.mean([dict_zOR53ls_state[(s, state)][i] for i in early_indices])
	
		# dict_classifzOR_reg[(seasonnum, state)] = (mean retrospective zOR, mean early warning zOR)
		dict_classifzOR_state[(s, state)] = (mean_retro_zOR, mean_early_zOR)
		
	return dict_classifzOR_state

##############################################
def contributions_CAO_to_attack(dict_wk, dict_incid):
	''' Import dict_wk and dict_incid. Sum values in dict_incid for children, adults, and other age groups to get an attack rate for each season. The sum of the child, adult, and other attack rates is the total attack rate. Calculate the percentage contribution of each age group to the total attack rate for each season, in preparation to plot data in a stacked 100% bar chart. The flu season is defined as weeks 40 to 20. 
		dict_wk[week] = seasonnum
		dict_incid[week] = (child ILI cases per 100,000 in US population in second calendar year of flu season, adult incid per 100,000, other age group ILI cases per 100,000)
		dict_perc_totAR[seasonnum] = (% contribution of child AR to total AR, % contribution of adult AR to total AR, % contribution of other ages AR to total AR)
		dict_tot_attack[seasonnum] = total attack rate for weeks 40 to 20 by 100,000
	'''
	main(contributions_CAO_to_attack)

	dict_incidC_season, dict_incidA_season, dict_incidO_season, dict_attackCAO, dict_tot_attack, dict_perc_totAR = defaultdict(list), defaultdict(list), defaultdict(list), {}, {}, {}
	
	for s in pseasons:
		# list of incidence per 100,000 by week for children and adults
		dict_incidC_season[s] = [dict_incid[week][0] for week in sorted(dict_wk) if dict_wk[week] == s]
		dict_incidA_season[s] = [dict_incid[week][1] for week in sorted(dict_wk) if dict_wk[week] == s]
		dict_incidO_season[s] = [dict_incid[week][2] for week in sorted(dict_wk) if dict_wk[week] == s]

		# attack rates per 100,000 for children, adults, and other age groups by week, include only wks 40 to 20 (52 weeks total in each season)
		dict_attackCAO[s] = (sum(dict_incidC_season[s][:33]), sum(dict_incidA_season[s][:33]), sum(dict_incidO_season[s][:33]))

		# total attack rate per 100,000 by season for export
		# dict_tot_attack[seasonnum] = total attack rate for weeks 40 to 20 by 100,000
		dict_tot_attack[s] = float(sum(dict_attackCAO[s]))

		# calculate percentage contribution of each age group's attack rate to total seasonal attack rate.
		# dict_perc_totAR[seasonnum] = (% contribution of child AR to total AR, % contribution of adult AR to total AR, % contribution of other ages AR to total AR)
		dict_perc_totAR[s] = tuple([AR/dict_tot_attack[s]*100 for AR in dict_attackCAO[s]])

	return dict_perc_totAR, dict_tot_attack

##############################################
def cum_incid_at_classif(dict_wk, dict_incid53ls, dict_Thanksgiving, snum):
	''' For a given season, calculate the cumulate incidence percentage for the weeks in the retrospective and early warning periods.
	'''
	# main(cum_incid_at_classif)

	
	weekdummy = sorted([key for key in dict_wk if dict_wk[key] == snum])
	
	# total season incidence
	tot_incid = float(sum(dict_incid53ls[snum][:gp_fluweeks]))

	# peak-based retrospective classification
	peak_index = peak_flu_week_index(dict_incid53ls[snum])
	print 'pk ix', peak_index
	begin_retro = peak_index - gp_begin_retro_week
	# list of week indices in retrospective period
	retro_indices = xrange(begin_retro, begin_retro+gp_retro_duration)
	cum_incid_retro = [sum(dict_incid53ls[snum][:i+1]) for i in retro_indices] # cumulative incidence up to and including index week
	cum_perc_incid_retro = [incid/tot_incid*100 for incid in cum_incid_retro]
	
	# Thanksgiving-based early warning classification
	Thx_index = weekdummy.index(dict_Thanksgiving[snum])
	begin_early = Thx_index + gp_begin_early_week
	# list of week indices in early warning period
	early_indices = xrange(begin_early, begin_early+gp_early_duration)
	cum_incid_early = [sum(dict_incid53ls[snum][:i+1]) for i in early_indices] # cumulative incidence up to and including index week
	cum_perc_incid_early = [incid/tot_incid*100 for incid in cum_incid_early]
		
	return cum_perc_incid_retro, cum_perc_incid_early

##############################################
def epidemic_duration(incid53ls, min_cum_perc, max_cum_perc):
	''' Return the number of weeks in an epidemic, given a list of the incidence curve for a complete season and the definition of epidemic duration. Epidemic duration is defined by the cumulative percentage of incidence during the flu epidemic.
	'''	
	tot_incid = float(sum(incid53ls[:gp_fluweeks]))
	cum_incid_perc = list(np.cumsum(incid53ls[:gp_fluweeks])/tot_incid*100)
	epi_index_min = bisect.bisect(cum_incid_perc, min_cum_perc)
	epi_index_max = bisect.bisect(cum_incid_perc, max_cum_perc)
	epidemic_dur = epi_index_max-epi_index_min+1
	return epidemic_dur

##############################################
def ILI_AR(csv_SDI):
	''' Import data of the format: season, week, year, week number, ILI cases, any diagnosis cases, total population size (SQL_export/F1.csv, SQL_export/Supp_acuteILI_wk.csv). Return dictionary dict_facilitytypeAR[season] = ILI cases/total population * 100,000.
	'''
	# dict_facilitytypeAR[season] = ILI cases/total population in second year of flu season * 100,000
	dict_facilitytypeAR = {}
	dict_wk, dict_ILI_dummy = {}, {}
	for row in csv_SDI:
		season, week = int(row[0]), row[1]
		ILI, pop = float(row[4]), int(row[6]) # pop is the same for every entry that takes place in the same year
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		dict_wk[wk] = season
		dict_ILI_dummy[wk] = (ILI, pop)
	# list of unique season numbers
	seasons = list(set([dict_wk[wk] for wk in dict_wk]))
	# generate dict of attack rate per 100,000 for flu season (gp_fluweeks long)
	for s in seasons:
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk] == s])[:gp_fluweeks]
		AR = sum([dict_ILI_dummy[wk][0] for wk in dummyweeks])/dict_ILI_dummy[dummyweeks[-1]][1] * 100000
		dict_facilitytypeAR[s] = AR

	return dict_facilitytypeAR

##############################################
def ILINet_week_OR_processing(csv_incidence, csv_population):
	''' Import CDC_Source/Import_Data/all_cdc_source_data.csv, which includes unique id, year, week, age group, and ILI incid. Import Census/Import_Data/totalpop_age_Census_98-14.csv, which includes season, age group code, and US population. Return dictionary with week to season number, week to ILI cases per 100,000 in total US population, and dictionary with week to OR. OR attack rates for children and adults will be calculated based on popstat variable of the population in the second calendar year of the flu season (eg. 2001-02 season is based on 2002 population). In ILINet, children are 5-24 years and adults are 25-64 years. In totalpop_age.csv, children are 5-19 years and adults are 20-59 years.
	dict_wk[week] = seasonnum
	dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season
	dict_OR[week] = OR
	'''
	main(ILINet_week_OR_processing)
	
	## import ILI data ##
	# dict_ILI_week[(week, agegroup code)] = ILI cases; dict_wk[week] = seasonnum, S1 = 2000-01
	dict_ILI_week, dict_wk = {}, {}
	for row in csv_incidence: 
		row_cl = [float('nan') if val == 'NA' else val for val in row]
		week = str(row_cl[0])+'0' # additional 0 represents Sunday
		wktime = datetime.strptime(week, '%Y%U%w') # format = 4-dig year, 2-dig week beginning on Monday (8/10/14), digit representing day of week; data are from one week later than week number listed on plots (for both ILINet and SDI data).
		wk = datetime.date(wktime) # remove the time from the datetime format
		dict_ILI_week[(wk, 'C')] = float(row_cl[33])
		dict_ILI_week[(wk, 'A')] = float(row_cl[34])
		dict_ILI_week[(wk, 'O')] = float(row_cl[27])-float(row_cl[33])-float(row_cl[34])
		dict_wk[wk] = int(row_cl[12])
	
	# define age group codes
	age_keys = ['C', 'A', 'O']
	
	## import population data ##
	dict_pop = {}
	for row in csv_population:
		season = int(row[0])
		agecode = row[1]
		# dict_pop[(season, agegroup code)] = population size of agegroup		
		dict_pop[(season, agecode)] = int(row[2]) 
	
	# generate incidence per 100,000 in US population and OR at the weekly level
	dict_incid, dict_OR = {}, {}
	for wk in dict_wk:
		s = dict_wk[wk]
		# dict_incid[week] = ILI incidence per 100,000 in US pop in second calendar year of flu season
		tot_incid = sum([dict_ILI_week[(wk, age)] for age in age_keys])/sum([dict_pop[(s, age)] for age in age_keys]) * 100000
		dict_incid[wk] = tot_incid
		# dict_OR[week] = OR
		child_attack = dict_ILI_week[(wk, 'C')]/dict_pop[(s, 'C')]
		adult_attack = dict_ILI_week[(wk, 'A')]/dict_pop[(s, 'A')]
		OR = (child_attack/(1-child_attack))/(adult_attack/(1-adult_attack))
		dict_OR[wk] = float(OR)
	
	return dict_wk, dict_incid, dict_OR

##############################################
def normalize_attackCA(dict_wk, dict_incid):
	''' Import dict_wk and dict_incid. Sum values in dict_incid for children and adults to get an attack rate for each season. The flu season is defined as weeks 40 to 20. Normalize the child and adult attack rates by dividing the raw attack rate by the average child and adult attack rates and subtract 1 (percentage deviation from baseline) across all seasons. 
		dict_wk[week] = seasonnum
		dict_incid[week] = (child ILI cases per 100,000 in US population in second calendar year of flu season, adult incid per 100,000, other age group ILI cases per 100,000)
		dict_attackCA_norm[seasonnum] = (% dev from baseline child attack rate, % dev from baseline adult attack rate)
	'''
	main(normalize_attackCA)

	dict_incidC_season, dict_incidA_season, dict_attackCA, dict_attackCA_norm = defaultdict(list), defaultdict(list), {}, {}
	
	for s in pseasons:
		# list of incidence per 100,000 by week for children and adults
		dict_incidC_season[s] = [dict_incid[week][0] for week in sorted(dict_wk) if dict_wk[week] == s]
		dict_incidA_season[s] = [dict_incid[week][1] for week in sorted(dict_wk) if dict_wk[week] == s]

		# attack rates per 100,000 for children and adults by week, include only wks 40 to 20 (52 weeks total in each season)
		dict_attackCA[s] = (sum(dict_incidC_season[s][:gp_fluweeks]), sum(dict_incidA_season[s][:gp_fluweeks]))

	# calculate average C and A attack rates across all seasons
	avg_attackC = float(np.mean([dict_attackCA[k][0] for k in dict_attackCA]))
	avg_attackA = float(np.mean([dict_attackCA[k][1] for k in dict_attackCA]))
	avgs = (avg_attackC, avg_attackA)

	# normalize incidence curves by average attack rate for the age group, subtract 1 to center the ratio at 0, multiply by 100 to recover the percent deviation in seasonal attack rate from baseline average of attack rates across all seasons in study
	for s in pseasons:	
		# dict_attackCA_norm[seasonnum] = (% dev from baseline C attack rate, % dev from baseline A attack rate)
		dict_attackCA_norm[s] = (((dict_attackCA[s][0]/avgs[0])-1)*100, ((dict_attackCA[s][1]/avgs[1])-1)*100)

	return dict_attackCA_norm

##############################################
def normalize_incidCA(dict_wk, dict_incid):
	''' Import dict_wk and dict_incid and normalize dict_incid by the maximum child incidence value during a flu season.
		dict_wk[week] = seasonnum
		dict_incid[week] = (child ILI cases per 10,000 in US population in second calendar year of flu season, adult incid per 10,000, other age group ILI cases per 10,000)
		dict_incidC_norm[seasonnum] = [norm child incid wk40, norm child incid wk41, ...]
		dict_incidA_norm[seasonnum] = [norm adult incid wk40, norm adult incid wk 41, ...]
	'''
	main(normalize_incidCA)

	dict_incidC_season, dict_incidA_season, dict_incidC_norm, dict_incidA_norm = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
	
	for s in set(dict_wk.values()):
		dict_incidC_season[s] = [dict_incid[week][0] for week in sorted(dict_wk) if dict_wk[week] == s]
		dict_incidA_season[s] = [dict_incid[week][1] for week in sorted(dict_wk) if dict_wk[week] == s]
		maxC = max(dict_incidC_season[s][:gp_fluweeks]) # max peak child epidemic during wks 40 to 20
		# normalize incidence curves by max peak child epidemic
		dict_incidC_norm[s] = [val/maxC for val in dict_incidC_season[s]]
		dict_incidA_norm[s] = [val/maxC for val in dict_incidA_season[s]]

	return dict_incidC_norm, dict_incidA_norm

##############################################
def peak_flu_week_index(incid53ls):
	''' Return index of peak week during the flu season when passed a list of the weekly incidence for the entire year (weeks 40 to 39). 
	'''
	main(peak_flu_week_index)
	peak_index = incid53ls.index(max(incid53ls[:gp_fluweeks]))
	return peak_index

##############################################
def proportion_ILI_anydiag(csv_SDI):
	''' Import data of the format: season, week, year, week number, ILI cases, any diagnosis cases, total population size (SQL_export/F1.csv, SQL_export/Supp_acuteILI_wk.csv). Return dictionary dict_ILI_anydiag[season] = ILI cases/any diagnosis cases.
	'''
	# dict_ILI_anydiag[season] = ILI cases/any diagnosis cases
	dict_ILI_anydiag = {}
	dict_wk, dict_prop_dummy = {}, {}
	for row in csv_SDI:
		season, week = int(row[0]), row[1]
		ILI, anydiag = float(row[4]), int(row[5])
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		dict_wk[wk] = season
		dict_prop_dummy[wk] = (ILI, anydiag)
	# list of unique season numbers
	seasons = list(set([dict_wk[wk] for wk in dict_wk]))
	# generate dict of ILI proportion of all cases at season level for flu weeks only
	for s in seasons:
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk] == s])[:gp_fluweeks]
		prop = sum([dict_prop_dummy[wk][0] for wk in dummyweeks])/sum([dict_prop_dummy[wk][1] for wk in dummyweeks])
		dict_ILI_anydiag[s] = prop

	return dict_ILI_anydiag

##############################################
def readNationalClassifFile(national_file):
	''' Import national classification file (season, mn_retro, mn_early) into dict.
	'''
	main(readNationalClassifFile)
	dict_national_classif = {}
	for line in national_file:
		season = int(line[0])
		mean_retro_zOR, mean_early_zOR = float(line[1]), float(line[2])
		dict_national_classif[season] = (mean_retro_zOR, mean_early_zOR)
	return dict_national_classif

##############################################
def readStateClassifFile(state_file):
	''' Import state classification file (season, state, mn_retro, mn_early) into dict. 
	'''
	main(readStateClassifFile)
	dict_state_classif = {}
	for line in state_file:
		season, state = int(line[0]), str(line[1])
		mean_retro_zOR, mean_early_zOR = float(line[2]), float(line[3])
		dict_state_classif[(season, state)] = (mean_retro_zOR, mean_early_zOR)
	return dict_state_classif

##############################################
def region_state_dictionary():
	''' Create dictionary with HHS region number and list of states in continental US in that region. Drawing state-level choropleths in ggplot2 requires a dataset with state names and the value for the choropleth.
	
	dict_region_state[season] = [state1 in region, state2, in region, ...]
	'''
	main(region_state_dictionary)
	
	dict_region_state = defaultdict(list)
	dict_region_state[1] = ["connecticut","maine","massachusetts","new hampshire","rhode island","vermont"]
	dict_region_state[2] = ["new york","new jersey"]
	dict_region_state[3] = ["delaware","district of columbia","maryland","pennsylvania","virginia","west virginia"]
	dict_region_state[4] = ["alabama", "florida","georgia","kentucky","mississippi","north carolina","south carolina","tennessee"]
	dict_region_state[5] = ["illinois","indiana","michigan","minnesota","ohio","wisconsin"]
	dict_region_state[6] = ["arkansas","louisiana","new mexico","oklahoma","texas"]
	dict_region_state[7] = ["iowa","kansas","missouri","nebraska"]
	dict_region_state[8] = ["colorado","montana","north dakota","south dakota","utah","wyoming"]
	dict_region_state[9] = ["arizona","california","nevada"]
	dict_region_state[10] = ["idaho","oregon","washington"]
	
	return dict_region_state

##############################################
def season_H3perc_CDC(csvreadfile):
	''' Import SQL_EXPORT/subtype5.csv data, which includes information on prominent subtype, subtypes of isolates that were identified, and isolates that match with the vaccine strains. Return a dictionary with season and proportion of H3 isolates of all isolates collected that season. The original source of isolate information is the CDC Flu Season Summaries, CDC surveillance system (not the WHO/NREVSS system).
	dict_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
	'''
	main(season_H3perc_CDC)
	
	dict_dummy = {}
	for row in csvreadfile:
		H1i, H3i, Bi, TOTi = float(row[4]), float(row[5]), float(row[6]), float(row[7])
		season = int(row[0]) # season number
		# include only seasons in pseasons in returned dictionary
		dict_dummy[season] = H3i/TOTi

	# dict_H3[seasonnum] = proportion H3 isolates of all isolates collected that season
	dict_H3 = dict((s, dict_dummy[s]) for s in pseasons)
	
	return dict_H3

##############################################
def season_H3perc_NREVSS(csvreadfile):
	''' Import My_Work/Clean_Data_for_Import/NREVSS_Isolates_Season_improved.csv data, which includes information on year, number of samples positive for flu, A samples, B samples, subtyped A samples, A/H1 samples, A/H3 samples, B samples, A/2009H1N1 samples, total speciments tested. Return a dictionary with season and proportion of H3 isolates of all subtyped flu isolates collected that season. The original source of isolate information is the CDC Flu Season Summaries, WHO NREVSS surveillance system (not the CDC system).
	dict_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
	'''
	main(season_H3perc_NREVSS)
	
	dict_dummy = {}
	for row in csvreadfile:
		A_H1, A_H3, A_09, B, H3N2v = int(row[2]), int(row[4]), int(row[5]), int(row[6]), int(row[7])
		TOTi = A_H1 + A_H3 + A_09 + B + H3N2v
		H3i = float(row[4])
		season = int(row[0]) - 2000 # season number
		# include only seasons in pseasons in returned dictionary
		dict_dummy[season] = H3i/TOTi

	# dict_H3[seasonnum] = proportion H3 isolates of all isolates collected that season
	dict_H3 = dict((s, dict_dummy[s]) for s in pseasons)
	
	return dict_H3

##############################################
def season_vaxmatch(csvreadfile):
	''' Import SQL_EXPORT/subtype5.csv data, which includes information on prominent subtype, subtypes of isolates that were identified, and isolates that match with the vaccine strains. Return a dictionary with season and proportion of isolates that match the trivalent vaccine of total isolates subtyped. The original source of isolate information is the CDC Flu Season Summaries, CDC surveillance system.
	dict_vaxmatch[seasonnum] = proportion of isolates matching the vaccine strain out of the total number of isolates subtyped.
	'''
	main(season_vaxmatch)
	
	dict_vaxmatch = {}
	for row in csvreadfile:
		# total isolates, matched isolates
		TOTi, TOTm = float(row[7]), float(row[11])
		season = int(row[0]) # season number
	
		dict_vaxmatch[season] = TOTm/TOTi

	return dict_vaxmatch

##############################################
def Thanksgiving_H3perc_NREVSS(csvreadfile):
	''' Import My_Bansal_Lab/Clean_Data_for_Import/NREVSS_Isolates_Thanksgiving.csv data, which includes information on seasons (eg. 2004 is 2003-04 season), total specimens tested, A/H1 samples, A/unable to subtype, A/H3 samples, A/2009H1N1 samples, B samples, H3N2v samples. Return a dictionary with season and proportion of H3 isolates of all subtyped flu isolates collected that season. The original source of isolate information is the CDC Flu Season Summaries, WHO NREVSS surveillance system (not the CDC system).
	dict_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
	'''
	main(Thanksgiving_H3perc_NREVSS)
	
	dict_dummy = {}
	for row in csvreadfile:
		a_H1, a_H3, a_09, B, H3N2v = int(row[2]), float(row[4]), int(row[5]), int(row[6]), int(row[7])
		TOTi = a_H1 + a_H3 + a_09 + B + H3N2v 
		season = int(row[0]) - 2000 # season number
		# include only seasons in pseasons in returned dictionary
		dict_dummy[season] = a_H3/TOTi

	# dict_H3[seasonnum] = proportion H3 isolates of all isolates collected that season
	dict_H3 = dict((s, dict_dummy[s]) for s in pseasons)
	
	return dict_H3

##############################################
def Thanksgiving_import(csv_Thanksgiving):
	''' Import Thanksgiving data from My_Bansal_Lab/ThanksgivingWeekData_cl.csv. Columns in dataset are year, week, total number of specimens, A/H1 samples, A/unable to subtype samples, A/H3 samples, A/2009H1N1 samples, A/no subtype information samples, B samples, A/H3N2v samples, percent of samples positive for flu, HHS region number, unique ID, season (the second calendar year of the flu season), date of the Sunday immediately preceding Thanksgiving. Return a dictionary with season to Sunday date of Thanksgiving week. These dates are used to determine which weeks fall under the early warning classification period.
	dict_Thanksgiving[seasonnum] = date of the Sunday immediately preceding Thanksgiving
	'''
	main(Thanksgiving_import)
	
	dict_Thanksgiving = {}
	for row in csv_Thanksgiving:
		week_og = row[14]
		Twk = date(int(week_og[6:]), int(week_og[:2]), int(week_og[3:5]))
		season = int(row[13])-2000 # 6/18/14, so season 1998 is converted to -2
		# dict_Thanksgiving[seasonnum] = date of the Sunday immediately preceding Thanksgiving
		dict_Thanksgiving[season] = Twk
		
	return dict_Thanksgiving

##############################################
def week_incidCA_processing(csv_incidence, csv_population):
	''' Import SQL_export/OR_allweeks_outpatient.csv data (or other OR_allweeks...csv data), which includes season number, week, age group, and ILI incid. Import SQL_export/totalpop_age.csv data, which includes calendar year, age group, and US population. Return dictionary with week to season number, week to child and adult ILI cases per 100,000 in total US population. Incidence rates for children, adults, and other age groups will be calculated based on popstat variable of the population in the second calendar year of the flu season (eg. 2001-02 season is based on 2002 population).
	dict_wk[week] = seasonnum
	dict_incid[week] = (child ILI cases per 100,000 in US population in second calendar year of flu season, adult incid per 100,000, other age group ILI cases per 100,000)
	'''
	main(week_incidCA_processing)
	
	## import ILI data ##
	# dict_ILI_week[(week, agegroup code)] = ILI cases; dict_wk[week] = seasonnum
	dict_ILI_week, dict_wk = {}, {}
	for row in csv_incidence: 
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		dict_ILI_week[(wk, str(row[2]))] = float(row[3])
		dict_wk[wk] = int(row[0])
	
	# define age group ranges
	age_keys = ['C', 'A', 'O']
	children = ['5-9 YEARS', '10-14 YEARS', '15-19 YEARS']
	adults = ['20-29 YEARS', '30-39 YEARS', '40-49 YEARS', '50-59 YEARS']
	other = ['<2 YEARS', '2-4 YEARS', '60-69 YEARS', '70-79 YEARS', '80 YEARS']
	dict_ages = defaultdict(list)
	# dict_ages[agegroup code] = [agegroup bin 1, age group bin 2,... in text]
	dict_ages = dict(zip(age_keys, [children, adults, other]))
	
	# fill dict_ILI_week with 0 if ILI cases for a certain age group are missing
	print 'missing ILI wks and ages'
	for wk, age in product(dict_wk, age_keys):
		if (wk, age) not  in dict_ILI_week:
			print (wk, age)
			dict_ILI_week[(wk, age)] = float(0)

	## import population data ##
	dict_pop_age = {}
	for row in csv_population:
		calendar_year = str(row[0])
		season = int(calendar_year[2:])
		age = row[1]
		# dict_pop_age[(seasonnum, age in text)] = population
		dict_pop_age[(season, age.upper())] = int(row[2]) 
	
	# dict_pop[(season, agegroup code)] = population size of agegroup
	seasons = list(set([k[0] for k in dict_pop_age]))
	age_texts = list(set([k[1] for k in dict_pop_age])) # age bins
	dict_pop = {}
	for s, ak in product(seasons, age_keys):
		dict_pop[(s, ak)] = float(sum([dict_pop_age[(s, at)] for at in age_texts if at in dict_ages[ak]]))
	
	# generate incidence per 100,000 in US population and OR at the weekly level
	dict_incid = {}
	for wk in dict_wk:
		s = dict_wk[wk]
		# dict_incid[week] = (child incid per 100,000, adult incid per 100,000, other incid per 1000,000)
		child_incid = dict_ILI_week[(wk, 'C')]/dict_pop[(s, 'C')]*100000
		adult_incid = dict_ILI_week[(wk, 'A')]/dict_pop[(s, 'A')]*100000
		other_incid = dict_ILI_week[(wk, 'O')]/dict_pop[(s, 'O')]*100000 # added 7/6/14
		dict_incid[wk] = (child_incid, adult_incid, other_incid)
	
	return dict_wk, dict_incid



##############################################
def week_OR_processing(csv_incidence, csv_population):
	''' Import SQL_export/OR_allweeks_outpatient.csv data (or other OR_allweeks...csv data), which includes season number, week, age group, and ILI incid. Import SQL_export/totalpop_age.csv data, which includes calendar year, age group, and US population. Return dictionary with week to season number, week to ILI cases per 100,000 in total US population, and dictionary with week to OR. OR attack rates for children and adults will be calculated based on popstat variable of the population in the second calendar year of the flu season (eg. 2001-02 season is based on 2002 population).
	dict_wk[week] = seasonnum
	dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season
	dict_OR[week] = OR
	'''
	main(week_OR_processing)
	
	## import ILI data ##
	# dict_ILI_week[(week, agegroup code)] = ILI cases; dict_wk[week] = seasonnum
	dict_ILI_week, dict_wk = {}, {}
	for row in csv_incidence: 
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		dict_ILI_week[(wk, str(row[2]))] = float(row[3])
		dict_wk[wk] = int(row[0])
	
	# define age group ranges
	age_keys = ['C', 'A', 'O']
	children = ['5-9 YEARS', '10-14 YEARS', '15-19 YEARS']
	adults = ['20-29 YEARS', '30-39 YEARS', '40-49 YEARS', '50-59 YEARS']
	other = ['<2 YEARS', '2-4 YEARS', '60-69 YEARS', '70-79 YEARS', '80 YEARS']
	dict_ages = defaultdict(list)
	# dict_ages[agegroup code] = [agegroup bin 1, age group bin 2,... in text]
	dict_ages = dict(zip(age_keys, [children, adults, other]))
	
	## import population data ##
	dict_pop_age = {}
	for row in csv_population:
		calendar_year = str(row[0])
		season = int(calendar_year[2:])
		age = row[1]
		# dict_pop_age[(seasonnum, age in text)] = population
		dict_pop_age[(season, age)] = int(row[2]) 
	
	# dict_pop[(season, agegroup code)] = population size of agegroup
	seasons = list(set([k[0] for k in dict_pop_age]))
	age_texts = list(set([k[1] for k in dict_pop_age])) # age bins
	dict_pop = {}
	for s, ak in product(seasons, age_keys):
		dict_pop[(s, ak)] = float(sum([dict_pop_age[(s, at)] for at in age_texts if at in dict_ages[ak]]))
	
	# generate incidence per 100,000 in US population and OR at the weekly level
	dict_incid, dict_OR = {}, {}
	for wk in dict_wk:
		s = dict_wk[wk]
		# dict_incid[week] = ILI incidence per 100,000 in US pop in second calendar year of flu season
		tot_incid = sum([dict_ILI_week[(wk, age)] for age in age_keys])/sum([dict_pop[(s, age)] for age in age_keys]) * 100000
		dict_incid[wk] = tot_incid
		child_attack = dict_ILI_week[(wk, 'C')]/dict_pop[(s, 'C')]
		adult_attack = dict_ILI_week[(wk, 'A')]/dict_pop[(s, 'A')]
		# 6/24/14: OR cannot be evaluated if child or adult incidence in a week is zero. Assign OR = NA if one of those conditions is met.
		if not child_attack or not adult_attack:
			OR = 'nan'
		else:
			OR = (child_attack/(1-child_attack))/(adult_attack/(1-adult_attack))
		# dict_OR[week] = OR
		dict_OR[wk] = float(OR)
	
	return dict_wk, dict_incid, dict_OR

##############################################
def week_OR_processing_region(csv_incidence_region, csv_population_region):
	''' Import R_export/OR_zip3_week_outpatient_cl.csv data, which includes season number, week, zip3, age group, and ILI incid. Import R_export/popstat_zip3_season_cl.csv data, which includes calendar year, uqsza, popstat, season, age group, state, lat, long, and HHS region. Return dictionaries with week to season number, zip3 to state and hhs region number, (week, hhs region) to total ILI incidence per popstat in 2nd calendar year of flu season, and (week, hhs region) to OR. OR attack rates for children and adults will be calculated based on popstat variable of the population in the second calendar year of the flu season within that region (eg. 2001-02 season is based on 2002 population). 
	dict_wk[week] = seasonnum
	dict_zip3_reg[zip3] = (state, hhsreg)
	dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season
	dict_OR_reg[(week, hhsreg)] = OR
	'''
	main(week_OR_processing_region)
	
	## import population data ##
	dict_pop_zip3_age, dict_zip3_reg = {}, {}
	for row in csv_population_region:
		season, zip3, age, pop = int(row[3]), str(row[0]), str(row[4]), int(row[2])
		state, hhs = str(row[5]), int(row[8])
		# dict_pop_zip3_age[(seasonnum, zip3, agegroup)] = population size in second calendar year of flu season
		dict_pop_zip3_age[(season, zip3, age)] = pop
		# dict_zip3_reg[zip3] = (state, hhs region number)
		dict_zip3_reg[zip3] = (state, hhs)
	
	age_keys = list(set([k[2] for k in dict_pop_zip3_age]))
	
	dict_pop_age = {}
	for s, h, ak in product(pseasons, gp_plotting_regions, age_keys):
		# dict_pop_age[(seasonnum, hhs, agegroup code)] = population size in second calendar year of flu season
		dict_pop_age[(s, h, ak)] = float(sum([dict_pop_zip3_age[(s, z, ak)] for z in dict_zip3_reg if dict_zip3_reg[z][1] == h]))
	
	## import ILI data ##
	dict_ILI_week, dict_wk = {}, {}
	for row in csv_incidence_region: 
		week, season = row[1], int(row[0])
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		zip3, age, ili = str(row[2]), str(row[3]), int(row[4])
		hhs = int(dict_zip3_reg[zip3][1])
		# dict_wk[week] = seasonnum
		dict_wk[wk] = season
		# dict_ILI_week[(week, hhs region number, agegroup code)] = ILI cases 
		if (wk, hhs, age) in dict_ILI_week:
			new_value = dict_ILI_week[(wk, hhs, age)] + ili
			dict_ILI_week[(wk, hhs, age)] = new_value
		else:
			dict_ILI_week[(wk, hhs, age)] = ili
	
	# subset dict_wk so that it includes only weeks with plotting seasons
	dict_wk_sub = dict((k, dict_wk[k]) for k in dict_wk if dict_wk[k] in pseasons) 
	
	# generate OR by region at the weekly level
	dict_incid_reg, dict_OR_reg = {}, {}
	for wk, r in product(dict_wk_sub, gp_plotting_regions):
		s = dict_wk_sub[wk]
		# dict_incid_reg[(week, region)] = total ILI incidence per 100,000 per popstat in second calendar year of the flu season
		tot_incid = sum([dict_ILI_week[(wk, r, age)] for age in age_keys])/sum([dict_pop_age[(s, r, age)] for age in age_keys]) * 100000
		dict_incid_reg[(wk, r)] = tot_incid
		
		child_attack = dict_ILI_week[(wk, r, 'C')]/dict_pop_age[(s, r, 'C')]
		adult_attack = dict_ILI_week[(wk, r, 'A')]/dict_pop_age[(s, r, 'A')]
		# 6/24/14: OR cannot be evaluated if child or adult incidence in a week is zero. Assign OR = NA if one of those conditions is met.
		if not child_attack or not adult_attack:
			OR = 'nan'
		else:
			OR = (child_attack/(1-child_attack))/(adult_attack/(1-adult_attack))	
		# dict_OR_reg[(week, region)] = OR
		dict_OR_reg[(wk, r)] = float(OR)
			
	return dict_wk_sub, dict_zip3_reg, dict_incid_reg, dict_OR_reg

##############################################
def week_OR_processing_state(csv_incidence_region, csv_population_region):
	''' Import R_export/OR_zip3_week_outpatient_cl.csv data, which includes season number, week, zip3, age group, and ILI incid. Import R_export/popstat_zip3_season_cl.csv data, which includes calendar year, uqsza, popstat, season, age group, state, lat, long, and HHS region. Return dictionaries with week to season number, zip3 to state and hhs region number, (week, state) to total ILI incidence per popstat in 2nd calendar year of flu season, and (week, state) to OR. OR attack rates for children and adults will be calculated based on popstat variable of the population in the second calendar year of the flu season within that region (eg. 2001-02 season is based on 2002 population). 
	dict_wk[week] = seasonnum
	dict_zip3_reg[zip3] = (state, hhsreg)
	dict_incid_state[(week, state)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season
	dict_OR_state[(week, state)] = OR
	6/23/14: state level analyses take precedence over HHS region level ones
	'''
	main(week_OR_processing_state)
	
	## import population data ##
	dict_pop_zip3_age, dict_zip3_reg = {}, {}
	for row in csv_population_region:
		season, zip3, age, pop = int(row[3]), str(row[0]), str(row[4]), int(row[2])
		state, hhs = str(row[5]), int(row[8])
		# dict_pop_zip3_age[(seasonnum, zip3, agegroup)] = population size in second calendar year of flu season
		dict_pop_zip3_age[(season, zip3, age)] = pop
		# dict_zip3_reg[zip3] = (state, hhs region number)
		dict_zip3_reg[zip3] = (state, hhs)
	
	age_keys = list(set([k[2] for k in dict_pop_zip3_age])) # A, C, O
	state_keys = list(set([dict_zip3_reg[k][0] for k in dict_zip3_reg]))
	
	dict_pop_age = {}
	for s, state, ak in product(pseasons, state_keys, age_keys):
		# dict_pop_age[(seasonnum, state, agegroup code)] = population size in second calendar year of flu season
		dict_pop_age[(s, state, ak)] = float(sum([dict_pop_zip3_age[(s, z, ak)] for z in dict_zip3_reg if dict_zip3_reg[z][0] == state]))
	
	## import ILI data ##
	dict_ILI_week, dict_wk = {}, {}
	for row in csv_incidence_region: 
		week, season = row[1], int(row[0])
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		zip3, age, ili = str(row[2]), str(row[3]), int(row[4])
		state = str(dict_zip3_reg[zip3][0])
		# dict_wk[week] = seasonnum
		dict_wk[wk] = season
		# dict_ILI_week[(week, state, agegroup code)] = ILI cases 
		if (wk, state, age) in dict_ILI_week:
			new_value = dict_ILI_week[(wk, state, age)] + ili # sum ili cases for all zip3s in a single state
			dict_ILI_week[(wk, state, age)] = new_value
		else:
			dict_ILI_week[(wk, state, age)] = ili
	
	# subset dict_wk so that it includes only weeks with plotting seasons
	# dict_wk_sub[week] = seasonnum
	dict_wk_sub = dict((k, dict_wk[k]) for k in dict_wk if dict_wk[k] in pseasons) 

	ct = 0
	print 'size of dict_ILI_week', len(dict_ILI_week)
	for wk, state, age in product(dict_wk_sub, state_keys, age_keys):
		if (wk, state, age) not in dict_ILI_week:
			ct += 1
			dict_ILI_week[(wk, state, age)] = 0
	print 'wk, state, agecode combinations not in dict_ILI_week', ct

	# generate OR by region at the weekly level
	dict_incid_state, dict_OR_state = {}, {}
	for wk, state in product(dict_wk_sub, state_keys):
		snum = dict_wk_sub[wk]
		# dict_incid_state[(week, state)] = total ILI incidence per 100,000 per popstat in second calendar year of the flu season
		tot_incid = sum([dict_ILI_week[(wk, state, age)] for age in age_keys])/sum([dict_pop_age[(snum, state, age)] for age in age_keys]) * 100000
		dict_incid_state[(wk, state)] = tot_incid
		# weekly child and adult incidence rates by population of children and adults that season
		child_attack = dict_ILI_week[(wk, state, 'C')]/dict_pop_age[(snum, state, 'C')]
		adult_attack = dict_ILI_week[(wk, state, 'A')]/dict_pop_age[(snum, state, 'A')]
		# 6/24/14: OR cannot be evaluated if child or adult incidence in a week is zero. Assign OR = NA if one of those conditions is met.
		if not child_attack or not adult_attack:
			OR = 'nan'
		else:
			OR = (child_attack/(1-child_attack))/(adult_attack/(1-adult_attack))	
		# dict_OR_state[(week, state)] = OR
		dict_OR_state[(wk, state)] = float(OR)
			
	return dict_wk_sub, dict_zip3_reg, dict_incid_state, dict_OR_state

##############################################
def week_plotting_dicts(dict_wk, dict_incid, dict_OR, dict_zOR):
	'''Return dictionaries for season to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. The week_zOR_processing function must be run before this one. SDI source files for csv_incidence and csv_population are 'SQL_export/OR_allweeks_outpatient.csv' and 'SQL_export/totalpop_age.csv' respectively. ILINet source files for csv_incidence and csv_population are 'CDC_Source/Import_Data/all_cdc_source_data.csv' and 'Census/Import_Data/totalpop_age_Census_98-14.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(week_plotting_dicts)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population, dict_OR[week] = OR; dict_zOR[week] = zOR
	
	dict_incid53ls, dict_OR53ls, dict_zOR53ls = defaultdict(list), defaultdict(list), defaultdict(list)
	for s in pseasons:
		incid53dummy = [dict_incid[wk] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		OR53dummy = [dict_OR[wk] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		zOR53dummy = [dict_zOR[wk] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		if len(incid53dummy) == 52:
			a53incid = (incid53dummy[12]+incid53dummy[13])/2.
			a53OR = (OR53dummy[12]+OR53dummy[13])/2.
			a53zOR = (zOR53dummy[12]+zOR53dummy[13])/2.
			incid53dummy.insert(13, a53incid)
			OR53dummy.insert(13, a53OR)
			zOR53dummy.insert(13, a53zOR)
		# dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...]
		# dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...]
		# dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
		dict_incid53ls[s] = incid53dummy
		dict_OR53ls[s] = OR53dummy
		dict_zOR53ls[s] = zOR53dummy
	
	return dict_incid53ls, dict_OR53ls, dict_zOR53ls

##############################################
def week_plotting_dicts_region(dict_wk, dict_incid_reg, dict_OR_reg, dict_zOR_reg):
	'''Return dictionaries for (season, region) to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. The week_zOR_processing_region function must be run before this one. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. 
	dict_wk[week] = seasonnum
	dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(week_plotting_dicts_region)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_reg[(week, hhsreg)] = OR, dict_zOR_reg[(week, hhsreg)] = zOR

	dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg = defaultdict(list), defaultdict(list), defaultdict(list)
	for s, r in product(pseasons, gp_plotting_regions):
		incid53dummy = [dict_incid_reg[(wk, r)] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		OR53dummy = [dict_OR_reg[(wk, r)] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		zOR53dummy = [dict_zOR_reg[(wk, r)] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		if len(incid53dummy) == 52:
			a53incid = (incid53dummy[12]+incid53dummy[13])/2.
			a53OR = (OR53dummy[12]+OR53dummy[13])/2.
			a53zOR = (zOR53dummy[12]+zOR53dummy[13])/2.
			incid53dummy.insert(13, a53incid)
			OR53dummy.insert(13, a53OR)
			zOR53dummy.insert(13, a53zOR)
		# dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...]
		# dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...
		# dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
		dict_incid53ls_reg[(s, r)] = incid53dummy
		dict_OR53ls_reg[(s, r)] = OR53dummy
		dict_zOR53ls_reg[(s, r)] = zOR53dummy
	
	return dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg

##############################################
def week_plotting_dicts_state(dict_wk, dict_incid_state, dict_OR_state, dict_zOR_state):
	'''Return dictionaries for (season, state) to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. The week_zOR_processing_state function must be run prior to this function. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. 
	dict_wk[week] = seasonnum
	dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls_state[(seasonnum, state)] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(week_plotting_dicts_state)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_state[(week, state)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_state[(week, state)] = OR, dict_zOR_reg[(week, state)] = zOR

	state_keys = list(set([k[1] for k in dict_incid_state]))

	dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state = defaultdict(list), defaultdict(list), defaultdict(list)
	for s, state in product(pseasons, state_keys):
		incid53dummy = [dict_incid_state[(wk, state)] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		OR53dummy = [dict_OR_state[(wk, state)] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		zOR53dummy = [dict_zOR_state[(wk, state)] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		if len(incid53dummy) == 52:
			a53incid = (incid53dummy[12]+incid53dummy[13])/2.
			a53OR = (OR53dummy[12]+OR53dummy[13])/2.
			a53zOR = (zOR53dummy[12]+zOR53dummy[13])/2.
			incid53dummy.insert(13, a53incid)
			OR53dummy.insert(13, a53OR)
			zOR53dummy.insert(13, a53zOR)
		# dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...]
		# dict_OR53ls_state[(seasonnum, state)] = [OR wk 40, OR wk 41, ...
		# dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
		dict_incid53ls_state[(s, state)] = incid53dummy
		dict_OR53ls_state[(s, state)] = OR53dummy
		dict_zOR53ls_state[(s, state)] = zOR53dummy
	
	return dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state

##############################################
def week_zOR_processing(dict_wk, dict_OR):
	''' Calculate zOR by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. The function week_OR_processing function must be run before this function. Return dictionaries of week to season number, week to OR, and week to zOR. SDI source files for csv_incidence and csv_population are 'SQL_export/OR_allweeks_outpatient.csv' and 'SQL_export/totalpop_age.csv' respectively. ILINet source files for csv_incidence and csv_population are 'CDC_Source/Import_Data/all_cdc_source_data.csv' and 'Census/Import_Data/totalpop_age_Census_98-14.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season
	dict_OR[week] = OR
	dict_zOR[week] = zOR
	'''
	main(week_zOR_processing)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
	
	dict_zOR = {}
	for s in pseasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR[wk] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR[wk] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR[wk]-season_mean)/season_sd for wk in weekdummy] #/season_sd
		for w, z in zip(weekdummy, list_dictdummy):
			dict_zOR[w] = z
	
	return dict_zOR

##############################################
def week_zOR_processing_pandemic(dict_wk, dict_OR, baseline_text):
	''' Calculate zOR by week with choice of different baselines: 'between pandemic waves', 'last season BL', or 'after pandemic'. The function week_OR_processing function must be run before this function. Return dictionaries of week to season number, week to OR, and week to zOR. SDI source files for csv_incidence and csv_population are 'SQL_export/OR_allweeks_outpatient.csv' and 'SQL_export/totalpop_age.csv' respectively. ILINet source files for csv_incidence and csv_population are 'CDC_Source/Import_Data/all_cdc_source_data.csv' and 'Census/Import_Data/totalpop_age_Census_98-14.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season
	dict_OR[week] = OR
	dict_zOR[week] = zOR with pandemic baseline
	'''
	main(week_zOR_processing_pandemic)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
	
	dict_zOR = {}
	for s in pseasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		# weeks from prior season
		weekdummypre = sorted([key for key in dict_wk if dict_wk[key] == s-1])
		if baseline_text == 'between pandemic waves':
			# week indexes of 2008-09 season that occurred between pandemic waves (weeks 26-32, indexes 39:45)
			season_mean = np.mean([dict_OR[wk] for wk in weekdummypre[39:46]])
			season_sd = np.std([dict_OR[wk] for wk in weekdummypre[39:46]])
			list_dictdummy = [(dict_OR[wk]-season_mean)/season_sd for wk in weekdummy] #/season_sd
		elif baseline_text == 'last season baseline':
			season_mean = np.mean([dict_OR[wk] for wk in weekdummypre[:gp_normweeks]])
			season_sd = np.std([dict_OR[wk] for wk in weekdummypre[:gp_normweeks]])
			list_dictdummy = [(dict_OR[wk]-season_mean)/season_sd for wk in weekdummy] #/season_sd
		elif baseline_text == 'after pandemic':
			season_mean = np.mean([dict_OR[wk] for wk in weekdummy[8:]])
			season_sd = np.std([dict_OR[wk] for wk in weekdummy[8:]])
			list_dictdummy = [(dict_OR[wk]-season_mean)/season_sd for wk in weekdummy] #/season_sd
		for w, z in zip(weekdummy, list_dictdummy):
			dict_zOR[w] = z
	
	return dict_zOR

##############################################
def week_zOR_processing_region(dict_wk, dict_OR_reg):
	''' Calculate zOR for each region by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. Each region is z-normalized by the first normweeks weeks of OR data for that region. The function 'week_OR_processing_region' must be run before this function. Return dictionaries of week to season number, zip3 to state and region, (week, region) to incidence, (week, region) to OR, and (week, region) to zOR.
	dict_wk[week] = seasonnum
	dict_zip3_reg[zip3] = (state, hhsreg)
	dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season
	dict_OR_reg[(week, hhsreg)] = OR
	dict_zOR_reg[(week, hhsreg)] = zOR
	'''
	main(week_zOR_processing_region)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_reg[(week, hhsreg)] = OR
		
	dict_zOR_reg = {}
	for s, r in product(pseasons, gp_plotting_regions):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR_reg[(wk, r)] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR_reg[(wk, r)] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR_reg[(wk, r)]-season_mean)/season_sd for wk in weekdummy]
		for w, zOR in zip(weekdummy, list_dictdummy):
			dict_zOR_reg[(w, r)] = zOR
	
	return dict_zOR_reg

##############################################
def week_zOR_processing_state(dict_wk, dict_OR_state):
	''' Calculate zOR for each state by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. Each region is z-normalized by the first normweeks weeks of OR data for that state. The function 'week_OR_processing_state' must be run before this function. Return dictionaries of week to season number, zip3 to state and region, (week, state) to incidence, (week, state) to OR, and (week, state) to zOR.
	dict_wk[week] = seasonnum
	dict_zip3_reg[zip3] = (state, hhsreg)
	dict_incid_state[(week, state)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season
	dict_OR_state[(week, state)] = OR
	dict_zOR_state[(week, state)] = zOR
	'''
	main(week_zOR_processing_state)
		
	state_keys = list(set([k[1] for k in dict_OR_state]))

	dict_zOR_state = {}
	for s, state in product(pseasons, state_keys):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR_state[(wk, state)] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR_state[(wk, state)] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR_state[(wk, state)]-season_mean)/season_sd for wk in weekdummy]
		for w, zOR in zip(weekdummy, list_dictdummy):
			dict_zOR_state[(w, state)] = zOR
	
	return dict_zOR_state


##############################################
##############################################
# footer

def main(function):
	print 'Running', __name__, function.__name__

if __name__ == '__main__':
	print 'Executed from the command line'
	main()