#!/usr/bin/python

##############################################
###Python template
###Author: Elizabeth Lee
###Date: 10/10/12
###Function: Draw exploratory charts for SDI data
###Import data: A1, A2, A3, B3, C1, C2, C3

###Command Line: ipython DrawCharts.py
##############################################

### notes ###
# can't read the same file multiple times in one program
# python closing index values are one greater than the actual index

### packages ###
import matplotlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## local packages ##


### data structures ###
yr=[]
wknum=[]
mag=[]
x01=[]
y01=[]
x02=[]
y02=[]
x03=[]
y03=[]
x04=[]
y04=[]
x05=[]
y05=[]
x06=[]
y06=[]
x07=[]
y07=[]
x08=[]
y08=[]
x09=[]
y09=[]
x=[]
y2yr=[]
y2_4yr=[]
y5_19yr=[]
y20_29yr=[]
y30_49yr=[]
y50_69yr=[]
y70yr=[]
wks_by_season=[]
peak=[]
weeks=[]
peakwk=[]
peakwk_shifted=[]
### parameters ###
#for single season charts
nextyr=np.arange(1,40,1)
firstyr=np.arange(40,54,1)
yr1 = '2001'
yr2 = '2002'
season = yr1+'-'+yr2
#for peak week charts
s_peak=0
s_wk=0
s_numshift=0
s_num=0
yax=[]
agelabel = ['<2 years', '2-4 years', '5-19 years', '20-29 years', '30-49 years', '50-69 years', '70+ years']
yr1vec = [2001,2002,2003,2004,2005,2006,2007,2008,2009]
yr2vec = [2002,2003,2004,2005,2006,2007,2008,2009,2010]

### functions ###
def G4season (csvreadfile, agevec): 
	for row in csvreadfile:
		yr = row[2][:4]
		wknum = int(row[3])
		month = row[2][5:7]
		if yr == yr1 and wknum in firstyr and month != "01":
			agevec.append(row[6])
			wks_by_season.append(wknum)
			weeks.append(row[2])
		elif yr == yr2 and wknum in nextyr:
			agevec.append(row[6])
			wks_by_season.append(wknum)
			weeks.append(row[2])
		else:
			continue
def peakweek (csvreadfile, peakval, wkval, numval, peakwkval, yearct): # week numbers for peaks do not appear to be correct, 
	ct=0
	for row in csvreadfile:
		yr = int(row[2][:4])
		wknum = int(row[3])
		month = row[2][5:7]
		null = float(row[6])
		if ((yr==yr1vec[yearct] and wknum in firstyr and month != "01") or (yr==yr2vec[yearct] and wknum in nextyr)):
			ct+=1
			if null>peakval:
				peakval=float(row[6])
				wkval=row[2]
				numval=ct
				peakwkval=int(row[3])
	peak.append(peakval)
	weeks.append(wkval)
	peakwk_shifted.append(numval)
	peakwk.append(peakwkval) #not needed for plotting, just as a check
def season_grabaxes (csvreadfile): #2001 and 2002 have 52 weeks
	ct=0
	for row in csvreadfile:
		yr = row[2][:4]
		wknum = int(row[3])
		month = row[2][5:7]
		if ((yr=='2001' and wknum in firstyr and month != "01") or (yr=='2002' and wknum in nextyr)):
			ct += 1
			yax.append(ct)
			wks_by_season.append(wknum)

### import data ###
A1in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/A1.csv','r')
A2in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/A2.csv','r')
A3in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/A3.csv','r')
B3in=A3in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/B3.csv','r')
C1in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/R_export/C1.csv','r')
C2in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/R_export/C2.csv','r')
C3in=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/R_export/C3.csv','r')
D1ain=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D1a.csv','r')
D1cin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D1c.csv','r')
D1din=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D1d.csv','r')
D1fin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D1f.csv','r')
E1cin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E1c.csv','r')
E1fin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E1f.csv','r')
E4ain=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
D4ain=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4a.csv','r')
D4bin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4b.csv','r')
D4cin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4c.csv','r')
D4din=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4d.csv','r')
D4ein=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4e.csv','r')
D4fin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4f.csv','r')
D4gin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/D4g.csv','r')
G4ain=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')

E4ain_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
E4ain_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
E4ain_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
E4ain_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
E4ain_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
E4ain_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')
E4ain_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4a.csv','r')
E4bin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4b.csv','r')
E4cin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4c.csv','r')
E4din_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4d.csv','r')
E4ein_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4e.csv','r')
E4fin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4f.csv','r')
E4gin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/E4g.csv','r')

