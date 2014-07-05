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

##############################################
# global parameters - methods

## SDI data ##
gp_normweeks = 7 # number of weeks in baseline normalization period
gp_fluweeks = 34 # number of weeks in flu season (weeks 40-20)
gp_retro_duration = 2 # duration of retrospective period in weeks
gp_begin_retro_week = 3 # number of weeks before the peak incidence week that the retrospective period should begin (that season only)
gp_early_duration = 2 # duration of the early warning period in weeks
gp_begin_early_week = 2 # number of weeks after the week with Thanksgiving that the early warning period should begin (that season only)
gp_plotting_seasons = xrange(2,10) # season numbers for which data will be plotted (eg. Season 2 = 2001-02)
gp_plotting_regions = xrange(1, 11) # region numbers
gp_mild =[3, 6, 7, 9] # seasons 3, 6, 7, 9
gp_mod = [2, 5] # seasons 2, 5
gp_sev = [4, 8] # seasons 4, 8, 10 (pandemic)

## ILINet data ## 
gp_ILINet_plotting_seasons = range(-2, 10) + range(11,15) # remove 2009-10 data

##############################################
# global parameters - plotting

## SDI data ##
gp_seasonlabels = ['01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09']
gp_colors_1_10 = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
gp_colors = ['black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet']
gp_regions = ['Boston (R1)', 'New York (R2)', 'Philadelphia (R3)', 'Atlanta (R4)', 'Chicago (R5)', 'Dallas (R6)', 'Kansas City (R7)', 'Denver (R8)', 'San Francisco (R9)', 'Seattle (R10)']
gp_weeklabels = range(40,54) # week number labels for plots vs. time
gp_weeklabels.extend(range(1,40))
gp_severitylabels = ['Mild', 'Moderate', 'Severe']
gp_severitycolors = ['y', 'b', 'r']
gp_line_style = ['-', ':']

