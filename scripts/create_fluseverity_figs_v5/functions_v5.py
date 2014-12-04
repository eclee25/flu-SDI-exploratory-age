#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/31/14

## Purpose: script of functions for data cleaning and processing to draw flu severity figures; supports figures in create_fluseverity_figs
## v2: swap child:adult OR to adult:child OR
## v3: continue swap, adjust incidence for age-specific ILI HC seeking behavior, ratio of week-specific any diagnosis visits in S9/S#
## v4: change to relative risk, coverage adjustment: ratio of season-specific any diagnosis visits in S9/S#, care-seeking adjustment: age-specific ILI HC seeking behavior
## v5: coverage adjustments are all non-age-specific. care-seeking adjustments are all age-specific.

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
import csv

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

## create dict_ages ##
age_keys = ['C', 'A', 'O']
children = ['5-9 YEARS', '10-14 YEARS', '15-19 YEARS']
adults = ['20-29 YEARS', '30-39 YEARS', '40-49 YEARS', '50-59 YEARS']
other = ['<2 YEARS', '2-4 YEARS', '60-69 YEARS', '70-79 YEARS', '80 YEARS']
dict_ages = defaultdict(list)
# dict_ages[agegroup code] = [agegroup bin 1, age group bin 2,... in text]
dict_ages = dict(zip(age_keys, [children, adults, other]))

## ILI care-seeking behavior ##
# national level, weighted averages based on sample size in Biggerstaff2012 and Biggerstaff2014
# children = 5-17, adults = 18-64, other = <5 & >64. See health_seeking_behavior_edited_101014.ods
dict_careseek_nat = {'C':0.5146, 'A':0.4095, 'O':0.6262, 'T':0.4501} 
# Census region level, Biggerstaff2012
# children = 0-17, adults >= 18
dict_careseek_census = {('NE', 'A'):0.44, ('MW', 'A'):0.39, ('SO', 'A'):0.42, ('WE', 'A'):0.33, ('NE', 'C'):0.58, ('MW', 'C'):0.48, ('SO', 'C'):0.66, ('WE', 'C'):0.50, ('NE', 'T'):0.47, ('MW', 'T'):0.41, ('SO', 'T'):0.48, ('WE', 'T'):0.37}


##############################################
# global parameters - plotting

## generic label formatting ##
gp_sigma_r = r'Retrospective Severity, $\bar \sigma_r$'
gp_sigma_w = r'Early Warning Severity, $\bar \sigma_w$'
gp_sigmat = r'Adj. Ratio of Adult:Child ILI, $\sigma(t)$'
gp_benchmark = r'Benchmark, $\beta$'
gp_attackrate = r'Seasonal ILI Visits per 100,000'
gp_adjILI = r'Adj. ILI Visits per 100,000'

## SDI data ##
gp_seasonlabels = ['01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09']
gp_colors_1_10 = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
# gp_colors = ['black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet']
gp_colors = ["#e41a1c", "#228b22", "#377eb8", "#ff7f00", "#984ea3", "#ffff33", "#a65628", "#f781bf"]
gp_retro_early_colors = ['black', '#7cfc00']
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
gp_marker = 'None'
gp_linewidth = 3