G4ain_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_2=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')
G4ain_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_3=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')
G4ain_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_4=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')
G4ain_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_5=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')
G4ain_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_6=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')
G4ain_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_7=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')
G4ain_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4a.csv','r')
G4bin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4b.csv','r')
G4cin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4c.csv','r')
G4din_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4d.csv','r')
G4ein_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4e.csv','r')
G4fin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4f.csv','r')
G4gin_8=open('/home/elizabeth/Documents/Georgetown/Bansal/SDI/SQL_export/G4g.csv','r')

A1=csv.reader(A1in, delimiter=',')
A2=csv.reader(A2in, delimiter=',')
A3=csv.reader(A3in, delimiter=',')
B3=csv.reader(B3in, delimiter=',')
C1=csv.reader(C1in, delimiter=',')
C2=csv.reader(C2in, delimiter=',')
C3=csv.reader(C3in, delimiter=',')
D1a=csv.reader(D1ain, delimiter=',')
D1c=csv.reader(D1cin, delimiter=',')
D1d=csv.reader(D1din, delimiter=',')
D1f=csv.reader(D1fin, delimiter=',')
E1c=csv.reader(E1cin, delimiter=',')
E1f=csv.reader(E1fin, delimiter=',')
E4a=csv.reader(E4ain, delimiter=',')
E4b=csv.reader(E4bin, delimiter=',')
E4c=csv.reader(E4cin, delimiter=',')
E4d=csv.reader(E4din, delimiter=',')
E4e=csv.reader(E4ein, delimiter=',')
E4f=csv.reader(E4fin, delimiter=',')
E4g=csv.reader(E4gin, delimiter=',')
D4a=csv.reader(D4ain, delimiter=',')
D4b=csv.reader(D4bin, delimiter=',')
D4c=csv.reader(D4cin, delimiter=',')
D4d=csv.reader(D4din, delimiter=',')
D4e=csv.reader(D4ein, delimiter=',')
D4f=csv.reader(D4fin, delimiter=',')
D4g=csv.reader(D4gin, delimiter=',')
G4a=csv.reader(G4ain, delimiter=',')
G4b=csv.reader(G4bin, delimiter=',')
G4c=csv.reader(G4cin, delimiter=',')
G4d=csv.reader(G4din, delimiter=',')
G4e=csv.reader(G4ein, delimiter=',')
G4f=csv.reader(G4fin, delimiter=',')
G4g=csv.reader(G4gin, delimiter=',')

E4a_2=csv.reader(E4ain_2, delimiter=',')
E4b_2=csv.reader(E4bin_2, delimiter=',')
E4c_2=csv.reader(E4cin_2, delimiter=',')
E4d_2=csv.reader(E4din_2, delimiter=',')
E4e_2=csv.reader(E4ein_2, delimiter=',')
E4f_2=csv.reader(E4fin_2, delimiter=',')
E4g_2=csv.reader(E4gin_2, delimiter=',')
E4a_3=csv.reader(E4ain_3, delimiter=',')
E4b_3=csv.reader(E4bin_3, delimiter=',')
E4c_3=csv.reader(E4cin_3, delimiter=',')
E4d_3=csv.reader(E4din_3, delimiter=',')
E4e_3=csv.reader(E4ein_3, delimiter=',')
E4f_3=csv.reader(E4fin_3, delimiter=',')
E4g_3=csv.reader(E4gin_3, delimiter=',')
E4a_4=csv.reader(E4ain_4, delimiter=',')
E4b_4=csv.reader(E4bin_4, delimiter=',')
E4c_4=csv.reader(E4cin_4, delimiter=',')
E4d_4=csv.reader(E4din_4, delimiter=',')
E4e_4=csv.reader(E4ein_4, delimiter=',')
E4f_4=csv.reader(E4fin_4, delimiter=',')
E4g_4=csv.reader(E4gin_4, delimiter=',')
E4a_5=csv.reader(E4ain_5, delimiter=',')
E4b_5=csv.reader(E4bin_5, delimiter=',')
E4c_5=csv.reader(E4cin_5, delimiter=',')
E4d_5=csv.reader(E4din_5, delimiter=',')
E4e_5=csv.reader(E4ein_5, delimiter=',')
E4f_5=csv.reader(E4fin_5, delimiter=',')
E4g_5=csv.reader(E4gin_5, delimiter=',')
E4a_6=csv.reader(E4ain_6, delimiter=',')
E4b_6=csv.reader(E4bin_6, delimiter=',')
E4c_6=csv.reader(E4cin_6, delimiter=',')
E4d_6=csv.reader(E4din_6, delimiter=',')
E4e_6=csv.reader(E4ein_6, delimiter=',')
E4f_6=csv.reader(E4fin_6, delimiter=',')
E4g_6=csv.reader(E4gin_6, delimiter=',')
E4a_7=csv.reader(E4ain_7, delimiter=',')
E4b_7=csv.reader(E4bin_7, delimiter=',')
E4c_7=csv.reader(E4cin_7, delimiter=',')
E4d_7=csv.reader(E4din_7, delimiter=',')
E4e_7=csv.reader(E4ein_7, delimiter=',')
E4f_7=csv.reader(E4fin_7, delimiter=',')
E4g_7=csv.reader(E4gin_7, delimiter=',')
E4a_8=csv.reader(E4ain_8, delimiter=',')
E4b_8=csv.reader(E4bin_8, delimiter=',')
E4c_8=csv.reader(E4cin_8, delimiter=',')
E4d_8=csv.reader(E4din_8, delimiter=',')
E4e_8=csv.reader(E4ein_8, delimiter=',')
E4f_8=csv.reader(E4fin_8, delimiter=',')
E4g_8=csv.reader(E4gin_8, delimiter=',')

