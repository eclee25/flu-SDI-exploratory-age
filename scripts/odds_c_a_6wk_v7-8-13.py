#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 7/8/13
###Function: 
#### 1) draw OR by season charts where season is defined as the 6 weeks before and after the peak incidence week for the total population (new season definition)
#### 2) draw OR by season charts for new season definition where OR is an average of ORs across zip3s
#### 3) draw OR by AR per season for the 6 weeks before and after the peak incidence week for the total population (8/27/13)
#### 4) draw OR by AR per week for the 6 weeks before and after the peak incidence week for the total population (8/27/13)

###Import data: SQL_export/OR_swk6.csv

###Command Line: python odds_c_a_6wk_v7-8-13.py 
##############################################


### notes ###


### packages ###
import matplotlib
import csv
import matplotlib.pyplot as plt

## local packages ##
import ORgenerator as od 

### data structures ###
s6dict, ORdict, s6ARcadict, s6ARtotdict = {},{},{},{}
s6wkdict, ORwkdict, ARwkdict, wkdict = {},{},{},{}


### parameters ###
USchild = 20348657 + 20677194 + 22040343 #US child popn from 2010 Census
USadult = 21585999 + 21101849 + 19962099 + 20179642 + 20890964 + 22708591 + 22298125 + 19664805 #US adult popn from 2010 Census
seasons = range(1,11) #seasons for which ORs will be generated

### functions ###

### import data ###
s6in=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_swk6.csv','r')
s6=csv.reader(s6in, delimiter=',')
s6wkin=open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_swk6_week.csv','r')
s6wk=csv.reader(s6wkin, delimiter=',')

### plotting settings ###
colorvec = ['grey', 'black', 'red', 'orange', 'gold', 'green', 'blue', 'cyan', 'darkviolet', 'hotpink']
labelvec = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10']

### program ###

# OR by season chart

# s6dict[(seasonnum, age marker)] = ILI ct
s6dict = od.import_d(s6, 0, 1, 2)
# ORdict[seasonnum] = OR
ORdict = od.ORgen_seas(s6dict, seasons)
# s6ARcadict[seasonnum] = (child attack rate per 1000, adult attack rate per 1000)
# s6ARtotdict[seasonnum] = total attack rate per 100000 # see OR vs AR chart
s6ARcadict, s6ARtotdict = od.ARdict_seas(s6dict, seasons)
keys = [int(key) for key in sorted(ORdict.keys())]
values = [ORdict[k] for k in sorted(ORdict.keys())]
print keys #order in which seasons will be plotted
# plot OR by season chart
plt.plot(keys, values, marker='o', color = 'black', label= "total")
plt.xlabel('Season number')
plt.ylabel('Attack Rate OR, c:a (US pop normalized, peak +/- 6wks)')
plt.show()
# output data file of attack rates
# with open('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/AR1000_s6_season.txt', 'a') as f:
# 	for k,v in s6ARdict.iteritems():
# 		print k,v
# 		f.write(str(k)) # season number
# 		f.write(',')
# 		f.write(str(v[0])) # child attack rate per 1000 for peak season
# 		f.write(',')
# 		f.write(str(v[1])) # adult attack rate per 1000 for peak season
# 		f.write('\n')
# f.close() # exported on 8/6/13


# OR by week chart
# s6wkdict[(week, age marker)] = ILI
# wkdict[week] = seasonnum
s6wkdict, wkdict, weeks = od.import_dwk(s6wk, 0, 1, 2, 3)
# ORwkdict[week] = OR
# ARwkdict[week] = total attack rate per 10000 # save for OR by AR per week chart
ORwkdict, ARwkdict = od.ORgen_wk(s6wkdict, weeks) 
for s in seasons:
	wkdummy = [key for key in sorted(weeks) if wkdict[key] == int(s)]
	wkdummy = set(wkdummy)
# 	print sorted(wkdummy) # edit ECL 6/12 wkdummy needs to be sorted because dictionary values don't have an order. y-axis ORs need to match the correct week number
	y = [ORwkdict[item] for item in sorted(wkdummy)]
	x = range(7-len(wkdummy), 7)
	print "season", s, len(wkdummy)
	plt.plot(x, y, marker='o', color = colorvec[s-1], label= labelvec[s-1], linewidth = 2)
plt.xlim([-6, 6])
plt.ylim([1,10])
plt.xlabel('Week Number')
plt.ylabel('Attack Rate OR, c:a (US pop normalized, peak +/- 6wks)')
plt.legend(loc="upper right")
plt.show()


# OR by AR per season chart
ARvals = [s6ARtotdict[k] for k in sorted(ORdict)]
ORvals = [ORdict[k] for k in sorted(ORdict)]
#order in which seasons will be plotted (check)
print "plotted order of season in OR by AR:", sorted(ORdict) 
# plot OR by AR season chart
plt.scatter(ARvals, ORvals, marker='o', color = 'black', label= "total")
for k, AR, OR in zip(sorted(ORdict), ARvals, ORvals):
	plt.annotate(k, xy = (AR, OR), xytext = (5,0), textcoords = 'offset points')
plt.xlabel('Peak Season Attack Rate per 100,000 (US pop)')
plt.ylabel('Attack Rate OR, c:a (US pop normalized, peak +/- 6wks)')
plt.show()


# OR by AR per week chart
# ARwkdict[week] = total attack rate per 10000 # save for OR by AR per week chart
wkdummy = [key for key in sorted(weeks)]
wkdummy = set(wkdummy)
ORvals = [ORwkdict[week] for week in sorted(wkdummy)]
ARvals = [ARwkdict[week] for week in sorted(wkdummy)]
print "num points in OR by AR per wk:", len(ARvals)
plt.scatter(ARvals, ORvals, marker='o', color = 'black', label= 'total')
plt.xlabel('Peak Season Attack Rate per 10,000 (US pop)')
plt.ylabel('Attack Rate OR, c:a (US pop normalized, peak +/- 6wks)')
plt.legend(loc="upper right")
plt.show()