## ILINet data ##
gp_ILINet_seasonlabels = ['97-98', '98-99', '99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '10-11', '11-12', '12-13', '13-14']
gp_ILINet_colors = cm.rainbow(np.linspace(0, 1, len(gp_ILINet_seasonlabels)))

##############################################
## call parameters ##
# set these parameters every time a plot is run

# pseasons = gp_ILINet_plotting_seasons
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
def classif_zRR_processing(dict_wk, dict_totIncidAdj53ls, dict_zRR53ls):
	''' Calculate retrospective and early warning zRR classification values for each season, which is the mean zRR for the duration of the retrospective and early warning periods, respectively. The retrospective period is designated relative to the peak incidence week in the flu season. The early warning period is designated relative to the week of Thanksgiving.
	Mean retrospective period zRR is based on a baseline normalization period (gp: normweeks), duration of retrospective period (gp: retro_duration), and number of weeks prior to peak incidence week, which dictates when the retrospective period begins that season (gp: begin_retro_week). Mean early warning period zRR is based on gp: normweeks, gp: early_duration, and gp: begin_early_week. 'gp' stands for global parameter, which is defined within functions.py. The Thanksgiving_import and identify_retro_early_weeks functions are nested within this function. Returns one dict:
	dict_classifzRR[seasonnum] = (mean retrospective zRR, mean early warning zRR)
	'''
	main(classif_zRR_processing)
	
	# dict_indices[(season, period ('r' or 'e'))] = (begin index, end index)
	dict_indices = identify_retro_early_weeks(dict_wk, dict_totIncidAdj53ls)
	
	dict_classifzRR = {}
	for s in pseasons:
	
		# peak-based retrospective classification
		begin_retro, end_retro = dict_indices[(s, 'r')]
		# list of week indices in retrospective period
		retro_indices = xrange(begin_retro, end_retro)
		mean_retro_zRR = np.mean([dict_zRR53ls[s][i] for i in retro_indices])
		
		# Thanksgiving-based early warning classification
		begin_early, end_early = dict_indices[(s, 'e')]
		# list of week indices in early warning period
		early_indices = xrange(begin_early, end_early)
		mean_early_zRR = np.mean([dict_zRR53ls[s][i] for i in early_indices])
	
		# dict_classifzRR[seasonnum] = (mean retrospective zRR, mean early warning zRR)
		dict_classifzRR[s] = (mean_retro_zRR, mean_early_zRR)
		
	return dict_classifzRR

##############################################
def classif_zRR_processing_spatial(dict_wk, dict_spatialTotIncidAdj53ls, dict_spatialZRR53ls, spatial_keys):
	''' Calculate retrospective and early warning zOR classification values for each season and spatial (state/region) combination. Spatial retrospective classifications are tied to the peak adjusted incidence week of the state/region in a given season. Spatial early warning classifications are tied to the week of Thanksgiving in a given season, and are thus the same as the early warning periods at the national level. The Thanksgiving_import and identify_retro_early_weeks functions are nested within this function. Returns one dict:
	dict_classifzRR_spatial[(season, spatial)] = (mean retrospective zOR, mean early warning zOR)
	'''
	main(classif_zRR_processing_spatial)
	
	dict_classifzRR_spatial = {}
	for spatial in spatial_keys:
		dict_incidAdj_dummy = dict((key[0], dict_spatialTotIncidAdj53ls[key]) for key in dict_spatialTotIncidAdj53ls if key[1] == spatial)
		# subset begin/end retro and early week indexes for a given spatial designation (in order to be able to use the identify_retro_early_weeks function)
		# dict_indices[(season, period ('r' or 'e'))] = (begin index, end index)
		dict_indices = identify_retro_early_weeks(dict_wk, dict_incidAdj_dummy)
		
		for s in pseasons:
			# peak-based retrospective classification
			begin_retro, end_retro = dict_indices[(s, 'r')]
			# list of week indices in retrospective period
			retro_indices = xrange(begin_retro, end_retro)
			mean_retro_zOR = np.mean([dict_spatialZRR53ls[(s, spatial)][i] for i in retro_indices])
			
			# Thanksgiving-based early warning classification
			begin_early, end_early = dict_indices[(s, 'e')]
			# list of week indices in early warning period
			early_indices = xrange(begin_early, end_early)
			mean_early_zOR = np.mean([dict_spatialZRR53ls[(s, spatial)][i] for i in early_indices])
		
			dict_classifzRR_spatial[(s, spatial)] = (mean_retro_zOR, mean_early_zOR)
		
	return dict_classifzRR_spatial

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
def identify_retro_early_weeks(dict_wk, dict_incid53ls):
	''' Identify weeks in the early warning and retrospective periods for each season using indices in list for incidence. Returns one dict: dict_indices[(snum, classif period)] = (first index, last index for index slicing)
	'''
	main(identify_retro_early_weeks)

	# import Thanksgiving data 
	thanksin = open('/home/elee/Dropbox/My_Bansal_Lab/Clean_Data_for_Import/ThanksgivingWeekData_cl.csv', 'r')
	thanksin.readline() # remove header
	csv_Thanksgiving = csv.reader(thanksin, delimiter=',')
	dict_Thanksgiving = Thanksgiving_import(csv_Thanksgiving) 

	dict_indices = {}
	for s in pseasons:
		weekdummy = sorted([wk for wk in dict_wk if dict_wk[wk] == s])
		# identify retrospective week indices
		peak_index = peak_flu_week_index(dict_incid53ls[s])
		# 11/7: if the season peaks before week 2
		if peak_index <= 15:
			begin_retro = 16 # fixed at week 3
			print s, 'peaks <= week 2'
		else:
			begin_retro = peak_index - gp_begin_retro_week
		end_retro = begin_retro + gp_retro_duration

		# identify early warning week indices
		Thx_index = weekdummy.index(dict_Thanksgiving[s])
		begin_early = Thx_index + gp_begin_early_week
		end_early = begin_early + gp_early_duration

		# create dictionary with early warning and retrospective indices by season
		dict_indices[(s, 'r')] = (begin_retro, end_retro)
		dict_indices[(s, 'e')] = (begin_early, end_early)

	return dict_indices

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
def ILINet_week_RR_processing(csv_incidence, csv_population):
	''' Import CDC_Source/Import_Data/all_cdc_source_data.csv, which includes unique id, year, week, age group, and ILI incid. Import Census/Import_Data/totalpop_age_Census_98-14.csv, which includes season, age group code, and US population.  In ILINet, children are 5-24 years and adults are 25-64 years. In totalpop_age.csv, children are 5-19 years and adults are 20-59 years. Coverage and care-seeking adjustment performed in function. Return five dicts:
	dict_wk[wk] = seasonnum
	dict_pop[(season, agegroup code)] = population size of agegroup
	dict_totILI53ls[s] = [ILI cases wk40,... wk 39] (unadjusted ILI counts)
	dict_totILIadj53ls[s] = [adjusted ILI cases wk 40, ...adj cases wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
	dict_ageILIadj_season[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]
	'''
	main(ILINet_week_RR_processing)
	
	## import ILI data ##
	# dict_ILI_week[(week, agegroup code)] = ILI cases; dict_wk[week] = seasonnum, S1 = 2000-01, dict_anyvisit_week[(week)] = total outpatients
	dict_ILI_week, dict_wk, dict_anyvisit_week = {},{},{}
	for row in csv_incidence: 
		row_cl = [float('nan') if val == 'NA' else val for val in row]
		week = str(row_cl[0])+'0' # additional 0 represents Sunday
		wktime = datetime.strptime(week, '%Y%U%w') # format = 4-dig year, 2-dig week beginning on Monday (8/10/14), digit representing day of week; data are from one week later than week number listed on plots (for both ILINet and SDI data).
		wk = datetime.date(wktime) # remove the time from the datetime format
		dict_ILI_week[(wk, 'C')] = float(row_cl[33])
		dict_ILI_week[(wk, 'A')] = float(row_cl[34])
		dict_ILI_week[(wk, 'O')] = float(row_cl[27])-float(row_cl[33])-float(row_cl[34])
		dict_wk[wk] = int(row_cl[12])
		dict_anyvisit_week[wk] = float(row_cl[28])
	
	## import population data ##
	dict_pop = {}
	for row in csv_population:
		season = int(row[0])
		agecode = row[1]
		# dict_pop[(season, agegroup code)] = population size of agegroup		
		dict_pop[(season, agecode)] = int(row[2]) 
	
	# adjust ILI cases by increasing coverage over time and constant age-specific ILI seeking behavior
	dict_ageILIadj_season, dict_totILI53ls, dict_totILIadj53ls = ILINet_coverageCareseek_adjustment(dict_ILI_week, dict_wk, dict_anyvisit_week)
	
	return dict_wk, dict_pop, dict_totILI53ls, dict_totILIadj53ls, dict_ageILIadj_season

##############################################
def ILINet_coverageCareseek_adjustment(dict_ILI_week, dict_wk, dict_anyvisit_week):
	''' ILINet analogue for incidence adjustments. Adjust age-specific ILI and total ILI by changing coverage by season (visits in season 14/visits in season #) and ILI-seeking behavior. Return three dicts: dict_ageILIAdjust53ls[(season, age)] = [ILI * (visits in flu season 14)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]; 	dict_totILI53ls[season] = [ILI wk 40,... ILI wk 39]; dict_totILIAdjust53ls = [adj ILI wk 40, ... adj ILI wk 39]
	'''
	main(ILINet_coverageCareseek_adjustment)

	# estimate number of ILI cases that would have been captured in the dataset had the coverage been at 08-09 flu season levels for all years
	dict_anyvisit_season, dict_ili_season, dict_totILI53ls, dict_totILIAdjust53ls = {}, defaultdict(list), defaultdict(list), defaultdict(list)
	for s in pseasons:
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk] == s])
		for age in age_keys:
			Visits = [dict_anyvisit_week[wk] for wk in dummyweeks]
			ILI = [dict_ILI_week[(wk, age)] for wk in dummyweeks]
			if len(dummyweeks) == 52:
				Visits.insert(13, (Visits[12]+Visits[13])/2.)
				ILI.insert(13, (ILI[12]+ILI[13])/2.)
			dict_anyvisit_season[s] = sum(Visits[:gp_fluweeks]) # total any diagnosis visits during flu season
			dict_ili_season[(s, age)] = ILI

		# list of lists for ili counts for all age groups
		all_lists = [dict_ili_season[(s, age)] for age in age_keys]
		# raw ili time series by season
		dict_totILI53ls[s] = [sum(ili) for ili in zip(*all_lists)]

	# create total incidence dict with coverage and ILI care-seeking adjustments
	visit14_Tpop = dict_anyvisit_season[14]
	for s in pseasons:
		visitS_Tpop = dict_anyvisit_season[s]
		# adjustment for total incidence dict
		Tadjustment = visit14_Tpop/visitS_Tpop/dict_careseek_nat['T']
		dict_totILIAdjust53ls[s] = [ili*Tadjustment for ili in dict_totILI53ls[s]]

	# create age-specific incidence dict with total pop coverage and ILI care-seeking behavior adjustments
	dict_ageILIAdjust53ls = defaultdict(list)
	for key in dict_ili_season:
		s, age = key
		careseek = dict_careseek_nat[age] # defined at top
		iliDummy = dict_ili_season[key]
		visitS_Tpop = dict_anyvisit_season[s]	
		# adjust ILI by coverage level in 08-09 flu season and age-specific care seeking behavior
		adjustment = visit14_Tpop/visitS_Tpop/careseek
		dict_ageILIAdjust53ls[key] = [ili*adjustment for ili in iliDummy]

	return dict_ageILIAdjust53ls, dict_totILI53ls, dict_totILIAdjust53ls