G4a_2=csv.reader(G4ain_2, delimiter=',')
G4b_2=csv.reader(G4bin_2, delimiter=',')
G4c_2=csv.reader(G4cin_2, delimiter=',')
G4d_2=csv.reader(G4din_2, delimiter=',')
G4e_2=csv.reader(G4ein_2, delimiter=',')
G4f_2=csv.reader(G4fin_2, delimiter=',')
G4g_2=csv.reader(G4gin_2, delimiter=',')
G4a_3=csv.reader(G4ain_3, delimiter=',')
G4b_3=csv.reader(G4bin_3, delimiter=',')
G4c_3=csv.reader(G4cin_3, delimiter=',')
G4d_3=csv.reader(G4din_3, delimiter=',')
G4e_3=csv.reader(G4ein_3, delimiter=',')
G4f_3=csv.reader(G4fin_3, delimiter=',')
G4g_3=csv.reader(G4gin_3, delimiter=',')
G4a_4=csv.reader(G4ain_4, delimiter=',')
G4b_4=csv.reader(G4bin_4, delimiter=',')
G4c_4=csv.reader(G4cin_4, delimiter=',')
G4d_4=csv.reader(G4din_4, delimiter=',')
G4e_4=csv.reader(G4ein_4, delimiter=',')
G4f_4=csv.reader(G4fin_4, delimiter=',')
G4g_4=csv.reader(G4gin_4, delimiter=',')
G4a_5=csv.reader(G4ain_5, delimiter=',')
G4b_5=csv.reader(G4bin_5, delimiter=',')
G4c_5=csv.reader(G4cin_5, delimiter=',')
G4d_5=csv.reader(G4din_5, delimiter=',')
G4e_5=csv.reader(G4ein_5, delimiter=',')
G4f_5=csv.reader(G4fin_5, delimiter=',')
G4g_5=csv.reader(G4gin_5, delimiter=',')
G4a_6=csv.reader(G4ain_6, delimiter=',')
G4b_6=csv.reader(G4bin_6, delimiter=',')
G4c_6=csv.reader(G4cin_6, delimiter=',')
G4d_6=csv.reader(G4din_6, delimiter=',')
G4e_6=csv.reader(G4ein_6, delimiter=',')
G4f_6=csv.reader(G4fin_6, delimiter=',')
G4g_6=csv.reader(G4gin_6, delimiter=',')
G4a_7=csv.reader(G4ain_7, delimiter=',')
G4b_7=csv.reader(G4bin_7, delimiter=',')
G4c_7=csv.reader(G4cin_7, delimiter=',')
G4d_7=csv.reader(G4din_7, delimiter=',')
G4e_7=csv.reader(G4ein_7, delimiter=',')
G4f_7=csv.reader(G4fin_7, delimiter=',')
G4g_7=csv.reader(G4gin_7, delimiter=',')
G4a_8=csv.reader(G4ain_8, delimiter=',')
G4b_8=csv.reader(G4bin_8, delimiter=',')
G4c_8=csv.reader(G4cin_8, delimiter=',')
G4d_8=csv.reader(G4din_8, delimiter=',')
G4e_8=csv.reader(G4ein_8, delimiter=',')
G4f_8=csv.reader(G4fin_8, delimiter=',')
G4g_8=csv.reader(G4gin_8, delimiter=',')

