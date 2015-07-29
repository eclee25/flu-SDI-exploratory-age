
## Name: Elizabeth Lee
## Date: 11/2/14
## Function: draw figure 1 for manuscript
### 10-year time series panels: SDI ILI % of total visits (outpatient only) & ILINet ILI % of total visits, positive lab test percentages, cumulative season hospital rate for children, cumulative season hospital rate for adults, pediatric deaths, P&I mortality (October 2001 through May 2009)
## Filenames: SQL_export/F1.csv, CDC_Source/Import_Data/all_cdc_source_data.csv
## Data Source: 'season', 'wk', 'yr', 'wknum', 'ILI', 'anydiag', 'pop'
## Notes: F1.csv: 'season', 'wk', 'yr', 'wknum', 'outpatient & office ILI', 'outpatient & office anydiag', 'pop'
## 11/2/14 Note: createF1.csv includes data from all service places while F1.csv includes only outpatient data\
## 7/27/15: add benchmark bars to panel e, extend from 1997-2014 (excl. 2009-10), change fig labels
## 7/29/15: formatting updates based on SB comments
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

require(dplyr)
require(tidyr)
# 12/4/14
setwd('/home/elee/R/source_functions')
source("dfsumm.R")
##########################################
# Data import
# SDI
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export')
sdi <- read.csv('F1.csv', colClasses = 'character', header = F)
names(sdi) <- c('season', 'wk', 'yr', 'wknum', 'ILI', 'anydiag', 'pop')
sdi$wk <- as.Date(sdi$wk)
sdi$ILI <- as.numeric(sdi$ILI)
sdi$anydiag <- as.numeric(sdi$anydiag)
sdi$pop <- as.numeric(sdi$pop)
sdi$wknum <- as.numeric(sdi$wknum)
sdi1wknum <- sdi[sdi$wknum < 10,]
sdi1wknum$wknum <- paste0('0', sdi1wknum$wknum)
sdi2wknum <- sdi[sdi$wknum > 9,]
sdi3 <- rbind(sdi1wknum, sdi2wknum)
sdi3$uqid <- paste0(sdi3$yr, sdi3$wknum)
# 7/27/15: rm subset
# # 11/2/14 subset S2 through S9 data
# sdi2 <- sdi3[(sdi3$uqid >= 200140 & sdi3$uqid <= 200920),]
sdi2 <- sdi3
# reorder sdi2 by uqid
sdi2 <- sdi2[order(sdi2$uqid, decreasing = FALSE),]

# CDC
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
cdc <- read.csv('all_cdc_source_data.csv', colClasses = 'character', header = T)
cdc$uqid <- as.character(cdc$uqid)
# 7/27/15L rm subset
# # 11/2/14 subset S2 through S9 data
# cdc_lm <- cdc[(cdc$uqid >= '200140' & cdc$uqid <= '200920'),]
cdc_lm <- cdc
cdc_lm$perc_pos <- as.numeric(cdc_lm$perc_pos)
cdc_lm$a_H1 <- as.numeric(cdc_lm$a_H1)
cdc_lm$a_H3sum <- as.numeric(cdc_lm$a_H3) + as.numeric(cdc_lm$a_H3N2)
cdc_lm$a_2009H1N1 <- as.numeric(cdc_lm$a_2009H1N1)
cdc_lm$b <- as.numeric(cdc_lm$b)
cdc_lm$hosp_18.49 <- as.numeric(cdc_lm$hosp_18.49)
cdc_lm$hosp_5.17 <- as.numeric(cdc_lm$hosp_5.17)
cdc_lm$hosp_tot <- as.numeric(cdc_lm$hosp_tot)
cdc_lm$season <- as.numeric(cdc_lm$season)
cdc_lm$pi_only <- as.numeric(cdc_lm$pi_only)
cdc_lm$ped_deaths <- as.numeric(cdc_lm$ped_deaths)
cdc_lm$perc_unwt_ili <- as.numeric(cdc_lm$perc_unwt_ili)

# check uqids across cdc_lm and sdi2
cdc_lm$uqid %in% sdi2$uqid
cdc_lm[c(327, 588),] # not in sdi2: 200353, 200853
sdi2$uqid %in% cdc_lm$uqid
sdi2[c(1, 314),] # not in cdc_lm: 200053, 200653


##########################################
# SDI % ILI of all visits
sdi2$ILI_diag_perc <- sdi2$ILI/sdi2$anydiag * 100