##############################################
def normalize_attackCA(dict_wk, dict_ageIncidAdjust53ls):
	''' Import dict_wk and dict_ageIncidAdjust53ls outputs from week_incidCA_processing function. Sum values in dict_incid for children and adults to get an attack rate for each season. The flu season is defined as weeks 40 to 20. Normalize the child and adult attack rates by dividing the raw attack rate by the average child and adult attack rates and subtract 1 (percentage deviation from baseline) across all seasons. Returns one dict:
		dict_attackCA_norm[seasonnum] = (% dev from baseline child attack rate, % dev from baseline adult attack rate)
	'''
	main(normalize_attackCA)

	dict_attackCA, dict_attackCA_norm = {}, {}
	
	for s in pseasons:
		# attack rates per 100,000 for children and adults by week, include only wks 40 to 20 (53 weeks total in each season)
		dict_attackCA[s] = (sum(dict_ageIncidAdjust53ls[(s, 'C')][:gp_fluweeks]), sum(dict_ageIncidAdjust53ls[(s, 'A')][:gp_fluweeks]))

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
def week_anydiag_processing(csv_anydiag):
	''' Import SQL_export/anydiag_allweeks_outpatient.csv and calculate number of visits/population per 100,000. dict_any[week] = visits per 100,000 in US pop in calendar of data week, dict_any53ls
	'''
	main(week_anydiag_processing)
	dict_wk, dict_any = {}, {}
	dict_any53ls = defaultdict(list)
	for row in csv_anydiag:
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		dict_wk[wk] = int(row[0])
		dict_any[wk] = float(row[2])/int(row[3])*100000

	# plotting version of dict_any
	for s in pseasons:
		any53dummy = [dict_any[wk] for wk in sorted(dict_wk) if dict_wk[wk] == s]
		if len(any53dummy) == 52:
			a53any = (any53dummy[12]+any53dummy[13])/2.
			any53dummy.insert(13, a53any)
		dict_any53ls[s] = any53dummy

	return dict_wk, dict_any, dict_any53ls