## ILINet data ##
gp_ILINet_seasonlabels = ['97-98', '98-99', '99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '10-11', '11-12', '12-13', '13-14']
gp_ILINet_colors = cm.rainbow(np.linspace(0, 1, len(gp_ILINet_seasonlabels)))


##############################################
def benchmark_import (csv_cdcseverity, index_col):
	''' Import CDC_Source/Import_Data/cdc_severity_index.csv data, which includes z-normalized contributors to CDC severity index. These data include: percent of positive flu lab tests, proportion of mortality due to P&I, pediatric deaths, proportion of ILI, 5-17 years hospitalization rate, and 18-49 years hospitalization rate. All data sources are not available for every season. Return dictionary with season to benchmark index value.
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
		year, week, season = int(row[1][2:]), int(row[2]), str(row[12])
		PI_deaths, allcoz_deaths = row[19], row[13]
		ILI, allpatients = row[17], row[18]
		CHR = str(row[26])
		
		if season == 'NA':
			# season variable is noted only for seasons in SDI dataset along the sequence such that the 2001-02 flu season is season 2, etc.
			season = 0
		if int(season) in gp_plotting_seasons:
			# dict_deaths_ILI_counts[(seasonnum, weeknum)] = (P&I deaths, all deaths, ILI cases, total patients)
			dict_deaths_ILI_counts[(int(season), week)] = (PI_deaths, allcoz_deaths, ILI, allpatients)
		
		# grab cumulative hospitalization rate at week 17 in each plotting season
		if year in gp_plotting_seasons and week == 17:
			# for seasons prior to 2003-04, CHR should be float('nan')
			if CHR == 'NA':
				CHR = float('nan')
			# dict_CHR[seasonnum] = cumulative lab-confirmed case-hospitalization rate per 100,000 individuals in population over the period from week 40 to week 17 during flu season
			dict_CHR[year] = float(CHR)
		
	# subset dict_deaths_ILI_counts for weeks that will contribute to each season's P&I mortality and ILI proportion rates (weeks 40 to 20)
	dict_deaths_ILI_counts_fluwks = dict([(k, dict_deaths_ILI_counts[k]) for k in dict_deaths_ILI_counts if k[1]>20 and k[1]<40])
	
	# sum PI_deaths, allcoz_deaths, ILI, allpatients for each season 
	dict_deaths, dict_ILI, dict_CFR = {}, {}, {}
	for s in gp_plotting_seasons:
		
		# dict_deaths[seasonnum] = (P&I deaths from wks 40 to 20, all cause deaths from wks to 40 to 20)
		dict_deaths[s] = (sum([float(dict_deaths_ILI_counts_fluwks[k][0]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]), sum([int(dict_deaths_ILI_counts_fluwks[k][1]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]))
		
		# dict_ILI[seasonnum] = (ILI cases from wks 40 to 20, all patients from wks 40 to 20)
		dict_ILI[s] = (sum([float(dict_deaths_ILI_counts_fluwks[k][2]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]), sum([int(dict_deaths_ILI_counts_fluwks[k][2]) for k in dict_deaths_ILI_counts_fluwks if k[0] == s]))
		
		# dict_CFR[seasonnum] = P&I deaths of all flu season deaths in 122 cities/outpatient ILI cases of all flu season patient visits to outpatient offices in ILINet
		dict_CFR[s] = (dict_deaths[s][0]/dict_deaths[s][1])/(dict_ILI[s][0]/dict_ILI[s][1])
	
	return dict_CHR, dict_CFR, dict_deaths, dict_ILI

##############################################
def classif_zOR_index(csv_incidence, csv_population, csv_Thanksgiving, csv_incidence_region, csv_population_region, retro_level_string):
	''' Find the retrospective and early warning period start weeks by season. The retrospective period may be designated in two manners -- relative to the national peak incidence week or regional peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving. This function returns a dictionary that can be used by classif_zOR_region_processing to set the classification periods for each region to that which was defined at the national level.
	The week_plotting_dicts and Thanksgiving_import functions are nested within this function. Return dictionary for season to (index of first retro period week, index of first early warning period week).
	dict_classifindex[seasonnum] = (index of first retro period week, index of first early warning period week)
	'''
	main(classif_zOR_index)

	# for nation-level peak-based retrospective classification
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls = week_plotting_dicts(csv_incidence, csv_population)
	# for region-level peak-based retrospective classification
	# (don't want to call dict_wk twice), dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
	_, dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg = week_plotting_dicts_region(csv_incidence_region, csv_population_region)
		
	dict_classifindex = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)

	for s, r in product(gp_plotting_seasons, gp_plotting_regions):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		
		# nation-lvl peak-based retrospective classification
		if retro_level_string == 'nation':
			peak_index = dict_incid53ls[s].index(max(dict_incid53ls[s]))
			begin_retro = peak_index - gp_begin_retro_week
		
		# region-lvl peak-based retrospective classif
		elif retro_level_string == 'region':
			peak_index = dict_incid53ls_reg[(s, r)].index(max(dict_incid53ls_reg[(s, r)]))
			begin_retro = peak_index - gp_begin_retro_week
		
		else:
			print 'retro_level_string error'
			break
		
		# Thanksgiving-based early warning classification
		Thx_index = weekdummy.index(dict_Thanksgiving[s])
		begin_early = Thx_index + gp_begin_early_week
		
		# dict_classifindex[(seasonnum, region)] = (index of first retro period week, index of first early warning period week)
		dict_classifindex[(s, r)] = (begin_retro, begin_early)
		
	return dict_classifindex, dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls, dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg
	
##############################################
def classif_zOR_index_state(csv_incidence, csv_population, csv_Thanksgiving, csv_incidence_region, csv_population_region, retro_level_string):
	''' Find the retrospective and early warning period start weeks by season. The retrospective period may be designated in two manners -- relative to the national peak incidence week or regional peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving. This function returns a dictionary that can be used by classif_zOR_region_processing to set the classification periods for each region to that which was defined at the national level.
	The week_plotting_dicts and Thanksgiving_import functions are nested within this function. Return dictionary for season to (index of first retro period week, index of first early warning period week).
	dict_classifindex[seasonnum] = (index of first retro period week, index of first early warning period week)
	'''
	main(classif_zOR_index_state)

	# for nation-level peak-based retrospective classification
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls = week_plotting_dicts(csv_incidence, csv_population)
	# for region-level peak-based retrospective classification
	# (don't want to call dict_wk twice), dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_state[(seasonnum, state)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
	_, dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state = week_plotting_dicts_state(csv_incidence_region, csv_population_region)
		
	dict_classifindex = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)

	# states in state-level analysis
	state_keys = list(set([k[1] for k in dict_incid53ls_state]))
	
	for s, state in product(gp_plotting_seasons, state_keys):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		
		# nation-lvl peak-based retrospective classification
		if retro_level_string == 'nation':
			peak_index = dict_incid53ls[s].index(max(dict_incid53ls[s]))
			begin_retro = peak_index - gp_begin_retro_week
		
		# state-lvl peak-based retrospective classif
		elif retro_level_string == 'state':
			peak_index = dict_incid53ls_state[(s, state)].index(max(dict_incid53ls_state[(s, state)]))
			begin_retro = peak_index - gp_begin_retro_week
		
		else:
			print 'retro_level_string error'
			break
		
		# Thanksgiving-based early warning classification
		Thx_index = weekdummy.index(dict_Thanksgiving[s])
		begin_early = Thx_index + gp_begin_early_week
		
		# dict_classifindex[(seasonnum, state)] = (index of first retro period week, index of first early warning period week)
		dict_classifindex[(s, state)] = (begin_retro, begin_early)
		
	return dict_classifindex, dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls, dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state

##############################################
def classif_zOR_processing(csv_incidence, csv_population, csv_Thanksgiving):
	''' Calculate retrospective and early warning zOR classification values for each season, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period is designated relative to the peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The week_plotting_dicts and Thanksgiving_import functions are nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR.
	dict_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zOR_processing)
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls = week_plotting_dicts(csv_incidence, csv_population)
	
	dict_classifzOR = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)
	
	for s in gp_plotting_seasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		
		# peak-based retrospective classification
		peak_index = dict_incid53ls[s].index(max(dict_incid53ls[s]))
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
def classif_zOR_region_processing(csv_incidence, csv_population, csv_Thanksgiving, csv_incidence_region, csv_population_region, retro_level_string):
	''' Calculate retrospective and early warning zOR classification values for each season and region combination, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period may be designated in two manners -- relative to the national peak incidence week or regional peak incidence week in the flu season.The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The week_plotting_dicts_region, classif_zOR_index, and Thanksgiving_import functions are nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR.
	dict_classifzOR_reg[(seasonnum, region)] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zOR_region_processing)
	

	# dict_classifindex[(seasonnum, region)] = (index of first retro period week, index of first early warning period week), dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...], dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
	dict_classifindex, dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls, dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg = classif_zOR_index(csv_incidence, csv_population, csv_Thanksgiving, csv_incidence_region, csv_population_region, retro_level_string)
	
	dict_classifzOR_reg = {}
	
	for s, r in product(gp_plotting_seasons, gp_plotting_regions):
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
def classif_zOR_state_processing(csv_incidence, csv_population, csv_Thanksgiving, csv_incidence_region, csv_population_region, retro_level_string):
	''' Calculate retrospective and early warning zOR classification values for each season and state combination, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period may be designated in two manners -- relative to the national peak incidence week or state peak incidence week in the flu season.The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The week_plotting_dicts_state, classif_zOR_index, and Thanksgiving_import functions are nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR.
	dict_classifzOR_state[(seasonnum, state)] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zOR_state_processing)
	

	# dict_classifindex[(seasonnum, state)] = (index of first retro period week, index of first early warning period week), dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...], dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...], dict_OR53ls_state[(seasonnum, stat)] = [OR wk 40, OR wk 41, ...], dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
	dict_classifindex, dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls, dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state = classif_zOR_index_state(csv_incidence, csv_population, csv_Thanksgiving, csv_incidence_region, csv_population_region, retro_level_string)
	
	dict_classifzOR_state = {}
	
	# states in state-level analysis
	state_keys = list(set([k[1] for k in dict_incid53ls_state]))

	for s, state in product(gp_plotting_seasons, state_keys):
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
def ILINet_classif_zOR_processing(csv_incidence, csv_population, csv_Thanksgiving):
	''' Calculate retrospective and early warning zOR classification values for each season, which is the mean zOR for the duration of the retrospective and early warning periods, respectively. The retrospective period is designated relative to the peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zOR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zOR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The week_plotting_dicts and Thanksgiving_import functions are nested within this function. Return dictionaries for week to season, week to OR, week to zOR, season to mean retrospective and early warning zOR. ILINet data
	dict_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(ILINet_classif_zOR_processing)
	# dict_wk[week] = seasonnum, dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...], dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...], dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls = ILINet_week_plotting_dicts(csv_incidence, csv_population)
	
	dict_ILINet_classifzOR = {}
	
	# import Thanksgiving data
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving)
	
	for s in gp_ILINet_plotting_seasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		
		# peak-based retrospective classification
		peak_index = dict_incid53ls[s].index(max(dict_incid53ls[s]))
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
	
		# dict_ILINet_classifzOR[seasonnum] = (mean retrospective zOR, mean early warning zOR)
		dict_ILINet_classifzOR[s] = (mean_retro_zOR, mean_early_zOR)
		
	return dict_ILINet_classifzOR

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
		wktime = datetime.strptime(week, '%Y%U%w') # format = 4-dig year, 2-dig week beginning on Sunday, digit representing day of week
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
def ILINet_week_plotting_dicts(csv_incidence, csv_population):
	'''Return dictionaries for season to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. Source files for csv_incidence and csv_population are 'CDC_Source/Import_Data/all_cdc_source_data.csv' and 'Census/Import_Data/totalpop_age_Census_98-14.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(ILINet_week_plotting_dicts)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population, dict_OR[week] = OR; dict_zOR[week] = zOR
	dict_wk, dict_incid, dict_OR, dict_zOR = ILINet_week_zOR_processing(csv_incidence, csv_population)
	
	dict_incid53ls, dict_OR53ls, dict_zOR53ls = defaultdict(list), defaultdict(list), defaultdict(list)
	for s in gp_ILINet_plotting_seasons:
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
	
	return dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls

