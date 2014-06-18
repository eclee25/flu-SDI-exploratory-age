#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 6/18/14
###Function: Clean age-specific estimates of population size that were obtained from US Census

###Import data: /Census/Source_Data/*.csv

###Command Line: python clean_pop_age_Census.py
##############################################


### notes ###


### packages/modules ###
import csv
from collections import defaultdict
from itertools import product

### functions ###
def print_dictionary_to_file(dic, filename):
	with open(filename, 'w+') as fwriter:
		for key, value in dic.items():
			fwriter.write("%s,%s,%s\n" % (key[0],key[1],value))

# d_pop[(seasonnum, agecode)] = population size
d_pop = {}


##############################################
## clean 2000 to 2010 pop by age data ##

### data structures ###
# d_yr_pop[ages] = [pop in yr 1, pop in yr 2,...]
d_yr_pop = defaultdict(list)

### parameters ###
years = xrange(2003, 2013)
ages4 = ['<5', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95-99', '100+']

### import data ###
filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/US-EST00INT-01.csv'
skip = 5 # number of rows to skip at top of file (7 rows before All Ages starting 2007)
lines = 21

with open(filename,'r') as datain:
	while skip:
		datain.next()
		skip -= 1
	data = csv.reader(datain, delimiter=',')
	for row in data:
		row2 = [val.replace(',', '').strip('.') for val in row][1:] # rm age group
		key = ages4.pop(0)
		# d_yr_pop[ages] = [pop in yr 1, pop in yr 2,...]
		d_yr_pop[key] = [int(val) for val in row2]
		lines -= 1
		if lines < 1:
			break

ages4 = ['<5', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95-99', '100+']
agecodes = list('OCCCCAAAAAAAAOOOOOOOO')
# d_ages[ages] = agecode
d_ages = dict(zip(ages4, agecodes))

# d_code_pop[agecode] = [pop in yr 1, pop in yr 2, ...]
d_code_pop = defaultdict(list)
for i in xrange(12): # rm July 2010 est. (last value in row2)
	if i != 1: # rm July 2000 est. 
		d_code_pop['C'].append(sum([d_yr_pop[key][i] for key in d_yr_pop if d_ages[key] == 'C']))
		d_code_pop['A'].append(sum([d_yr_pop[key][i] for key in d_yr_pop if d_ages[key] == 'A']))
		d_code_pop['O'].append(sum([d_yr_pop[key][i] for key in d_yr_pop if d_ages[key] == 'O']))

# d_pop[(seasonnum, agecode)] = population size
for key, snum in product(d_code_pop, xrange(11)):
	d_pop[(snum, key)] = d_code_pop[key][snum]


##############################################
## clean 1998-99 pop by age data ##

fns9899 = ['/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/US-EST90INT-07-1998.csv', '/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/US-EST90INT-07-1999.csv']

### data structures ###
# d_singleage[ageyear] = population size
d_singleage9899 = {}

for filename, snum in zip(fns9899, xrange(-2,0)):
	skip = 3
	lines = 102

	with open(filename, 'r') as datain:
		while skip:
			datain.next()
			skip -= 1
		data = csv.reader(datain, delimiter=',')
		for row in data:
			# d_singleage[ageyear] = population size
			d_singleage9899[row[1]] = int(row[2])
			lines -= 1
			if lines < 1:
				break

	d_pop[(snum, 'C')] = sum([d_singleage9899[str(key)] for key in range(5, 25)])
	d_pop[(snum, 'A')] = sum([d_singleage9899[str(key)] for key in range(25, 65)])
	d_pop[(snum, 'O')] = d_singleage9899['All Age'] - d_pop[(snum, 'C')] - d_pop[(snum, 'A')]

##############################################
## clean 2011-13 pop by age data ##
fns1113 = ['/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/NC-EST2012-ALLDATA-R-File03-Jan2011.csv', '/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/NC-EST2012-ALLDATA-R-File05-Jan2012.csv', '/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/NC-EST2012-ALLDATA-R-File07-Jan2013.csv']

### data structures ###
# d_singleage[ageyear] = population size
d_singleage = {}

for filename, snum in zip(fns1113, xrange(11,14)):
	skip = 1
	lines = 102

	with open(filename, 'r') as datain:
		while skip:
			datain.next()
			skip -= 1
		data = csv.reader(datain, delimiter=',')
		for row in data:
			# d_singleage[ageyear] = population size
			d_singleage[row[3]] = int(row[4])
			lines -= 1
			if lines < 1:
				break

	d_pop[(snum, 'C')] = sum([d_singleage[str(key)] for key in range(5, 25)])
	d_pop[(snum, 'A')] = sum([d_singleage[str(key)] for key in range(25, 65)])
	d_pop[(snum, 'O')] = d_singleage['999'] - d_pop[(snum, 'C')] - d_pop[(snum, 'A')]

##############################################
## clean 2014 pop by age data ##
# grab month 12 from 2013 as closest approximation of 2014 data (so 2014 must be done separately from 2011-13)

### data structures ###
# d_singleage[ageyear] = population size
d_singleage14 = {}

filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Source_Data/NC-EST2012-ALLDATA-R-File08-Dec2013.csv'
skip = 511 
lines = 102

with open(filename, 'r') as datain:
	while skip:
		datain.next()
		skip -= 1
	data = csv.reader(datain, delimiter=',')
	for row in data:
		# d_singleage[ageyear] = population size
		d_singleage14[row[3]] = int(row[4])
		lines -= 1
		if lines < 1:
			break

d_pop[(14, 'C')] = sum([d_singleage14[str(key)] for key in range(5, 25)])
d_pop[(14, 'A')] = sum([d_singleage14[str(key)] for key in range(25, 65)])
d_pop[(14, 'O')] = d_singleage14['999'] - d_pop[(14, 'C')] - d_pop[(14, 'A')]

##############################################
# check values
print '14', [d_pop[key] for key in d_pop if key[0]==14]
print '12', [d_pop[key] for key in d_pop if key[0]==12]
print '8', [d_pop[key] for key in d_pop if key[0]==8]
print '-2', [d_pop[key] for key in d_pop if key[0]==-2]

##############################################
## print d_pop to file ##
filename = '/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data/totalpop_age_Census_98-14.csv'
print_dictionary_to_file(d_pop, filename)
# written to file 6/18/14, 17:24
##############################################