##############################################
def week_incidCA_processing(csv_incidence, csv_population):
	''' Import SQL_export/OR_allweeks_outpatient.csv data (or other OR_allweeks...csv data), which includes season number, week, age group, and ILI incid. Import SQL_export/totalpop_age.csv data, which includes calendar year, age group, and US population. Includes coverage and ILI care-seeking adjustment. Return two dicts:
	dict_wk[week] = seasonnum
	dict_ageIncidAdjust53ls[(season, age)] = [adj incid per 100000 wk 40, ... wk 39]
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
	
	# adjust ILI cases by increasing coverage over time and constant age-specific ILI seeking behavior 
	# 10/31/14: could change this to anydiag_allweeks_outpatient.csv since coverage adjustment is no longer age-specific
	fname = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient_age.csv'
	
	# dict_ageILIadj_season[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]
	dict_ageILIadj_season,_,_ = coverageCareseek_adjustment(fname, dict_ILI_week)
	
	dict_ageIncidAdjust53ls = defaultdict(list)
	# generate age-specific adjusted incidence per 100,000 
	for s in pseasons:
		# child and adult attack rates
		child_attack = [adjILI/dict_pop[(s, 'C')]*100000 for adjILI in dict_ageILIadj_season[(s, 'C')]]
		adult_attack = [adjILI/dict_pop[(s, 'A')]*100000 for adjILI in dict_ageILIadj_season[(s, 'A')]]
		dict_ageIncidAdjust53ls[(s, 'C')] = child_attack
		dict_ageIncidAdjust53ls[(s, 'A')] = adult_attack

	return dict_wk, dict_ageIncidAdjust53ls

##############################################
def coverageCareseek_adjustment(filename_anydiagAge, dict_ILI_week):
	''' Import any diagnosis visits by week and age group. Adjust age-specific ILI and total ILI by changing coverage by season (visits in season 9/visits in season #) and ILI-seeking behavior. Function argument is the filename string. Return three dicts: dict_ageILIAdjust53ls[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]; dict_totILI53ls[season] = [ILI wk 40,... ILI wk 39]; dict_totILIAdjust53ls = [adj ILI wk 40, ... adj ILI wk 39]
	'''
	main(coverageCareseek_adjustment)

	anydiagin = open(filename_anydiagAge, 'r')
	anydiagin.readline() # rm header
	anydiag = csv.reader(anydiagin, delimiter=',')

	dict_anyvisit_week, dict_wk = {},{}
	for row in anydiag:
		season = int(row[0])
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		agecode = str(row[2])
		visits = int(row[3])
		dict_anyvisit_week[(wk, agecode)] = float(visits)
		dict_wk[wk] = (season, wk.isocalendar()[1]+1) # isocalendar wk number+1 because isocalendar goes from Monday to Sunday

	# estimate number of ILI cases that would have been captured in the dataset had the coverage been at 08-09 flu season levels for all years
	dict_anyvisit_season, dict_ili_season, dict_totILI53ls, dict_totILIAdjust53ls = {}, defaultdict(list), defaultdict(list), defaultdict(list)
	for s in pseasons:
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk][0] == s])
		for age in age_keys:
			Visits = [dict_anyvisit_week[(wk, age)] for wk in dummyweeks]
			ILI = [dict_ILI_week[(wk, age)] for wk in dummyweeks]
			if len(dummyweeks) == 52:
				Visits.insert(13, (Visits[12]+Visits[13])/2.)
				ILI.insert(13, (ILI[12]+ILI[13])/2.)
			dict_anyvisit_season[(s, age)] = sum(Visits[:gp_fluweeks]) # total any diagnosis visits during flu season
			dict_ili_season[(s, age)] = ILI

		# list of lists for ili counts for all age groups
		all_lists = [dict_ili_season[(s, age)] for age in age_keys]
		# raw ili time series by season
		dict_totILI53ls[s] = [sum(ili) for ili in zip(*all_lists)]

	# create total incidence dict with coverage and ILI care-seeking adjustments
	visit9_Tpop = sum([dict_anyvisit_season[(9, age)] for age in age_keys])
	for s in pseasons:
		visitS_Tpop = sum([dict_anyvisit_season[(s, age)] for age in age_keys])
		# adjustment for total incidence dict
		Tadjustment = visit9_Tpop/visitS_Tpop/dict_careseek_nat['T']
		dict_totILIAdjust53ls[s] = [ili*Tadjustment for ili in dict_totILI53ls[s]]

	# create age-specific incidence dict with total pop coverage and ILI care-seeking behavior adjustments
	dict_ageILIAdjust53ls = defaultdict(list)
	for key in dict_ili_season:
		s, age = key
		careseek = dict_careseek_nat[age] # defined at top
		iliDummy = dict_ili_season[key]
		visitS_Tpop = sum([dict_anyvisit_season[(s, age)] for age in age_keys])		
		# adjust ILI by coverage level in 08-09 flu season and age-specific care seeking behavior
		adjustment = visit9_Tpop/visitS_Tpop/careseek
		dict_ageILIAdjust53ls[key] = [ili*adjustment for ili in iliDummy]

	return dict_ageILIAdjust53ls, dict_totILI53ls, dict_totILIAdjust53ls

##############################################
def week_OR_processing(csv_incidence, csv_population):
	''' Import SQL_export/OR_allweeks_outpatient.csv data (or other OR_allweeks...csv data), which includes season number, week, age group, and ILI incid. Import SQL_export/totalpop_age.csv data, which includes calendar year, age group, and US population. Function 'coverageCareseek_adjustment' is nested. Return five dicts:
	dict_wk[wk] = seasonnum
	dict_pop[(season, agegroup code)] = population size of agegroup
	dict_totILI53ls[s] = [ILI cases wk40,... wk 39] (unadjusted ILI counts)
	dict_totILIadj53ls[s] = [adjusted ILI cases wk 40, ...adj cases wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
	dict_ageILIadj_season[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]
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
	
	# adjust ILI cases by increasing coverage over time and constant age-specific ILI seeking behavior 
	# 10/31/14: could change this to anydiag_allweeks_outpatient.csv since coverage adjustment is no longer age-specific
	fname = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient_age.csv'
	# dict_ageILIadj_season[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]; dict_totILI53ls[season] = [ILI wk 40,... ILI wk 39]; dict_totILIAdjust53ls = [adj ILI wk 40, ... adj ILI wk 39]
	dict_ageILIadj_season, dict_totILI53ls, dict_totILIadj53ls = coverageCareseek_adjustment(fname, dict_ILI_week)
	# 11/6/14: when summer baselines are needed, uncomment
	# dict_ageILIadj_season, dict_totILI53ls, dict_totILIadj53ls = coverageCareseek_adjustment_altbaseline(fname, dict_ILI_week)

	return dict_wk, dict_pop, dict_totILI53ls, dict_totILIadj53ls, dict_ageILIadj_season

##############################################
def week_RR_processing_part2(dict_pop, dict_totILI53ls, dict_totILIadj53ls, dict_ageILIadj_season):
	''' Import adjusted and non-adjusted ILI cases by age group from week_OR_processing or ILINet_week_RR_processing. Return four dicts:
	dict_totIncid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
	dict_totIncidAdj53ls[s] = [adjusted incid rate per 100000 wk 40, ...adj incid wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
	dict_RR53ls[s] = [RR wk 40,... RR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
	dict_zRR53ls[s] = [zRR wk 40,... zRR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
		'''
	main(week_RR_processing_part2)

	dict_totIncid53ls, dict_totIncidAdj53ls, dict_RR53ls, dict_zRR53ls = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
	# generate adjusted incidence per 100,000 in US population, OR, and zOR at the weekly level
	for s in pseasons:
		# total population in the season
		tot_pop = sum([dict_pop[(s, ak)] for ak in age_keys])
		# totIncid53ls dict
		dict_totIncid53ls[s] = [ili/tot_pop*100000 for ili in dict_totILI53ls[s]]
		# totIncidAdj53ls
		dict_totIncidAdj53ls[s] = [iliAdj/tot_pop*100000 for iliAdj in dict_totILIadj53ls[s]]
		# RR53ls dict
		child_attack = [adjILI/dict_pop[(s, 'C')] for adjILI in dict_ageILIadj_season[(s, 'C')]]
		adult_attack = [adjILI/dict_pop[(s, 'A')] for adjILI in dict_ageILIadj_season[(s, 'A')]]
		# 10/19/14: RR should not be evaluated if child or adult incidence is zero
		# 10/16/14 change OR to relative risk
		RR = [a/c if c and a else float('nan') for c, a in zip(child_attack, adult_attack)] 
		dict_RR53ls[s] = RR
		# zRR53ls dict
		normalization_period = dict_RR53ls[s][:gp_normweeks]
		season_mean = np.mean(normalization_period)
		season_sd = np.std(normalization_period)
		dict_zRR53ls[s] = [(val-season_mean)/season_sd for val in dict_RR53ls[s]]

	return dict_totIncid53ls, dict_totIncidAdj53ls, dict_RR53ls, dict_zRR53ls

##############################################
def coverageCareseek_adjustment_altbaseline(filename_anydiagAge, dict_ILI_week):
	''' Import any diagnosis visits by week and age group. Adjust age-specific ILI and total ILI by changing coverage by season (visits in season 9/visits in season #) and ILI-seeking behavior. Function argument is the filename string. Return three dicts: dict_ageILIAdjust53ls[(season, age)] = [ILI * (visits in flu season 9)/(visits in flu season #)/(ILI care-seeking behavior) wk 40, ...wk 39]; dict_totILI53ls[season] = [ILI wk 40,... ILI wk 39]; dict_totILIAdjust53ls = [adj ILI wk 40, ... adj ILI wk 39]
	'''
	main(coverageCareseek_adjustment_altbaseline)

	anydiagin = open(filename_anydiagAge, 'r')
	anydiagin.readline() # rm header
	anydiag = csv.reader(anydiagin, delimiter=',')

	dict_anyvisit_week, dict_wk = {},{}
	for row in anydiag:
		season = int(row[0])
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		agecode = str(row[2])
		visits = int(row[3])
		dict_anyvisit_week[(wk, agecode)] = float(visits)
		dict_wk[wk] = (season, wk.isocalendar()[1]+1) # isocalendar wk number+1 because isocalendar goes from Monday to Sunday

	# estimate number of ILI cases that would have been captured in the dataset had the coverage been at 08-09 flu season levels for all years
	dict_anyvisit_season, dict_ili_season, dict_totILI53ls, dict_totILIAdjust53ls = {}, defaultdict(list), defaultdict(list), defaultdict(list)
	for s in range(1,10):
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk][0] == s])
		for age in age_keys:
			Visits = [dict_anyvisit_week[(wk, age)] for wk in dummyweeks]
			ILI = [dict_ILI_week[(wk, age)] for wk in dummyweeks]
			if len(dummyweeks) == 52:
				Visits.insert(13, (Visits[12]+Visits[13])/2.)
				ILI.insert(13, (ILI[12]+ILI[13])/2.)
			dict_anyvisit_season[(s, age)] = sum(Visits[:gp_fluweeks]) # total any diagnosis visits during flu season
			dict_ili_season[(s, age)] = ILI

		# list of lists for ili counts for all age groups
		all_lists = [dict_ili_season[(s, age)] for age in age_keys]
		# raw ili time series by season
		dict_totILI53ls[s] = [sum(ili) for ili in zip(*all_lists)]

	# create total incidence dict with coverage and ILI care-seeking adjustments
	visit9_Tpop = sum([dict_anyvisit_season[(9, age)] for age in age_keys])
	for s in range(1,10):
		visitS_Tpop = sum([dict_anyvisit_season[(s, age)] for age in age_keys])
		# adjustment for total incidence dict
		Tadjustment = visit9_Tpop/visitS_Tpop/dict_careseek_nat['T']
		dict_totILIAdjust53ls[s] = [ili*Tadjustment for ili in dict_totILI53ls[s]]

	# create age-specific incidence dict with total pop coverage and ILI care-seeking behavior adjustments
	dict_ageILIAdjust53ls = defaultdict(list)
	for key in dict_ili_season:
		s, age = key
		careseek = dict_careseek_nat[age] # defined at top
		iliDummy = dict_ili_season[key]
		visitS_Tpop = sum([dict_anyvisit_season[(s, age)] for age in age_keys])		
		# adjust ILI by coverage level in 08-09 flu season and age-specific care seeking behavior
		adjustment = visit9_Tpop/visitS_Tpop/careseek
		dict_ageILIAdjust53ls[key] = [ili*adjustment for ili in iliDummy]

	return dict_ageILIAdjust53ls, dict_totILI53ls, dict_totILIAdjust53ls