### program ###
#for row in A1:	
#	x = np.arange(2000,2011,1)
#	y = row[2:]
#	plt.plot(x,y,label=row[1])
#plt.legend(loc=2)
#plt.ylabel('Number of ILI cases')
#plt.show()

#for row in A2:	
#	x = np.arange(2000,2011,1)
#	y = row[2:]
#	plt.plot(x,y,label=row[1])
#plt.legend(loc=2)
#plt.ylabel('Number of total visits')
#plt.show()

#for row in A3:	
#	x = np.arange(2000,2011,1)
#	y = row[2:]
#	plt.plot(x,y,label=row[1])
#plt.legend(loc=2)
#plt.ylabel('Proportion of ILI cases from total visits')
#plt.axis([2000,2010,0,0.1])
#plt.show()

#for row in B3:
#	yr.append(int(row[1]))
#	wknum.append(int(row[3]))
#	mag.append(float(row[4]))
#mag2 = array(mag)*5000
#scatter(yr,wknum,marker = 'o',s=mag2)
#plt.ylabel('Week Number')
#plt.xlabel('Year')
#plt.text(1999,30,'Week 1-11: Winter\nWeek 12-24: Spring\nWeek 25-37: Summer\nWeek 38-50: Fall\nWeek 51-52: Winter')
#plt.text(1999,-7,'Peak season is defined as ILI proportion > .02 for 10-14 year olds')
#plt.show()

#ct=0
#dates=[]
#for row in C1:
#	if ct==0:
#		dates=row[1:]
#		ct+=1
#		continue
#	if row[1]=='NA':
#		row[1]=0
#	x = np.arange(0,496,1)
#	y = row[1:]
#	plt.plot(x,y,label=row[0])
#	ct+=1
#plt.legend(loc=2)
#plt.ylabel('Number of ILI cases')
#plt.show()

#ct=0
#dates=[]
#for row in C2:
#	if ct==0:
#		dates=row[1:]
#		ct+=1
#		continue
#	if row[1]=='NA':
#		row[1]=0
#	x = np.arange(0,496,1)
#	y = row[1:]
#	plt.plot(x,y,label=row[0])
#	ct+=1
#plt.legend(loc=2)
#plt.ylabel('Number of total visits')
#plt.show()

#ct=0
#dates=[]
#for row in C3:
#	if ct==0:
#		dates=row[1:]
#		ct+=1
#		continue
#	if row[1]=='NA':
#		row[1]=0
#	x = np.arange(0,496,1)
#	y = row[1:]
#	plt.plot(x,y,label=row[0])
#	ct+=1
#plt.legend(loc=2)
#plt.ylabel('Proportion of ILI cases from total visits')
#plt.show()

#for row in D1a:
#	yr = row[2][:4]
#	if yr == "2000" or yr == "2010":
#		continue
#	if yr == '2001':
#		x01.append(row[3])
#		y01.append(row[4])
#	elif yr == '2002':
#		x02.append(row[3])
#		y02.append(row[4])
#	elif yr == '2003':
#		x03.append(row[3])
#		y03.append(row[4])
#	elif yr == '2004':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]=='53':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]<'53':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]=='52':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]<'52':
#		x06.append(row[3])
#		y06.append(row[4])
#	elif yr == '2007':
#		x07.append(row[3])
#		y07.append(row[4])
#	elif yr == '2008':
#		x08.append(row[3])
#		y08.append(row[4])
#	elif yr == '2009':
#		x09.append(row[3])
#		y09.append(row[4])
#plt.plot(x01,y01, label = '2001')
#plt.plot(x02,y02, label = '2002')
#plt.plot(x03,y03, label = '2003')
#plt.plot(x04,y04, label = '2004')
#plt.plot(x05,y05, label = '2005')
#plt.plot(x06,y06, label = '2006')
#plt.plot(x07,y07, label = '2007')
#plt.plot(x08,y08, label = '2008')
#plt.plot(x09,y09, label = '2009')
#plt.legend(loc=2)
#plt.xlim(xmax=55)
#plt.ylabel('Number of ER ILI cases, ages <2')
#plt.xlabel('Week Number')
#plt.show()

