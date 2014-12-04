
## Name: Elizabeth Lee
## Date: 11/2/14
## Function: draw figure 1 for manuscript
### 10-year time series panels: SDI ILI % of total visits (outpatient only) & ILINet ILI % of total visits, positive lab test percentages, cumulative season hospital rate for children, cumulative season hospital rate for adults, pediatric deaths, P&I mortality (October 2001 through May 2009)
## Filenames: SQL_export/F1.csv, CDC_Source/Import_Data/all_cdc_source_data.csv
## Data Source: 'season', 'wk', 'yr', 'wknum', 'ILI', 'anydiag', 'pop'
## Notes: F1.csv: 'season', 'wk', 'yr', 'wknum', 'outpatient & office ILI', 'outpatient & office anydiag', 'pop'
## 11/2/14 Note: createF1.csv includes data from all service places while F1.csv includes only outpatient data
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

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
# 11/2/14 subset S2 through S9 data
sdi2 <- sdi3[(sdi3$uqid >= 200140 & sdi3$uqid <= 200920),]
# reorder sdi2 by uqid
sdi2 <- sdi2[order(sdi2$uqid, decreasing = FALSE),]
# CDC
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
cdc <- read.csv('all_cdc_source_data.csv', colClasses = 'character', header = T)
cdc$uqid <- as.character(cdc$uqid)
# 11/2/14 subset S2 through S9 data
cdc_lm <- cdc[(cdc$uqid >= '200140' & cdc$uqid <= '200920'),]
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
cdc_lm[c(118, 379),] # not in sdi2: 200353, 200853
sdi2$uqid %in% cdc_lm$uqid
sdi2[274,] # not in cdc_lm: 200053, 200653


##########################################
# SDI % ILI of all visits
sdi2$ILI_diag_perc <- sdi2$ILI/sdi2$anydiag * 100

##########################################
# process hosp rates so that they are not cumulative
# 12/4/14: Matt says that the non-cumulative data are not accurate because hospitalizations are backfilled on the week of reporting, not on the week of the event # the plots will be changed to a cumulative hospitalization rate version
cdc_lm$hosp_tot_diff <- NA
cdc_lm$hosp_5.17_diff <- NA
cdc_lm$hosp_18.49_diff <- NA
for (s in 2:9){
  dat <- cdc_lm[cdc_lm$season == s,]
  cdc_lm$hosp_tot_diff[cdc_lm$season == s] <- c(dat$hosp_tot[1], diff(dat$hosp_tot, lag = 1))
  cdc_lm$hosp_5.17_diff[cdc_lm$season == s] <- c(dat$hosp_5.17[1], diff(dat$hosp_5.17, lag = 1))
  cdc_lm$hosp_18.49_diff[cdc_lm$season == s] <- c(dat$hosp_18.49[1], diff(dat$hosp_18.49, lag = 1))
}

##########################################
# plotting parameters
w = 580 
h = 580
ps = 14
margin = c(1, 4, 1, 4) + 0.1 # bottom, left, top, right
lastmargin = c(4, 4, 0, 4)
omargin = c(1, 1, 1, 1)
sz = 2
sz2 = 1.2
un = "px"
wkticks = c(seq(1, dim(sdi2)[1], by = 52), dim(sdi2)[1])
wklabs = paste(c(rep('Oct', length(wkticks)-1), 'May'), substr(sdi2$wk[wkticks], 3, 4), sep=' ')

##########################################
# combined figure
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5/F1')

png(filename="all_panels.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mfrow = c(4, 1), mar = margin)

# ILI panel
plot(sdi2$ILI_diag_perc, type = 'l', xlab = '', ylab = '', ylim = c(0, 7.5), col = 'tomato', axes = F, lwd = sz, cex.lab = sz)
axis(2, at = seq(0, 7, by=1), labels=seq(0, 7, by=1))
mtext(2, text = 'ILI / outpat. (%)', line = 2, cex = sz2)
lines(cdc_lm$perc_unwt_ili, type = 'l', col = 'turquoise3', lwd = sz)
legend('topleft', c('ILINet data', 'medical claims data'), lwd = sz, col = c('turquoise3', 'tomato'))

# perc_pos panel
par(mar=margin)
plot(cdc_lm$a_H1, col = 'navy', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0, 1600))
lines(cdc_lm$a_H3sum, col = 'violetred3', type = 'l', lwd = sz2)
lines(cdc_lm$b, col = 'orange', type = 'l', lwd = sz2)
axis(2, at = seq(0, 1600, by=500), labels = seq(0, 1600, by=500), col.axis = 'black', col = 'black')
mtext(2, text = 'samples (#)', line = 2.5, cex = sz2, col = 'black')
par(new=T)
plot(cdc_lm$perc_pos, type = 'l', xlab = '', ylab = '', ylim = c(0, 35), col = 'black', axes = F, lwd = sz, cex.lab = sz)
axis(4, at=seq(0, 35, by=15), labels=seq(0, 35, by=15))
mtext(4, text = 'positive tests (%)', line = 2, cex = sz2)
legend('topleft', c('A/H1 samp.', 'A/H3 samp.', 'B samp.', '% pos tests'), col = c('navy', 'violetred3', 'orange', 'black'), lwd = c(sz2, sz2, sz2, sz))

# laboratory confirmed panel (cumulative hospitalization rates, pediatric deaths)
par(mar=margin)
plot(cdc_lm$ped_deaths, col = 'forestgreen ', type = 'l', lwd = sz, axes = F, ylab = '', xlab = '', ylim = c(0,15))
axis(4, at = seq(0, 15, by=5), labels = seq(0, 15, by=5), col.axis = 'black', col = 'black', col.ticks = 'black')
mtext(4, text = 'deaths (#)', line = 2.5, col = 'black', cex = sz2)
par(new=T)
plot(cdc_lm$hosp_5.17, type = 'l', xlab = '', ylab = '', axes = F, lwd = sz, ylim = c(0, 15), cex.lab = sz, col = 'red')
lines(cdc_lm$hosp_18.49, type = 'l', col = 'blue', lwd = sz)
axis(2, at=seq(0, 15, by=5), labels=seq(0, 15, by=5))
mtext(2, text = 'cum. hosp. rate', line = sz, cex = sz2)
legend('topleft', c('5-17 yr hosp.', '18-49 yr hosp.', 'pediatric deaths'), col = c('red', 'blue', 'forestgreen'), lwd = c(sz, sz, sz))

# death panel
par(mar=lastmargin) 
plot(cdc_lm$pi_only, type = 'l', xlab = '', ylab = '', axes = F, lwd = 2, ylim = c(400, 1400), cex.lab = sz)
axis(2, at = seq(400, 1400, by = 500), labels = seq(400, 1400, by = 500))
mtext(2, text = 'P&I deaths (#)', line = 2, cex = sz2)
axis(1, at = wkticks, labels = wklabs, las = 2, cex = sz)
dev.off()