##############################################
def ILINet_week_zOR_processing(csv_incidence, csv_population):
	''' Calculate zOR by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. The function 'week_OR_processing' is nested within this function. Return dictionaries of week to season number, week to OR, and week to zOR. Source files for csv_incidence and csv_population are 'CDC_Source/Import_Data/all_cdc_source_data.csv' and 'Census/Import_Data/totalpop_age_Census_98-14.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season
	dict_OR[week] = OR
	dict_zOR[week] = zOR
	'''
	main(ILINet_week_zOR_processing)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
	dict_wk, dict_incid, dict_OR = ILINet_week_OR_processing(csv_incidence, csv_population)
	
	dict_zOR = {}
	for s in gp_ILINet_plotting_seasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR[wk] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR[wk] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR[wk]-season_mean)/season_sd for wk in weekdummy]
		for w, z in zip(weekdummy, list_dictdummy):
			dict_zOR[w] = z
	
	return dict_wk, dict_incid, dict_OR, dict_zOR

##############################################
def normalize_incidCA(dict_wk, dict_incid):
	''' Import dict_wk and dict_incid and normalize dict_incid by the maximum child incidence value during a flu season.
		dict_wk[week] = seasonnum
		dict_incid[week] = (child ILI cases per 10,000 in US population in second calendar year of flu season, adult incid per 10,000)
		dict_incidC_norm[seasonnum] = [norm child incid wk40, norm child incid wk41, ...]
		dict_incidA_norm[seasonnum] = [norm adult incid wk40, norm adult incid wk 41, ...]
	'''
	main(normalize_incidCA)

	dict_incidC_season, dict_incidA_season, dict_incidC_norm, dict_incidA_norm = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
	
	for s in set(dict_wk.values()):
		dict_incidC_season[s] = [dict_incid[week][0] for week in sorted(dict_wk) if dict_wk[week] == s]
		dict_incidA_season[s] = [dict_incid[week][1] for week in sorted(dict_wk) if dict_wk[week] == s]
		maxC = max(dict_incidC_season[s]) # max peak child epidemic
		# normalize incidence curves by max peak child epidemic
		dict_incidC_norm[s] = [val/maxC for val in dict_incidC_season[s]]
		dict_incidA_norm[s] = [val/maxC for val in dict_incidA_season[s]]

	return dict_incidC_norm, dict_incidA_norm


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
		# include only seasons in gp_plotting_seasons in returned dictionary
		dict_dummy[season] = H3i/TOTi

	# dict_H3[seasonnum] = proportion H3 isolates of all isolates collected that season
	dict_H3 = dict((s, dict_dummy[s]) for s in gp_plotting_seasons)
	
	return dict_H3

