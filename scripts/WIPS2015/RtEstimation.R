
## Name: Elizabeth Lee
## Date: 2/3/15
## Function: Try EpiEstim package for R(t) estimation. Look at holiday periods
## Filenames: 
## Data Source: incidentCases_RtEstimation_dataExport.py; explore/Py_export/EpiEstim_totalILI_allLocs_S%s.csv
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

setwd('/home/elee/R/source_functions')
source("dfsumm.R")

require(EpiEstim)

#####################
## Leave these parameters fixed ##
### Serial Interval Data (mean, sd) ###
# Cowling et al 2011: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3057478/
Cowling2011 <-c(3.6, 1.6) # this is in days -- I think the data needs to be converted to days too

### Plotting Parameters ###
seasons <- 2:9
labels <- c('2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09')
Thx <- c('2001-11-22', '2002-11-28', '2003-11-27', '2004-11-25', '2005-11-24', '2006-11-23', '2007-11-22', '2008-11-27', '2009-11-26')
######################################
## Set these parameters every time ##
index <-5
mean.std.si <- Cowling2011
start.index <- 1:50
end.index <- 3:52
######################################
## Leave these relationships fixed ##
seas <-seasons[index]
seasonlab <- labels[index]
Thx.date <- TLhx[index]

#####################
## Import Data ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
data <- read.csv(sprintf('EpiEstim_totalILI_allLocs_787_S%s.csv', seas), header=FALSE, colClasses='character')
names(data) <- c('season', 'week', 'cases')
incident.cases <- as.numeric(data$cases)

# Cori et al. 2013 R(t) estimation method
Cori.output <- EstimateR(incident.cases, T.Start=start.index, T.End=end.index, method="ParametricSI", Mean.SI=mean.std.si[1], Std.SI=mean.std.si[2], Mean.Prior=5, Std.Prior=5, CV.Posterior=0.3, plot=TRUE, leg.pos="topright")

# # Wallinga & Teunis R(t) estimation method
# WT.output <- WT(incident.cases, T.Start=start.index, T.End=end.index, method="ParametricSI", Mean.SI=mean.std.si[1], Std.SI=mean.std.si[2], nSim=10, plot=TRUE, leg.pos="topright")

#####################
# plotting parameters
w = 580 
h = 580
ps = 14
margin = c(6,4,4,4) + 0.1 # bottom, left, top, right
omargin = c(0.5, 0.5, 0.5, 0.5)
lab_sz = 1.5
axis_sz = 1.5
main_sz = 1.5
linewidth = 3
un = "px"
Thx.poly <- c(which(data$week==Thx.date), which(data$week==Thx.date), which(data$week==Thx.date)+1, which(data$week==Thx.date)+1) # x-axis polygon coords for Thx holiday
Xmas.poly <- c(12, 12, 14, 14) # x-axis polygon coords for Xmas holiday
incid.poly <-  c(0,500,500,0) # y-axis polygon coords for incidence curve
Rt.poly <- c(0,5,5,0) # y-axis polygon coords for estimated R plot
holiday.col <- adjustcolor('gray', alpha.f=0.5) # holiday fill colors

################################
## assign variable names
weeklabels <- substr(data$week[seq(1, 52, 10)], 6, 10)
meanRt <- Cori.output$R[,3]
meanRt.upper <- Cori.output$R[,11]
meanRt.lower <- Cori.output$R[,5]
################################
## plots ##

par(mfrow=c(1,1), mar=margin, oma=omargin)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Anne/EpiEstim/figures')
png(filename=sprintf('incidentCases_S%s.png', seasonlab), units=un, width=w, height=h, pointsize=ps, bg = 'white')
plot(incident.cases, main=sprintf('Austin, TX - %s', seasonlab), xaxt='n', type='l', xlab='', ylab='new cases', cex.lab=lab_sz, cex.main=main_sz, cex.axis=axis_sz, lwd=linewidth)
polygon(Thx.poly, incid.poly, col=holiday.col) # Thx dates
polygon(Xmas.poly, incid.poly, col=holiday.col) # Xmas dates
axis(1, at=seq(1, 52, 10), labels=weeklabels, las=2, cex.axis=axis_sz)
dev.off()

par(mfrow=c(1,1), mar=margin, oma=omargin)
png(filename=sprintf('estimatedR_S%s.png', seasonlab), units=un, width=w, height=h, pointsize=ps, bg = 'white')
plot(meanRt, main=sprintf('%s', seasonlab), xaxt='n', type='l', xlab='', ylab='estimated R effective', lwd=linewidth, ylim=c(0,4), cex.lab=lab_sz, cex.axis=axis_sz, cex.main=main_sz)
lines(meanRt.upper, col='red', lwd=linewidth)
lines(meanRt.lower, col='red', lwd=linewidth)
polygon(Thx.poly, Rt.poly, col=holiday.col) # Thx dates
polygon(Xmas.poly, Rt.poly, col=holiday.col) # Xmas dates
axis(1, at=seq(1, 52, 10), labels=weeklabels, las=2, cex.axis=axis_sz)
dev.off()


### two-paneled figure with incidence and R effective over time ###
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Anne/EpiEstim/figures') # reset this to the working directory where figures should be saved
png(filename=sprintf('incidentCases_estimatedR_S%s.png', seasonlab), units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mfrow=c(2,1), mar=c(0.5,4,1.5,0.5), oma=c(4,1,0,1))

plot(incident.cases, main='incidence', xaxt='n', type='l', xlab='', ylab='new cases', cex.lab=lab_sz, cex.main=main_sz, cex.axis=axis_sz, lwd=linewidth)
polygon(Thx.poly, incid.poly, col=holiday.col) # Thx dates
polygon(Xmas.poly, incid.poly, col=holiday.col) # Xmas dates

plot(meanRt, main='time-varying transmission', xaxt='n', type='l', xlab='', ylab='estimated R effective', lwd=linewidth, ylim=c(0,4), cex.lab=lab_sz, cex.axis=axis_sz, cex.main=main_sz)
lines(meanRt.upper, col='red', lwd=linewidth)
lines(meanRt.lower, col='red', lwd=linewidth)
polygon(Thx.poly, Rt.poly, col=holiday.col) # Thx dates
polygon(Xmas.poly, Rt.poly, col=holiday.col) # Xmas dates
axis(1, at=seq(1, 52, 10), labels=weeklabels, las=2, cex.axis=axis_sz)
dev.off()