##############################################
def week_RR_processing_part2_altbaseline(dict_pop, dict_totILI53ls, dict_totILIadj53ls, dict_ageILIadj_season):
	''' Import adjusted and non-adjusted ILI cases by age group from week_OR_processing or ILINet_week_RR_processing. Summer baseline period (as opposed to fall) must be specified. Return four dicts:
	dict_totIncid53ls[s] = [incid rate per 100000 wk40,... incid rate per 100000 wk 39] (unadjusted ILI incidence)
	dict_totIncidAdj53ls[s] = [adjusted incid rate per 100000 wk 40, ...adj incid wk 39] (total population adjusted for coverage and ILI care-seeking behavior)
	dict_RR53ls[s] = [RR wk 40,... RR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
	dict_zRR53ls[s] = [zRR wk 40,... zRR wk 39] (children and adults adjusted for SDI data coverage and ILI care-seeking behavior)
		'''
	main(week_RR_processing_part2_altbaseline)

	dict_totIncid53ls, dict_totIncidAdj53ls, dict_RR53ls, dict_zRR53ls = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
	# generate adjusted incidence per 100,000 in US population, OR, and zOR at the weekly level
	allseasons = range(1,10)
	for s in allseasons:
		# total population in the season
		tot_pop = sum([dict_pop[(s, ak)] for ak in age_keys])
		# totIncid53ls dict
		dict_totIncid53ls[s] = [ili/tot_pop*100000 for ili in dict_totILI53ls[s]]
		# totIncidAdj53ls
		dict_totIncidAdj53ls[s] = [iliAdj/tot_pop*100000 for iliAdj in dict_totILIadj53ls[s]]
		# RR53ls dict
		child_attack = [adjILI/dict_pop[(s, 'C')] for adjILI in dict_ageILIadj_season[(s, 'C')]]
		adult_attack = [adjILI/dict_pop[(s, 'A')] for adjILI in dict_ageILIadj_season[(s, 'A')]]
		# 10/19/14: RR should not be evaluated if child or adult incidence is zero
		# 10/16/14 change OR to relative risk
		RR = [a/c if c and a else float('nan') for c, a in zip(child_attack, adult_attack)] 
		dict_RR53ls[s] = RR
		# zRR53ls dict
	for s in pseasons:
		normalization_period = dict_RR53ls[s-1][-gp_normweeks:]
		season_mean = np.mean(normalization_period)
		season_sd = np.std(normalization_period)
		dict_zRR53ls[s] = [(val-season_mean)/season_sd for val in dict_RR53ls[s]]

	return dict_totIncid53ls, dict_totIncidAdj53ls, dict_RR53ls, dict_zRR53ls