#for row in D1c:
#	yr = row[2][:4]
#	if yr == "2000" or yr == "2010":
#		continue
#	if yr == '2001':
#		x01.append(row[3])
#		y01.append(row[4])
#	elif yr == '2002':
#		x02.append(row[3])
#		y02.append(row[4])
#	elif yr == '2003':
#		x03.append(row[3])
#		y03.append(row[4])
#	elif yr == '2004':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]=='53':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]<'53':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]=='52':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]<'52':
#		x06.append(row[3])
#		y06.append(row[4])
#	elif yr == '2007':
#		x07.append(row[3])
#		y07.append(row[4])
#	elif yr == '2008':
#		x08.append(row[3])
#		y08.append(row[4])
#	elif yr == '2009':
#		x09.append(row[3])
#		y09.append(row[4])
#plt.plot(x01,y01, label = '2001')
#plt.plot(x02,y02, label = '2002')
#plt.plot(x03,y03, label = '2003')
#plt.plot(x04,y04, label = '2004')
#plt.plot(x05,y05, label = '2005')
#plt.plot(x06,y06, label = '2006')
#plt.plot(x07,y07, label = '2007')
#plt.plot(x08,y08, label = '2008')
#plt.plot(x09,y09, label = '2009')
#plt.legend(loc=2)
#plt.xlim(xmax=55)
#plt.ylabel('Number of ER ILI cases, ages 5-19')
#plt.xlabel('Week Number')
#plt.show()

#for row in D1d:
#	yr = row[2][:4]
#	if yr == "2000" or yr == "2010":
#		continue
#	if yr == '2001':
#		x01.append(row[3])
#		y01.append(row[4])
#	elif yr == '2002':
#		x02.append(row[3])
#		y02.append(row[4])
#	elif yr == '2003':
#		x03.append(row[3])
#		y03.append(row[4])
#	elif yr == '2004':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]=='53':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]<'53':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]=='52':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]<'52':
#		x06.append(row[3])
#		y06.append(row[4])
#	elif yr == '2007':
#		x07.append(row[3])
#		y07.append(row[4])
#	elif yr == '2008':
#		x08.append(row[3])
#		y08.append(row[4])
#	elif yr == '2009':
#		x09.append(row[3])
#		y09.append(row[4])
#plt.plot(x01,y01, label = '2001')
#plt.plot(x02,y02, label = '2002')
#plt.plot(x03,y03, label = '2003')
#plt.plot(x04,y04, label = '2004')
#plt.plot(x05,y05, label = '2005')
#plt.plot(x06,y06, label = '2006')
#plt.plot(x07,y07, label = '2007')
#plt.plot(x08,y08, label = '2008')
#plt.plot(x09,y09, label = '2009')
#plt.legend(loc=2)
#plt.xlim(xmax=55)
#plt.ylabel('Number of ER ILI cases, ages 20-29')
#plt.xlabel('Week Number')
#plt.show()

#for row in D1f:
#	yr = row[2][:4]
#	if yr == "2000" or yr == "2010":
#		continue
#	if yr == '2001':
#		x01.append(row[3])
#		y01.append(row[4])
#	elif yr == '2002':
#		x02.append(row[3])
#		y02.append(row[4])
#	elif yr == '2003':
#		x03.append(row[3])
#		y03.append(row[4])
#	elif yr == '2004':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]=='53':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]<'53':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]=='52':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]<'52':
#		x06.append(row[3])
#		y06.append(row[4])
#	elif yr == '2007':
#		x07.append(row[3])
#		y07.append(row[4])
#	elif yr == '2008':
#		x08.append(row[3])
#		y08.append(row[4])
#	elif yr == '2009':
#		x09.append(row[3])
#		y09.append(row[4])
#plt.plot(x01,y01, label = '2001')
#plt.plot(x02,y02, label = '2002')
#plt.plot(x03,y03, label = '2003')
#plt.plot(x04,y04, label = '2004')
#plt.plot(x05,y05, label = '2005')
#plt.plot(x06,y06, label = '2006')
#plt.plot(x07,y07, label = '2007')
#plt.plot(x08,y08, label = '2008')
#plt.plot(x09,y09, label = '2009')
#plt.legend(loc=1)
#plt.xlim(xmax=55)
#plt.ylabel('Number of ER ILI cases, ages 50-69')
#plt.xlabel('Week Number')
#plt.show()