##########################################
# process hosp rates so that they are not cumulative
# 12/4/14: Matt says that the non-cumulative data are not accurate because hospitalizations are backfilled on the week of reporting, not on the week of the event # the plots will be changed to a cumulative hospitalization rate version
cdc_lm$hosp_tot_diff <- NA
cdc_lm$hosp_5.17_diff <- NA
cdc_lm$hosp_18.49_diff <- NA
for (s in -2:14){
  dat <- cdc_lm[cdc_lm$season == s,]
  cdc_lm$hosp_tot_diff[cdc_lm$season == s] <- c(dat$hosp_tot[1], diff(dat$hosp_tot, lag = 1))
  cdc_lm$hosp_5.17_diff[cdc_lm$season == s] <- c(dat$hosp_5.17[1], diff(dat$hosp_5.17, lag = 1))
  cdc_lm$hosp_18.49_diff[cdc_lm$season == s] <- c(dat$hosp_18.49[1], diff(dat$hosp_18.49, lag = 1))
}

##########################################
# 2/11/15: process pediatric deaths so that they are cumulative
cdc_lm$ped_deaths_cum <- NA
for (s in -2:14){
  dat <- cdc_lm[cdc_lm$season == s,]
  # put NA for first week in every season so that the cumulative deaths will not be connected across seasons (there are no ped deaths in those weeks anyways)
  cdc_lm$ped_deaths_cum[cdc_lm$season == s] <- c(NA, cumsum(dat$ped_deaths[2:length(dat$ped_deaths)]))
}

##########################################
# 7/27/15 benchmark barplot
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
benchmark <- read.csv('benchmark_ixTavg_altnorm_comparisons.csv', header=T)

##########################################
# 7/27/15 merge cdc_lm and sdi2 data 
sdi_drop <- tbl_df(sdi2) %>% select(uqid, ILI_diag_perc)
cdc_drop <- tbl_df(cdc_lm) %>% select(uqid, yr, wk, season, perc_unwt_ili, a_H1, a_H3, b, perc_pos, ped_deaths_cum, hosp_5.17, hosp_18.49, pi_only)
merge1 <- left_join(cdc_drop, sdi_drop, by = "uqid") 
merge2 <- merge1 %>% filter(uqid < "200940" | uqid >= "201040")
# cdc data has week 200353, but sdi data does not; interpolate with mean
merge2[which(merge2$uqid=='200353'),]$ILI_diag_perc <- mean(merge2[which(merge2$uqid=='200352'):which(merge2$uqid=='200401'),]$ILI_diag_perc, na.rm=T)