##############################################
def week_import_zip3(csv_incidence_region, csv_population_region):
	''' Import R_export/OR_zip3_week_outpatient_cl.csv data, which includes season number, week, zip3, age group, and ILI incid. Import R_export/popstat_zip3_season_cl.csv data, which includes calendar year, uqsza, popstat, season, age group, state, lat, long, and HHS region. Returns 4 dicts:
	dict_wk[week] = seasonnum
	dict_weekZip3_ili[(wk, zip3, age)] = ili
	dict_seasZip3_pop[(season, zip3, age)] = pop in 2nd calendar year of flu season
	dict_zip3_region[zip3] = (state, hhs)
	'''
	main(week_import_zip3)
	
	## import ILI data ##
	dict_weekZip3_ili, dict_wk = {}, {}
	for row in csv_incidence_region: 
		week, season = row[1], int(row[0])
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		zip3, age, ili = str(row[2]), str(row[3]), int(row[4])
		dict_wk[wk] = season
		dict_weekZip3_ili[(wk, zip3, age)] = ili

	## import population data ##
	dict_seasZip3_pop, dict_zip3_region = {}, {}
	for row in csv_population_region:
		season, zip3, age, pop = int(row[3]), str(row[0]), str(row[4]), int(row[2])
		state, hhs = str(row[5]), int(row[8])
		dict_seasZip3_pop[(season, zip3, age)] = pop
		dict_zip3_region[zip3] = (state, hhs)

	return dict_wk, dict_weekZip3_ili, dict_seasZip3_pop, dict_zip3_region

##############################################
def week_ILI_processing_spatial(dict_wk, dict_weekZip3_ili, dict_seasZip3_pop, dict_zip3_region, spatial_level):
	''' Aggregate ILI data from zip3 to state or region level by season and age group. Run 'week_import_zip3' first. Returns two dicts: 
	dict_seasSpatialAge_iliLS[(season, spatial, agegroup)] = [ILI cases wk 40, ... wk 39]
	dict_seasSpatial_pop[(season, spatial, agegroup)] = population in 2nd year of flu season
	'''
	main(week_ILI_processing_spatial)

	# branching for state vs. region level analysis
	if spatial_level == 'state':
		spatial_keys = list(set([dict_zip3_region[k][0] for k in dict_zip3_region]))
		# index for state info in dict_zip3_region
		code = 0
	elif spatial_level == 'region':
		spatial_keys = list(set([dict_zip3_region[k][1] for k in dict_zip3_region]))
		# index for region info in dict_zip3_region
		code = 1

	# aggregate ili to spatial level
	dict_seasSpatialAge_iliLS = defaultdict(list)
	for spatial, season in product(spatial_keys, pseasons):
		dummyzip3 = [zip3 for zip3 in dict_zip3_region if dict_zip3_region[zip3][code] == spatial]
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk] == season])
		# by age group
		for age in age_keys:
			dummyallILI_spatial = [[dict_weekZip3_ili.get((wk, zip3, age), 0) for wk in dummyweeks] for zip3 in dummyzip3]
			dict_seasSpatialAge_iliLS[(season, spatial, age)] = [sum(ili) for ili in zip(*dummyallILI_spatial)]

	# aggregate population to spatial level
	dict_seasSpatial_pop = {}
	for s, spatial, ak in product(pseasons, spatial_keys, age_keys):
		dict_seasSpatial_pop[(s, spatial, ak)] = float(sum([dict_seasZip3_pop[(s, z, ak)] for z in dict_zip3_region if dict_zip3_region[z][code] == spatial]))

	return dict_seasSpatialAge_iliLS, dict_seasSpatial_pop