#for row in E1c:
#	yr = row[2][:4]
#	if yr == "2000" or yr == "2010":
#		continue
#	if yr == '2001':
#		x01.append(row[3])
#		y01.append(row[4])
#	elif yr == '2002':
#		x02.append(row[3])
#		y02.append(row[4])
#	elif yr == '2003':
#		x03.append(row[3])
#		y03.append(row[4])
#	elif yr == '2004':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]=='53':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]<'53':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]=='52':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]<'52':
#		x06.append(row[3])
#		y06.append(row[4])
#	elif yr == '2007':
#		x07.append(row[3])
#		y07.append(row[4])
#	elif yr == '2008':
#		x08.append(row[3])
#		y08.append(row[4])
#	elif yr == '2009':
#		x09.append(row[3])
#		y09.append(row[4])
#plt.plot(x01,y01, label = '2001')
#plt.plot(x02,y02, label = '2002')
#plt.plot(x03,y03, label = '2003')
#plt.plot(x04,y04, label = '2004')
#plt.plot(x05,y05, label = '2005')
#plt.plot(x06,y06, label = '2006')
#plt.plot(x07,y07, label = '2007')
#plt.plot(x08,y08, label = '2008')
#plt.plot(x09,y09, label = '2009')
#plt.legend(loc=2)
#plt.xlim(xmax=55)
#plt.ylabel('Number of ILI cases, ages 5-19')
#plt.xlabel('Week Number')
#plt.show()

#for row in E1f:
#	yr = row[2][:4]
#	if yr == "2000" or yr == "2010":
#		continue
#	if yr == '2001':
#		x01.append(row[3])
#		y01.append(row[4])
#	elif yr == '2002':
#		x02.append(row[3])
#		y02.append(row[4])
#	elif yr == '2003':
#		x03.append(row[3])
#		y03.append(row[4])
#	elif yr == '2004':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]=='53':
#		x04.append(row[3])
#		y04.append(row[4])
#	elif yr == '2005' and row[3]<'53':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]=='52':
#		x05.append(row[3])
#		y05.append(row[4])
#	elif yr == '2006' and row[3]<'52':
#		x06.append(row[3])
#		y06.append(row[4])
#	elif yr == '2007':
#		x07.append(row[3])
#		y07.append(row[4])
#	elif yr == '2008':
#		x08.append(row[3])
#		y08.append(row[4])
#	elif yr == '2009':
#		x09.append(row[3])
#		y09.append(row[4])
#plt.plot(x01,y01, label = '2001')
#plt.plot(x02,y02, label = '2002')
#plt.plot(x03,y03, label = '2003')
#plt.plot(x04,y04, label = '2004')
#plt.plot(x05,y05, label = '2005')
#plt.plot(x06,y06, label = '2006')
#plt.plot(x07,y07, label = '2007')
#plt.plot(x08,y08, label = '2008')
#plt.plot(x09,y09, label = '2009')
#plt.legend(loc=1)
#plt.xlim(xmax=55)
#plt.ylabel('Number of ILI cases, ages 50-69')
#plt.xlabel('Week Number')
#plt.show()

## E4 all years
#x = np.arange(0,496,1)
#for row in E4a:
#	y2yr.append(row[6])
#for row in E4b:
#	y2_4yr.append(row[6])
#for row in E4c:
#	y5_19yr.append(row[6])
#for row in E4d:
#	y20_29yr.append(row[6])
#for row in E4e:
#	y30_49yr.append(row[6])
#for row in E4f:
#	y50_69yr.append(row[6])
#for row in E4g:
#	y70yr.append(row[6])
#print len(y2yr), len(y2_4yr), len(y5_19yr), len(y20_29yr), len(y30_49yr), len(y50_69yr), len(y70yr)
#plt.plot(x,y2yr, label = '<2 years')
#plt.plot(x,y2_4yr, label = '2-4 years')
#plt.plot(x,y5_19yr, label = '5-19 years')
#plt.plot(x,y20_29yr, label = '20-29 years')
#plt.plot(x,y30_49yr, label = '30-49 years')
#plt.plot(x,y50_69yr, label = '50-69 years')
#plt.plot(x,y70yr, label = '70+ years')
#plt.legend(loc=2)
#plt.ylabel('Number of ILI cases per 100,000')
#plt.xlabel('Week Number 12-31-2000 to 6-27-2010')
#plt.show()

## E4 seasonal series
#G4season(E4a, y2yr)
#G4season(E4b, y2_4yr)
#G4season(E4c, y5_19yr)
#G4season(E4d, y20_29yr)
#G4season(E4e, y30_49yr)
#G4season(E4f, y50_69yr)
#G4season(E4g, y70yr)
#x=np.arange(1,len(y2yr)+1,1)
#plt.plot(x,y2yr, label = '<2 years')
#plt.plot(x,y2_4yr, label = '2-4 years')
#plt.plot(x,y5_19yr, label = '5-19 years')
#plt.plot(x,y20_29yr, label = '20-29 years')
#plt.plot(x,y30_49yr, label = '30-49 years')
#plt.plot(x,y50_69yr, label = '50-69 years')
#plt.plot(x,y70yr, label = '70+ years')
#plt.legend(loc=2)
#plt.xticks(x, wks_by_season, rotation = 90)
#plt.ylabel('Number of ILI cases per 100,000')
#plt.xlabel('Week Number ('+season+' flu season)')
#plt.xlim(xmax=55)
#plt.show()