##############################################
def season_H3perc_NREVSS(csvreadfile):
	''' Import My_Bansal_Lab/Clean_Data_for_Import/NREVSS_Isolates_Season.csv data, which includes information on year, number of samples positive for flu, A samples, B samples, subtyped A samples, A/H1 samples, A/H3 samples, B samples, A/2009H1N1 samples, total speciments tested. Return a dictionary with season and proportion of H3 isolates of all subtyped flu isolates collected that season. The original source of isolate information is the CDC Flu Season Summaries, WHO NREVSS surveillance system (not the CDC system).
	dict_H3[seasonnum] = proportion of H3 isolates of all isolates collected that season
	'''
	main(season_H3perc_NREVSS)
	
	dict_dummy = {}
	for row in csvreadfile:
		A_sub, B = int(row[4]), int(row[3])
		TOTi = A_sub + B
		H3i = float(row[6])
		season = int(row[0][7:]) # season number
		# include only seasons in gp_plotting_seasons in returned dictionary
		dict_dummy[season] = H3i/TOTi

	# dict_H3[seasonnum] = proportion H3 isolates of all isolates collected that season
	dict_H3 = dict((s, dict_dummy[s]) for s in gp_plotting_seasons)
	
	return dict_H3

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
		season = int(row[0][2:]) # season number
		# include only seasons in gp_plotting_seasons in returned dictionary
		dict_dummy[season] = a_H3/TOTi

	# dict_H3[seasonnum] = proportion H3 isolates of all isolates collected that season
	dict_H3 = dict((s, dict_dummy[s]) for s in gp_plotting_seasons)
	
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
	''' Import SQL_export/OR_allweeks_outpatient.csv data (or other OR_allweeks...csv data), which includes season number, week, age group, and ILI incid. Import SQL_export/totalpop_age.csv data, which includes calendar year, age group, and US population. Return dictionary with week to season number, week to child and adult ILI cases per 100,000 in total US population. Incidence rates for children and adults will be calculated based on popstat variable of the population in the second calendar year of the flu season (eg. 2001-02 season is based on 2002 population).
	dict_wk[week] = seasonnum
	dict_incid[week] = (child ILI cases per 100,000 in US population in second calendar year of flu season, adult incid per 100,000)
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
	dict_incid = {}
	for wk in dict_wk:
		s = dict_wk[wk]
		# dict_incid[week] = (child incid per 100,000, adult incid per 100,000)
		child_incid = dict_ILI_week[(wk, 'C')]/dict_pop[(s, 'C')]*100000
		adult_incid = dict_ILI_week[(wk, 'A')]/dict_pop[(s, 'A')]*100000
		dict_incid[wk] = (child_incid, adult_incid)
	
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
	for s, h, ak in product(gp_plotting_seasons, gp_plotting_regions, age_keys):
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
	dict_wk_sub = dict((k, dict_wk[k]) for k in dict_wk if dict_wk[k] in gp_plotting_seasons) 
	
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
	for s, state, ak in product(gp_plotting_seasons, state_keys, age_keys):
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
	dict_wk_sub = dict((k, dict_wk[k]) for k in dict_wk if dict_wk[k] in gp_plotting_seasons) 

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
def week_plotting_dicts(csv_incidence, csv_population):
	'''Return dictionaries for season to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. Source files for csv_incidence and csv_population are 'SQL_export/OR_allweeks_outpatient.csv' and 'SQL_export/totalpop_age.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid53ls[seasonnum] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls[seasonnum] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls[seasonnum] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(week_plotting_dicts)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population, dict_OR[week] = OR; dict_zOR[week] = zOR
	dict_wk, dict_incid, dict_OR, dict_zOR = week_zOR_processing(csv_incidence, csv_population)
	
	dict_incid53ls, dict_OR53ls, dict_zOR53ls = defaultdict(list), defaultdict(list), defaultdict(list)
	for s in gp_plotting_seasons:
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
	
	return dict_wk, dict_incid53ls, dict_OR53ls, dict_zOR53ls