##############################################
def covCareseek_adjustment_spatial(dict_seasSpatialAge_iliLS, dict_zip3_region, spatial_level):
	''' Perform SDI data coverage and ILI care-seeking adjustments at the spatial level (state or region). Analogous to coverageCareseek_adjustment (nation-level) function. Nested in week_RR_processing_spatial function. Returns four items:
	dict_spatialAgeILIadj53ls[(s, spatial, age)] = [adj ILI wk 40, ... wk 39]
	dict_spatialTotILI53ls[(s, spatial)] = [tot pop ILI wk 40, ... wk 39]
	dict_spatialTotAdjILI53ls[(s, sptatial)] = [adj tot pop ILI wk 40, ... wk 39]
	spatial_keys = sorted list of states or regions, according to spatial_level argument
	'''
	main(covCareseek_adjustment_spatial)
	
	# import any diagnosis visit data at zip3 level (total population)
	visitFilename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient_zip3.csv'
	anydiagin = open(visitFilename, 'r')
	anydiagin.readline() # rm header
	anydiag = csv.reader(anydiagin, delimiter=',')
	dict_wk, dict_weekZip3_visit = {}, {}
	for row in anydiag:
		season = int(row[0])
		week = row[1]
		wk = date(int(week[:4]), int(week[5:7]), int(week[8:]))
		zip3 = str(row[2])
		visits = float(row[3])
		dict_weekZip3_visit[(wk, zip3)] = visits
		dict_wk[wk] = season

	# branching for state vs. region level analysis
	if spatial_level == 'state':
		spatial_keys = sorted(list(set([dict_zip3_region[k][0] for k in dict_zip3_region])))
		# index for state info in dict_zip3_region
		code = 0
	elif spatial_level == 'region':
		spatial_keys = sorted(list(set([dict_zip3_region[k][1] for k in dict_zip3_region])))
		# index for region info in dict_zip3_region
		code = 1

	# aggregate any diagnosis data to spatial level of interest, add week 53 to any diagnosis and ILI data, create dict for total incidence by spatial level 
	dict_spatialTot_visits, dict_spatialAgeILI53ls, dict_spatialTotILI53ls = {}, defaultdict(list), defaultdict(list)
	for spatial, s in product(spatial_keys, pseasons):
		dummyzip3 = sorted([zip3 for zip3 in dict_zip3_region if dict_zip3_region[zip3][code] == spatial])
		dummyweeks = sorted([wk for wk in dict_wk if dict_wk[wk] == s])
		# sum total visits by zip3
		dummyallvisits_spatial = [[dict_weekZip3_visit.get((wk, zip3), 0) for wk in dummyweeks] for zip3 in dummyzip3]
		spatialVisits = [sum(visit) for visit in zip(*dummyallvisits_spatial)]
		if len(spatialVisits) == 52:
				spatialVisits.insert(13, (spatialVisits[12]+spatialVisits[13])/2.)
		# total visits during flu season
		dict_spatialTot_visits[(s, spatial)] = sum(spatialVisits[:gp_fluweeks])
		# add week 53 for age-specific ILI
		for age in age_keys:
			spatialILI = dict_seasSpatialAge_iliLS[(s, spatial, age)]
			if len(spatialILI) == 52:
				spatialILI.insert(13, (spatialILI[12]+spatialILI[13])/2.)
			# weekly ILI cases
			dict_spatialAgeILI53ls[(s, spatial, age)] = spatialILI

		# create raw total incidence dict
		all_lists = [dict_spatialAgeILI53ls[(s, spatial, age)] for age in age_keys]
		dict_spatialTotILI53ls[(s, spatial)] = [sum(ili) for ili in zip(*all_lists)]
	
	# import dict_careseek_spatial[spatial key] = weighted average of % ILI seeking
	dict_careseek_spatial = create_dict_careseek_spatial(spatial_level)

	# create total incidence dict adjusted for coverage and ILI care seeking # 10/30: convert careseek from age-specific to total pop
	visit9_Tpop = dict_spatialTot_visits[(9, spatial)]
	dict_spatialTotAdjILI53ls = defaultdict(list)
	for key in dict_spatialTotILI53ls:
		s, spatial = key
		visitS_Tpop = dict_spatialTot_visits[(s, spatial)]
		Tadjustment = visit9_Tpop/visitS_Tpop/dict_careseek_spatial[(spatial, 'T')]
		dict_spatialTotAdjILI53ls[key] = [ili*Tadjustment for ili in dict_spatialTotILI53ls[key]]
	
	# subset only CA ILI53ls
	dict_spatialCAILI53ls = dict((key, dict_spatialAgeILI53ls[key]) for key in dict_spatialAgeILI53ls if key[2] != 'O')
	# create child and adult incidence dict with total population coverage and ILI care-seeking behavior adjustments
	dict_spatialAgeILIadj53ls = defaultdict(list)
	for key in dict_spatialCAILI53ls:
		s, spatial, age = key
		careseek = dict_careseek_spatial[(spatial, age)]
		visitS_Tpop = dict_spatialTot_visits[(s, spatial)]
		iliDummy = dict_spatialAgeILI53ls[key]
		# adjust ili by coverage level in 08-09 flu season and ILI care seeking behavior in that age group
		adjustment = visit9_Tpop/visitS_Tpop/careseek
		dict_spatialAgeILIadj53ls[key] = [ili * adjustment for ili in iliDummy]

	return dict_spatialAgeILIadj53ls, dict_spatialTotILI53ls, dict_spatialTotAdjILI53ls, spatial_keys