#D4 all years
#x = np.arange(0,496,1)
#for row in D4a:
#	y2yr.append(row[6])
#for row in D4b:
#	y2_4yr.append(row[6])
#for row in D4c:
#	y5_19yr.append(row[6])
#for row in D4d:
#	y20_29yr.append(row[6])
#for row in D4e:
#	y30_49yr.append(row[6])
#for row in D4f:
#	y50_69yr.append(row[6])
#for row in D4g:
#	y70yr.append(row[6])
#print len(y2yr), len(y2_4yr), len(y5_19yr), len(y20_29yr), len(y30_49yr), len(y50_69yr), len(y70yr)
#plt.plot(x,y2yr, label = '<2 years')
#plt.plot(x,y2_4yr, label = '2-4 years')
#plt.plot(x,y5_19yr, label = '5-19 years')
#plt.plot(x,y20_29yr, label = '20-29 years')
#plt.plot(x,y30_49yr, label = '30-49 years')
#plt.plot(x,y50_69yr, label = '50-69 years')
#plt.plot(x,y70yr, label = '70+ years')
#plt.legend(loc=2)
#plt.ylabel('Number of ILI cases at the ER per 10,000')
#plt.xlabel('Week Number 12-31-2000 to 6-27-2010')
#plt.show() 

## D4 seasonal series
#G4season(D4a, y2yr)
#G4season(D4b, y2_4yr)
#G4season(D4c, y5_19yr)
#G4season(D4d, y20_29yr)
#G4season(D4e, y30_49yr)
#G4season(D4f, y50_69yr)
#G4season(D4g, y70yr)
#x=np.arange(1,len(y2yr)+1,1)
#plt.plot(x,y2yr, label = '<2 years')
#plt.plot(x,y2_4yr, label = '2-4 years')
#plt.plot(x,y5_19yr, label = '5-19 years')
#plt.plot(x,y20_29yr, label = '20-29 years')
#plt.plot(x,y30_49yr, label = '30-49 years')
#plt.plot(x,y50_69yr, label = '50-69 years')
#plt.plot(x,y70yr, label = '70+ years')
#plt.legend(loc=1)
#plt.xticks(x, wks_by_season, rotation = 90)
#plt.ylabel('Number of ILI cases at the ER per 10,000')
#plt.xlabel('Week Number ('+season+' flu season)')
#plt.xlim(xmax=55)
#plt.show()

## G4 all years
#x = np.arange(0,496,1)
#for row in G4a:
#	y2yr.append(row[6])
#for row in G4b:
#	y2_4yr.append(row[6])
#for row in G4c:
#	y5_19yr.append(row[6])
#for row in G4d:
#	y20_29yr.append(row[6])
#for row in G4e:
#	y30_49yr.append(row[6])
#for row in G4f:
#	y50_69yr.append(row[6])
#for row in G4g:
#	y70yr.append(row[6])
#plt.plot(x,y2yr, label = '<2 years')
#plt.plot(x,y2_4yr, label = '2-4 years')
#plt.plot(x,y5_19yr, label = '5-19 years')
#plt.plot(x,y20_29yr, label = '20-29 years')
#plt.plot(x,y30_49yr, label = '30-49 years')
#plt.plot(x,y50_69yr, label = '50-69 years')
#plt.plot(x,y70yr, label = '70+ years')
#plt.legend(loc=2)
#plt.ylabel('Number of ILI cases in acute care facilities per 10,000')
#plt.xlabel('Week Number 12-31-2000 to 6-27-2010')
#plt.show() 

## G4 seasonal series
#G4season(G4a, y2yr)
#G4season(G4b, y2_4yr)
#G4season(G4c, y5_19yr)
#G4season(G4d, y20_29yr)
#G4season(G4e, y30_49yr)
#G4season(G4f, y50_69yr)
#G4season(G4g, y70yr)
#x=np.arange(1,len(y2yr)+1,1)
#plt.plot(x,y2yr, label = '<2 years')
#plt.plot(x,y2_4yr, label = '2-4 years')
#plt.plot(x,y5_19yr, label = '5-19 years')
#plt.plot(x,y20_29yr, label = '20-29 years')
#plt.plot(x,y30_49yr, label = '30-49 years')
#plt.plot(x,y50_69yr, label = '50-69 years')
#plt.plot(x,y70yr, label = '70+ years')
#plt.legend(loc=2)
#plt.xticks(x, wks_by_season, rotation = 90)
#plt.ylabel('Number of ILI cases in acute care facilities per 10,000')
#plt.xlabel('Week Number ('+season+' flu season)')
#plt.xlim(xmax=55)
#plt.show()