##########################################
# plotting parameters
w = 580 
h = 700
ps = 14
margin = c(0.5, 4, 1, 4) # bottom, left, top, right
omargin = c(3.5, 0, 0, 0)
sz = 2
sz2 = 1.2
sz3 = 2.5
un = "px"
wkticks <- which(substring(merge2$uqid, 5, 6)=='40')
# wklabs <- paste(c(rep('Oct', length(wkticks)-1), 'May'), substr(merge2$yr[wkticks], 3, 4), sep=' ')
seasonlabs <- c('97-98', '98-99', '99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '10-11', '11-12', '12-13', '13-14')
# benchmark bar colors
sev <- which(benchmark$b0_classifq==1)
mod <- which(benchmark$b0_classifq==0)
colorvec <- rep('blue',16)
colorvec[sev] <- 'red'
colorvec[mod] <- 'yellow'
pandemiccol <- 'dark grey'
dividercol <- 'black'

##########################################
# combined figure
setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/MainFigures/F1')

png(filename="all_panels.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mfrow = c(5, 1), mar = margin, oma = omargin)

# ILI panel
plot(merge2$ILI_diag_perc, type = 'l', xlab = '', ylab = '', ylim = c(0, 9), col = 'tomato', axes = F, lwd = sz, cex.lab = sz)
segments(which(merge2$uqid=='201040'), 0, y1 = 2000, lwd = sz2, col = pandemiccol)
abline(h = 0, lwd = sz2, col = dividercol)
axis(2, at = seq(0, 9, by=2), labels=seq(0, 9, by=2))
mtext(2, text = 'percent', line = sz3, cex = sz2)
lines(merge2$perc_unwt_ili, type = 'l', col = 'turquoise3', lwd = sz)
legend('topleft', c('medical claims', 'ILINet'), lwd = sz, col = c('tomato', 'turquoise3'), , title = 'ILI (%) of all visits')

# perc_pos panel
par(mar=margin)
plot(merge2$a_H1, col = 'navy', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0, 1600))
lines(merge2$a_H3sum, col = 'violetred3', type = 'l', lwd = sz2)
lines(merge2$b, col = 'orange', type = 'l', lwd = sz2)
segments(which(merge2$uqid=='201040'), 0, y1 = 2000, lwd = sz2, col = pandemiccol)
abline(h = 0, lwd = sz2, col = dividercol)
axis(2, at = seq(0, 1600, by=800), labels = seq(0, 1600, by=800), col.axis = 'black', col = 'black')
mtext(2, text = 'samples', line = sz3, cex = sz2, col = 'black')
par(new=T)
plot(merge2$perc_pos, type = 'l', xlab = '', ylab = '', ylim = c(0, 60), col = 'black', axes = F, lwd = sz, cex.lab = sz)
axis(4, at=seq(0, 60, by=30), labels=seq(0, 60, by=30))
mtext(4, text = 'percent', line = sz3, cex = sz2)
legend('topleft', c('A/H1 samples', 'A/H3 ...', 'B ...', 'positive tests (%)'), col = c('navy', 'violetred3', 'orange', 'black'), lwd = c(sz2, sz2, sz2, sz))

# laboratory confirmed panel (cumulative hospitalization rates, pediatric deaths)
par(mar=margin)
plot(merge2$ped_deaths_cum, col = 'forestgreen ', type = 'l', lwd = sz, axes = F, ylab = '', xlab = '', ylim = c(0, 200))
segments(which(merge2$uqid=='201040'), 0, y1 = 2000, lwd = sz2, col = pandemiccol)
abline(h = 0, lwd = sz2, col = dividercol)
axis(4, at = seq(0, 200, by=100), labels = seq(0, 200, by=100), col.axis = 'black', col = 'black', col.ticks = 'black')
mtext(4, text = 'deaths', line = sz3, col = 'black', cex = sz2)
par(new=T)
plot(merge2$hosp_5.17, type = 'l', xlab = '', ylab = '', axes = F, lwd = sz,  cex.lab = sz, col = 'red', ylim = c(0, 22))
lines(merge2$hosp_18.49, type = 'l', col = 'blue', lwd = sz)
axis(2, at=seq(0, 22, by=10), labels=seq(0, 22, by=10))
mtext(2, text = 'rate', line = sz3, cex = sz2)
legend('topleft', c('5-17 yr hosp. rate', '18-49 yr hosp. rate', 'pediatric deaths'), col = c('red', 'blue', 'forestgreen'), lwd = c(sz, sz, sz, sz), title = 'Cumulative lab-confirmed:')

# death panel
par(mar=margin) 
plot(merge2$pi_only, type = 'l', xlab = '', ylab = '', axes = F, lwd = 2, ylim = c(300, 1600), cex.lab = sz)
segments(which(merge2$uqid=='201040'), 300, y1 = 2000, lwd = sz2, col = pandemiccol)
abline(h = 300, lwd = sz2, col = dividercol)
axis(2, at = seq(300, 1600, by = 650), labels = seq(300, 1600, by = 650))
mtext(2, text = 'P&I deaths', line = sz3, cex = sz2)
# legend('topleft', 'P&I-associated', col = 'black', lwd = sz)

# benchmark panel
par(mar=margin)
mp <- barplot(benchmark$beta_norm0, xlab = '', ylab = '', axes = F, col = colorvec, cex.lab = sz, width=diff(wkticks), ylim = c(-1.5, 1.5))
segments((mp[13]+mp[12])/2, -3, y1 = 2000, lwd = sz2, col = pandemiccol) # force line bw 2008-09 and 2010-11 seasons
abline(h = 0, lwd = sz2, col = dividercol)
axis(2, at = seq(-1, 1, by = 1), labels = seq(-1, 1, by = 1))
mtext(2, text = "benchmark", line = sz3, cex = sz2)
legend('topleft', c('Mild', 'Moderate', 'Severe'), col = c('blue', 'yellow', 'red'), lwd = c(sz, sz, sz))

# x-axis
axis(1, at = mp, labels = seasonlabs, las = 2, cex.axis = sz2)
dev.off()