##############################################
def create_dict_careseek_spatial(spatial_level):
	''' 10/30/14 Use Census region estimates of ILI care seeking from Biggerstaff2012 for all states in the region.
	'''
	main(create_dict_careseek_spatial)

	# import data
	filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/from_Matt/clean/ili_health_care_seek_bystate_summary.csv'
	filein = open(filename, 'r')
	filein.readline() # rm header
	csvfile = csv.reader(filein, delimiter=',')

	# dict_careseek_spatial[(spatial, age)] = proportion ILI care-seeking
	dict_careseek_spatial = {} 
	# grab values from global dict dict_careseek_census
	# 11/7/14 age-specific state estimates
	if spatial_level == 'state':
		dict_state_census = {}
		for row in csvfile:
			stateAbbr, census = str(row[1]), str(row[7])
			dict_state_census[stateAbbr] = census
			adult0910, child0910 = float(row[2]), float(row[8])
			dict_careseek_spatial[(stateAbbr, 'A')] = adult0910
			dict_careseek_spatial[(stateAbbr, 'C')] = child0910
			# assign estimate for census region if state data is 0
			if adult0910 == float(0):
				dict_careseek_spatial[(stateAbbr, 'A')] = dict_careseek_census[(census, 'A')]
			if child0910 == float(0):
				dict_careseek_spatial[(stateAbbr, 'C')] = dict_careseek_census[(census, 'C')]
		for st in dict_state_census:
			census = dict_state_census[st]
			dict_careseek_spatial[(st, 'T')] = dict_careseek_census[(census, 'T')]

	# vestigial code for region-level analysis (if ever needed again)
	# elif spatial_level == 'region':
	# 	filename = ''

	return dict_careseek_spatial

##############################################
def week_RR_processing_spatial(dict_wk, dict_seasSpatialAge_iliLS, dict_seasSpatial_pop, dict_zip3_region, spatial_level):
	''' Run function week_ILI_processing_state or region first. Function 'covCareseek_adjustment_spatial' is nested. Returns four dicts: 
	dict_spatialTotIncid53ls = [(s, spatial)] = [tot incid per 100,000 wk 40, ... wk 39]
	dict_spatialTotIncidAdj53ls = [(s, spatial)] = [adj tot incid per 100,000 wk 40, ... wk 39]
	dict_spatialRR53ls[(s, spatial)] = [RR wk 40, ... wk 39] based on adj ILI
	dict_spatialZRR53ls[(s, spatial)] = [zRR wk 40, ... wk 39] based on adj ILI
	'''
	main(week_RR_processing_spatial)

	# spatial keys == state_keys or region_keys
	dict_spatialAgeILIadj53ls, dict_spatialTotILI53ls, dict_spatialTotAdjILI53ls, spatial_keys = covCareseek_adjustment_spatial(dict_seasSpatialAge_iliLS, dict_zip3_region, spatial_level)

	dict_spatialTotIncid53ls, dict_spatialTotIncidAdj53ls, dict_spatialRR53ls, dict_spatialZRR53ls, dict_validDataCount = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), {}
	# generate total and adjusted total incidence per 100,000, relative risk in adults:children, and z-normalized relative risk at the specified "spatial_level" (state or region)
	for s, spatial in product(pseasons, spatial_keys):
		# total pop of spatial_level in the season
		spatial_pop = sum([dict_seasSpatial_pop[(s, spatial, age)] for age in age_keys])
		# spatialTotIncid53ls dict
		dict_spatialTotIncid53ls[(s, spatial)] = [ili/spatial_pop*100000 for ili in dict_spatialTotILI53ls[(s, spatial)]]
		# spatialTotIncidAdj53ls dict
		dict_spatialTotIncidAdj53ls[(s, spatial)] = [iliAdj/spatial_pop*100000 for iliAdj in dict_spatialTotAdjILI53ls[(s, spatial)]]
		# spatialRR53ls dict
		child_attack = [adjILI/dict_seasSpatial_pop[(s, spatial, 'C')] for adjILI in dict_spatialAgeILIadj53ls[(s, spatial, 'C')]]
		adult_attack = [adjILI/dict_seasSpatial_pop[(s, spatial, 'A')] for adjILI in dict_spatialAgeILIadj53ls[(s, spatial, 'A')]]
		RR = [a/c if c and a else float('nan') for c, a in zip(child_attack, adult_attack)]
		dict_spatialRR53ls[(s, spatial)] = RR
		## spatialZRR53ls dict ##
		normalization_period = dict_spatialRR53ls[(s, spatial)][:gp_normweeks]
		# mask array values that are nans
		norm_period_masked = np.ma.masked_array(normalization_period, np.isnan(normalization_period))
		# count number of 'valid norm weeks for each s-spatial combination'
		valid_normweeks = len(norm_period_masked[~norm_period_masked.mask])
		# calculate zRR only if all normweeks are available
		if valid_normweeks == gp_normweeks:
			season_mean = np.mean(norm_period_masked)
			season_sd = np.std(norm_period_masked)
			dict_spatialZRR53ls[(s, spatial)] = [((val-season_mean)/season_sd) for val in dict_spatialRR53ls[(s, spatial)]]
		else:
			# sd is 0 when there is only one value and subject to high variation with a small number of values
			dict_spatialZRR53ls[(s, spatial)] = [float('nan') for val in dict_spatialRR53ls[(s, spatial)]] 
		# number of valid normalization weeks
		dict_validDataCount[(s, spatial)] = valid_normweeks

	return dict_spatialTotIncid53ls, dict_spatialTotIncidAdj53ls, dict_spatialRR53ls, dict_spatialZRR53ls, dict_validDataCount

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
##############################################
# footer

def main(function):
	print 'Running', __name__, function.__name__

if __name__ == '__main__':
	print 'Executed from the command line'
	main()