### E4peak_season series
#season_grabaxes(D4a) #grabs only values for axes, chose a year with all weeks (already hardcoded in function)
#yrct=0
#x=np.arange(1,8,1) #there are seven age groups along the x axis
#seasontext = str(yr1vec[yrct]) +"-"+ str(yr2vec[yrct])
#peakweek(E4a, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[0:7], marker = 'o', label = seasontext, color='r')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_2, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_2, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_2, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_2, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_2, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_2, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_2, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[7:14], marker = 'o', label = seasontext, color='orange')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_3, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_3, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_3, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_3, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_3, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_3, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_3, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[14:21], marker = 'o', label = seasontext, color='y')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_4, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_4, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_4, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_4, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_4, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_4, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_4, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[21:28], marker = 'o', label = seasontext, color='g')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_5, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_5, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_5, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_5, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_5, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_5, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_5, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[28:35], marker = 'o', label = seasontext, color='b')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_6, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_6, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_6, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_6, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_6, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_6, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_6, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[35:42], marker = 'o', label = seasontext, color='violet')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_7, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_7, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_7, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_7, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_7, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_7, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_7, s_peak, s_wk, s_numshift, s_num, yrct)
#scatter(x, peakwk_shifted[42:49], marker = 'o', label = seasontext, color='black')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()
#yrct +=1
#seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])
#peakweek(E4a_8, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4b_8, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4c_8, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4d_8, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4e_8, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4f_8, s_peak, s_wk, s_numshift, s_num, yrct)
#peakweek(E4g_8, s_peak, s_wk, s_numshift, s_num, yrct)
#print peakwk_shifted
#scatter(x, peakwk_shifted[49:56], marker = 'o', label = seasontext, color='cyan')
#plt.ylabel('Week Number in the Year')
#plt.xlabel('Age Group')
#plt.yticks(yax, wks_by_season) 
#plt.xticks(x, agelabel)
#plt.legend(loc=2)
#plt.show()

## G4peak_season series
season_grabaxes(D4a) #grabs only values for axes, chose a year with all weeks (already hardcoded in function)
yrct=0
x=np.arange(1,8,1) #there are seven age groups along the x axis
seasontext = str(yr1vec[yrct]) +"-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[0:7], marker = 'o', label = seasontext, color='r')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_2, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_2, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_2, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_2, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_2, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_2, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_2, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[7:14], marker = 'o', label = seasontext, color='orange')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_3, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_3, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_3, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_3, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_3, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_3, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_3, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[14:21], marker = 'o', label = seasontext, color='y')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_4, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_4, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_4, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_4, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_4, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_4, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_4, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[21:28], marker = 'o', label = seasontext, color='g')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_5, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_5, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_5, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_5, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_5, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_5, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_5, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[28:35], marker = 'o', label = seasontext, color='b')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_6, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_6, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_6, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_6, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_6, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_6, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_6, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[35:42], marker = 'o', label = seasontext, color='violet')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_7, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_7, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_7, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_7, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_7, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_7, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_7, s_peak, s_wk, s_numshift, s_num, yrct)
scatter(x, peakwk_shifted[42:49], marker = 'o', label = seasontext, color='black')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()
yrct +=1
seasontext = str(yr1vec[yrct])+ "-"+ str(yr2vec[yrct])+" acute peak"
peakweek(G4a_8, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4b_8, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4c_8, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4d_8, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4e_8, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4f_8, s_peak, s_wk, s_numshift, s_num, yrct)
peakweek(G4g_8, s_peak, s_wk, s_numshift, s_num, yrct)
print peakwk_shifted
scatter(x, peakwk_shifted[49:56], marker = 'o', label = seasontext, color='cyan')
plt.ylabel('Week Number in the Year')
plt.xlabel('Age Group')
plt.yticks(yax, wks_by_season) 
plt.xticks(x, agelabel)
plt.legend(loc=2)
plt.show()

#duration of peak above --baseline x percent of peak? (subgraph of D4 series)

 
#hypotheses: low crossover reaction between virus and vaccine changes magnitude of influenza but perhaps not the peak
#potential inverse relationship between duration and magnitude


