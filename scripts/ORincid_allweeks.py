#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 9/15/13
###Function: OR by week and child & adult incidence by week with two axes
#### Allow us to compare the OR values by the magnitude of infection in children and adults

###Import data: OR_allweeks.csv

###Command Line: python 
##############################################


### notes ###


### packages/modules ###
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys

## local modules ##
import ORgenerator as od 

### data structures ###
# ilidict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
# weeks = list of unique weeks in the data
# ORdict[week] = OR
# ageARdict[week] = (child attack rate per 100,000, adult attack rate per 100,000)

### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn from 2010 Census
seasons = range(2,11) #seasons for which ORs will be generated

### plotting settings ###
xlabels = range(40,54)
xlabels.extend(range(1,40))
ORmarker = 'o'
incidmarker = '^'
ORcol = 'black'
chcol = 'red'
adcol = 'blue'

### functions ###

### import data ###
datain=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_allweeks.csv','r')
data=csv.reader(datain, delimiter=',')

ilidict, wkdict, weeks = od.import_dwk(data, 0, 1, 2, 3)
ORdict, ageARdict = od.ORincid_wk(ilidict, weeks)

# OR and attack rate chart (two axes) for each season
for s in seasons:
	# wkdummy will represent list of weeks for chart in season to use as key for OR dict
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy) # wkdummy needs to be sorted bc dict values don't have order when pulling dict values in list comprehension
	# create two y-axes
	fig, yax_OR = plt.subplots()
	yax_AR = yax_OR.twinx()
	
	# for seasons with 53 weeks (season 5 only)
	if len(wkdummy) == 53:
		## OR y-axis
		chartORs = [ORdict[wk] for wk in sorted(wkdummy)]
		chartwks = xrange(len(sorted(wkdummy)))
		OR, = yax_OR.plot(chartwks, chartORs, marker = ORmarker, color = ORcol, label = "Odds Ratio", lw = 4, ms = 8)
		
		## incidence y-axis (one line each for child and adult AR)
		c_AR = [ageARdict[wk][0] for wk in sorted(wkdummy)]
		a_AR = [ageARdict[wk][1] for wk in sorted(wkdummy)]
		child, = yax_AR.plot(chartwks, c_AR, marker = incidmarker, color = chcol, label = 'Child Attack Rate', lw = 3, ms = 8)
		adult, = yax_AR.plot(chartwks, a_AR, marker = incidmarker, color = adcol, label = 'Adult Attack Rate', lw = 3, ms = 8)	
	
		## designate legend labels
		lines = [OR, child, adult]
		yax_OR.legend(lines, [l.get_label() for l in lines], loc = 'upper right')

	# for seasons with 52 weeks
	else: 
		## OR y-axis
		chartORs = [ORdict[wk] for wk in sorted(wkdummy)]
		avg53 = (chartORs[12] + chartORs[13])/2
		chartORs.insert(13, avg53)
		chartwks = xrange(len(sorted(wkdummy)) + 1)
		OR, = yax_OR.plot(chartwks, chartORs, marker = ORmarker, color = ORcol, label = "Odds Ratio", lw = 4, ms = 8)
		
		## incidence y-axis
		c_AR = [ageARdict[wk][0] for wk in sorted(wkdummy)]
		a_AR = [ageARdict[wk][1] for wk in sorted(wkdummy)]
		avgc = (c_AR[12] + c_AR[13])/2
		avga = (a_AR[12] + a_AR[13])/2
		c_AR.insert(13, avgc)
		a_AR.insert(13, avga)
		child, = yax_AR.plot(chartwks, c_AR, marker = incidmarker, color = chcol, label = 'Child Incidence Rate', lw = 3, ms = 8)
		adult, = yax_AR.plot(chartwks, a_AR, marker = incidmarker, color = adcol, label = 'Adult Incidence Rate', lw = 3, ms = 8)

		## designate legend labels
		lines = [OR, child, adult]
		yax_OR.legend(lines, [l.get_label() for l in lines], loc = 'upper right')

	## separate flu and off seasons
	plt.plot([33, 33], [0, 100], color = 'k', linewidth = 1)

	## plot settings
	yax_OR.set_xlabel('Week Number, Season ' + str(s), fontsize=24)
	yax_OR.set_ylim([0, 10])
	yax_OR.set_ylabel('OR, child:adult', fontsize=24)
	yax_AR.set_ylim([0, 100])
	yax_AR.set_yticks(xrange(0,110,10))
	yax_AR.set_ylabel('Incidence Rate per 100,000', fontsize=24)
	plt.xlim([0, 52])
	plt.xticks(xrange(53), xlabels)
	plt.show()