##############################################
def week_plotting_dicts_region(csv_incidence_region, csv_population_region):
	'''Return dictionaries for (season, region) to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. 
	dict_wk[week] = seasonnum
	dict_incid53ls_reg[(seasonnum, region)] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls_reg[(seasonnum, region)] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls_reg[(seasonnum, region)] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(week_plotting_dicts_region)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_reg[(week, hhsreg)] = OR, dict_zOR_reg[(week, hhsreg)] = zOR
	dict_wk, dict_zip3_reg, dict_incid_reg, dict_OR_reg, dict_zOR_reg = week_zOR_processing_region(csv_incidence_region, csv_population_region)

	dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg = defaultdict(list), defaultdict(list), defaultdict(list)
	for s, r in product(gp_plotting_seasons, gp_plotting_regions):
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
	
	return dict_wk, dict_incid53ls_reg, dict_OR53ls_reg, dict_zOR53ls_reg

##############################################
def week_plotting_dicts_state(csv_incidence_region, csv_population_region):
	'''Return dictionaries for (season, state) to incidence, OR, and zOR by week as a list, adding 53rd week data as the average of week 52 and week 1 if necessary. Dictionary keys are created only for seasons in gp: plotting_seasons, where 'gp' is a global parameter defined within functions.py. 
	dict_wk[week] = seasonnum
	dict_incid53ls_state[(seasonnum, state)] = [ILI wk 40, ILI wk 41,...]
	dict_OR53ls_state[(seasonnum, state)] = [OR wk 40, OR wk 41, ...]
	dict_zOR53ls_state[(seasonnum, state)] = [zOR wk 40, zOR wk 41, ...]
	'''
	main(week_plotting_dicts_state)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_state[(week, state)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_state[(week, state)] = OR, dict_zOR_reg[(week, state)] = zOR
	dict_wk, dict_zip3_reg, dict_incid_state, dict_OR_state, dict_zOR_state = week_zOR_processing_state(csv_incidence_region, csv_population_region)

	state_keys = list(set([dict_zip3_reg[k][0] for k in dict_zip3_reg]))

	dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state = defaultdict(list), defaultdict(list), defaultdict(list)
	for s, state in product(gp_plotting_seasons, state_keys):
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
	
	return dict_wk, dict_incid53ls_state, dict_OR53ls_state, dict_zOR53ls_state

##############################################
def week_zOR_processing(csv_incidence, csv_population):
	''' Calculate zOR by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. The function 'week_OR_processing' is nested within this function. Return dictionaries of week to season number, week to OR, and week to zOR. Source files for csv_incidence and csv_population are 'SQL_export/OR_allweeks_outpatient.csv' and 'SQL_export/totalpop_age.csv' respectively.
	dict_wk[week] = seasonnum
	dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season
	dict_OR[week] = OR
	dict_zOR[week] = zOR
	'''
	main(week_zOR_processing)
	# dict_wk[week] = seasonnum; dict_incid[week] = ILI cases per 10,000 in US population in second calendar year of flu season, dict_OR[week] = OR
	dict_wk, dict_incid, dict_OR = week_OR_processing(csv_incidence, csv_population)
	
	dict_zOR = {}
	for s in gp_plotting_seasons:
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR[wk] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR[wk] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR[wk]-season_mean)/season_sd for wk in weekdummy]
		for w, z in zip(weekdummy, list_dictdummy):
			dict_zOR[w] = z
	
	return dict_wk, dict_incid, dict_OR, dict_zOR

##############################################
def week_zOR_processing_region(csv_incidence_region, csv_population_region):
	''' Calculate zOR for each region by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. Each region is z-normalized by the first normweeks weeks of OR data for that region. The function 'week_OR_processing_region' is nested within this function. Return dictionaries of week to season number, zip3 to state and region, (week, region) to incidence, (week, region) to OR, and (week, region) to zOR.
	dict_wk[week] = seasonnum
	dict_zip3_reg[zip3] = (state, hhsreg)
	dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season
	dict_OR_reg[(week, hhsreg)] = OR
	dict_zOR_reg[(week, hhsreg)] = zOR
	'''
	main(week_zOR_processing_region)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_reg[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_reg[(week, hhsreg)] = OR
	dict_wk, dict_zip3_reg, dict_incid_reg, dict_OR_reg = week_OR_processing_region(csv_incidence_region, csv_population_region)
		
	dict_zOR_reg = {}
	for s, r in product(gp_plotting_seasons, gp_plotting_regions):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR_reg[(wk, r)] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR_reg[(wk, r)] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR_reg[(wk, r)]-season_mean)/season_sd for wk in weekdummy]
		for w, zOR in zip(weekdummy, list_dictdummy):
			dict_zOR_reg[(w, r)] = zOR
	
	return dict_wk, dict_zip3_reg, dict_incid_reg, dict_OR_reg, dict_zOR_reg

##############################################
def week_zOR_processing_state(csv_incidence_region, csv_population_region):
	''' Calculate zOR for each state by week based on normweeks and plotting_seasons gp. 'gp' is global parameter defined at the beginning of functions.py. Each region is z-normalized by the first normweeks weeks of OR data for that state. The function 'week_OR_processing_state' is nested within this function. Return dictionaries of week to season number, zip3 to state and region, (week, state) to incidence, (week, state) to OR, and (week, state) to zOR.
	dict_wk[week] = seasonnum
	dict_zip3_reg[zip3] = (state, hhsreg)
	dict_incid_state[(week, state)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season
	dict_OR_state[(week, state)] = OR
	dict_zOR_state[(week, state)] = zOR
	'''
	main(week_zOR_processing_state)
	# dict_wk[week] = seasonnum, dict_zip3_reg[zip3] = (state, hhsreg), dict_incid_state[(week, hhsreg)] = total ILI incidence per 100,000 popstat in 2nd calendar year of flu season, dict_OR_state[(week, hhsreg)] = OR
	dict_wk, dict_zip3_reg, dict_incid_state, dict_OR_state = week_OR_processing_state(csv_incidence_region, csv_population_region)
		
	state_keys = list(set([dict_zip3_reg[k][0] for k in dict_zip3_reg]))

	dict_zOR_state = {}
	for s, state in product(gp_plotting_seasons, state_keys):
		weekdummy = sorted([key for key in dict_wk if dict_wk[key] == s])
		season_mean = np.mean([dict_OR_state[(wk, state)] for wk in weekdummy[:gp_normweeks]])
		season_sd = np.std([dict_OR_state[(wk, state)] for wk in weekdummy[:gp_normweeks]])
		list_dictdummy = [(dict_OR_state[(wk, state)]-season_mean)/season_sd for wk in weekdummy]
		for w, zOR in zip(weekdummy, list_dictdummy):
			dict_zOR_state[(w, state)] = zOR
	
	return dict_wk, dict_zip3_reg, dict_incid_state, dict_OR_state, dict_zOR_state


##############################################
##############################################
# footer

def main(function):
	print 'Running', __name__, function.__name__

if __name__ == '__main__':
	print 'Executed from the command line'
	main()