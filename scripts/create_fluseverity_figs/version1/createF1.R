
## Name: Elizabeth Lee
## Date: 2/13/14
## Function: draw figure 1 for manuscript
### 10-year time series panels: SDI ILI % of total visits ILINet ILI % of total visits, positive lab test percentages, hospital rate for children, hospital rate for adults, pediatric deaths, P&I mortality
## Filenames: SQL_export/create_F1.csv, CDC_Source/Import_Data/all_cdc_source_data.csv
## Data Source: 
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")


dfsumm<-function(x) {
	if(!class(x)[1]%in%c("data.frame","matrix"))
		stop("You can't use dfsumm on ",class(x)," objects!")
	cat("\n",nrow(x),"rows and",ncol(x),"columns")
	cat("\n",nrow(unique(x)),"unique rows\n")
	s<-matrix(NA,nrow=6,ncol=ncol(x))
	for(i in 1:ncol(x)) {
		iclass<-class(x[,i])[1]
		s[1,i]<-paste(class(x[,i]),collapse=" ")
		y<-x[,i]
		yc<-na.omit(y)
		if(iclass%in%c("factor","ordered"))
			s[2:3,i]<-levels(yc)[c(1,length(levels(yc)))] else
		if(iclass=="numeric")
			s[2:3,i]<-as.character(signif(c(min(yc),max(yc)),3)) else
		if(iclass=="logical")
			s[2:3,i]<-as.logical(c(min(yc),max(yc))) else
			s[2:3,i]<-as.character(c(min(yc),max(yc)))
			s[4,i]<-length(unique(yc))
			s[5,i]<-sum(is.na(y))
			s[6,i]<-!is.unsorted(yc)
	}
	s<-as.data.frame(s)
	rownames(s)<-c("Class","Minimum","Maximum","Unique (excld. NA)","Missing values","Sorted")
	colnames(s)<-colnames(x)
	print(s)
} 

##########################################
# Data import
# SDI
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export')
sdi <- read.csv('createF1.csv', colClasses = 'character', header = F)
names(sdi) <- c('season', 'wk', 'yr', 'wknum', 'ILI', 'anydiag', 'pop')
sdi$wk <- as.Date(sdi$wk)
sdi$ILI <- as.numeric(sdi$ILI)
sdi$anydiag <- as.numeric(sdi$anydiag)
sdi$pop <- as.numeric(sdi$pop)
sdi$wknum <- as.numeric(sdi$wknum)
sdi1wknum <- sdi[sdi$wknum < 10,]
sdi1wknum$wknum <- paste0('0', sdi1wknum$wknum)
sdi2wknum <- sdi[sdi$wknum > 9,]
sdi2 <- rbind(sdi1wknum, sdi2wknum)
sdi2$uqid <- paste0(sdi2$yr, sdi2$wknum)
# reorder sdi2 by uqid
sdi2 <- sdi2[order(sdi2$uqid, decreasing = FALSE),]
# CDC
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
cdc <- read.csv('all_cdc_source_data.csv', colClasses = 'character', header = T)
cdc$uqid <- as.numeric(cdc$uqid)
cdc_lm <- cdc[(cdc$uqid > '200052' & cdc$uqid < '201027'),]
cdc_lm$perc_pos <- as.numeric(cdc_lm$perc_pos)
cdc_lm$a_H1 <- as.numeric(cdc_lm$a_H1)
cdc_lm$a_H3sum <- as.numeric(cdc_lm$a_H3) + as.numeric(cdc_lm$a_H3N2)
cdc_lm$a_2009H1N1 <- as.numeric(cdc_lm$a_2009H1N1)
cdc_lb$b <- as.numeric(cdc_lm$b)
cdc_lm$hosp_18.49 <- as.numeric(cdc_lm$hosp_18.49)
cdc_lm$hosp_5.17 <- as.numeric(cdc_lm$hosp_5.17)
cdc_lm$hosp_tot <- as.numeric(cdc_lm$hosp_tot)
cdc_lm$season <- as.numeric(cdc_lm$season)
cdc_lm$pi_only <- as.numeric(cdc_lm$pi_only)
cdc_lm$ped_deaths <- as.numeric(cdc_lm$ped_deaths)

# check uqids across cdc_lm and sdi2
cdc_lm$uqid %in% sdi2$uqid
cdc_lm[c(157, 418),] # not in sdi2: 200353, 200853
sdi2$uqid %in% cdc_lm$uqid
sdi2[c(91, 350),] # not in cdc_lm: 200053, 200653


##########################################
# SDI % ILI of all visits
sdi2$ILI_diag_perc <- sdi2$ILI/sdi2$anydiag * 100

##########################################
# process hosp rates so that they are not cumulative
cdc_lm$hosp_tot_diff <- NA
cdc_lm$hosp_5.17_diff <- NA
cdc_lm$hosp_18.49_diff <- NA
for (s in 1:10){
  dat <- cdc_lm[cdc_lm$season == s,]
  cdc_lm$hosp_tot_diff[cdc_lm$season == s] <- c(dat$hosp_tot[1], diff(dat$hosp_tot, lag = 1))
  cdc_lm$hosp_5.17_diff[cdc_lm$season == s] <- c(dat$hosp_5.17[1], diff(dat$hosp_5.17, lag = 1))
  cdc_lm$hosp_18.49_diff[cdc_lm$season == s] <- c(dat$hosp_18.49[1], diff(dat$hosp_18.49, lag = 1))
}
# season 9's data picks up again towards the end of the season because of the pandemic, so the start of that sequence needs to be added to the differenced values
cdc_lm$hosp_tot_diff[453] <- cdc_lm$hosp_tot[453]
cdc_lm$hosp_5.17_diff[453] <- cdc_lm$hosp_5.17[453]
cdc_lm$hosp_18.49_diff[453] <- cdc_lm$hosp_18.49[453]


##########################################
# plotting parameters
w = 580 
h = 580
ps = 14
margin = c(1, 4, 1, 4) + 0.1 # bottom, left, top, right
omargin = c(1, 1, 1, 1)
sz = 2
sz2 = 1.2
un = "px"
wklabs = c('12/2000', '1/2002', '1/2003', '1/2004', '1/2005', '1/2006', '2/2007', '2/2008', '2/2009', '2/2010') # sdi2$wk[seq(1, 496, by = 53)]


##########################################
# combined figure
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F1')

png(filename="all_panels.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mfrow = c(4, 1), mar = margin)

# ILI panel
plot(sdi2$ILI_diag_perc, type = 'l', xlab = '', ylab = '', ylim = c(0, 5), col = 'blue', axes = F, lwd = 2, cex.lab = sz)
axis(2, at = seq(0, 5, by=1), labels=seq(0, 5, by=1))
mtext(2, text = 'ILI % of all visits', line = 2, cex = sz2)
lines(cdc_lm$perc_unwt_ili, type = 'l', col = 'black', lwd = 2)
legend('topleft', c('ILINet', 'insurance claims'), lwd = 2, col = c('black', 'blue'))

# perc_pos panel
par(mar=margin)
plot(cdc_lm$perc_pos, type = 'l', xlab = '', ylab = '', col = 'black', axes = F, lwd = 2, cex.lab = sz)
axis(2, at = seq(0, 40, by=10), labels=seq(0, 40, by=10))
mtext(2, text = '% pos. lab tests', line = 2, cex = sz2)
par(new=T)
plot(cdc_lm$a_H1, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0, 1600))
lines(cdc_lm$a_H3sum, col = 'red', type = 'l')
lines(cdc_lm$b, col = 'orange', type = 'l')
lines(cdc_lm$a_2009H1N1, col = 'green', type = 'l')
axis(4, at = seq(0, 1600, by=250), labels = seq(0, 1600, by=250))
mtext(4, text = 'pos. lab samples', line = 2.5, cex = sz2)
legend('topleft', c('% pos tests', 'A/H1 samples', 'A/H3', 'B', '2009 H1N1'), col = c('black', 'blue', 'red', 'orange', 'green'), lwd = c(2, 1, 1, 1, 1))

# hosp panel
par(mar=margin)
plot(cdc_lm$hosp_tot_diff, type = 'l', xlab = '', ylab = '', axes = F, lwd = 2, ylim = c(0, 4), cex.lab = sz)
axis(2, at = seq(0, 4, by=1), labels=seq(0, 4, by=1))
mtext(2, text = 'hosp. per 100,000', line = 2, cex = sz2)
lines(cdc_lm$hosp_5.17_diff, type = 'l', col = 'red', lwd = 2)
lines(cdc_lm$hosp_18.49_diff, type = 'l', col = 'blue', lwd = 2)
legend('topleft', c('Total Pop', '5-17 Years', '18-49 Years'), col = c('black', 'red', 'blue'), lwd = 2)

# death panel
par(mar=c(6, 4, 0, 4))
plot(cdc_lm$pi_only, type = 'l', xlab = '', ylab = '', axes = F, lwd = 2, ylim = c(400, 1400), cex.lab = sz)
axis(2, at = seq(400, 1400, by = 250), labels = seq(400, 1400, by = 250))
mtext(2, text = 'P&I deaths', line = 2, cex = sz2)
axis(1, at = seq(1, 496, by = 53), labels = wklabs, las = 2, cex = sz)
par(new=T)
plot(cdc_lm$ped_deaths, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0,20))
axis(4, at = seq(0, 20, by=4), labels = seq(0, 20, by=4), col.axis = 'blue', col = 'blue', col.ticks = 'blue')
mtext(4, text = 'ped. deaths', line = 2.5, col = 'blue', cex = sz2)
dev.off()

##########################################
# separate figures intended to stack
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F1')
par(mfrow = c(1, 1))

png(filename="ILI_diag_perc_a.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar = margin, oma = omargin)
# ILI panel
plot(sdi2$ILI_diag_perc, type = 'l', xlab = '', ylab = 'ILI % of all visits', ylim = c(0, 5), col = 'blue', xaxt = 'n', lwd = 2)
lines(cdc_lm$perc_unwt_ili, type = 'l', col = 'black', lwd = 2)
legend('topleft', c('ILINet', 'insurance claims'), lwd = 2, col = c('black', 'blue'))
dev.off()

# perc_pos panel
png(filename="perc_pos_b.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin, oma = omargin)
plot(cdc_lm$perc_pos, type = 'l', xlab = '', ylab = '% positive lab tests', col = 'black', xaxt = 'n', lwd = 2)
par(new=T)
plot(cdc_lm$a_H1, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0, 1600))
lines(cdc_lm$a_H3sum, col = 'red', type = 'l')
lines(cdc_lm$b, col = 'orange', type = 'l')
lines(cdc_lm$a_2009H1N1, col = 'green', type = 'l')
axis(4, at = seq(0, 1600, by=250), labels = seq(0, 1600, by=250))
mtext(4, text = 'Positive Lab Samples', line = 2.5)
legend('topleft', c('% pos tests', 'A/H1 samples', 'A/H3', 'B', '2009 H1N1'), col = c('black', 'blue', 'red', 'orange', 'green'), lwd = c(2, 1, 1, 1, 1))
dev.off()

# hosp panel
png(filename="hosp_rate_c.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar = margin, oma = omargin)
plot(cdc_lm$hosp_tot_diff, type = 'l', xlab = '', ylab = 'Hospitalizations per 100,000', xaxt = 'n', lwd = 2, ylim = c(0, 4))
lines(cdc_lm$hosp_5.17_diff, type = 'l', col = 'red', lwd = 2)
lines(cdc_lm$hosp_18.49_diff, type = 'l', col = 'blue', lwd = 2)
legend('topleft', c('Total Pop', '5-17 Years', '18-49 Years'), col = c('black', 'red', 'blue'), lwd = 2)
dev.off()

# death panel
png(filename="deaths_d.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar = margin)
par(oma = c(6, 1, 1, 1))
plot(cdc_lm$pi_only, type = 'l', xlab = '', ylab = 'Pneumonia & Influenza Deaths', xaxt = 'n', lwd = 2, ylim = c(400, 1300))
axis(1, at = seq(1, 496, by = 53), labels = sdi2$wk[seq(1, 496, by = 53)], las = 2)
par(new=T)
plot(cdc_lm$ped_deaths, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0,20))
axis(4, at = seq(0, 20, by=4), labels = seq(0, 20, by=4), col.axis = 'blue', col = 'blue', col.ticks = 'blue')
mtext(4, text = 'Pediatric Deaths', line = 2.5, col = 'blue')
dev.off()



##########################################
# plot % ILI of all visits for sdi2 and cdc_lm
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F1')
cdc_lm$perc_unwt_ili <- as.numeric(cdc_lm$perc_unwt_ili)

png(filename="ILI_diag_perc.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)
plot(sdi2$ILI_diag_perc, type = 'l', xlab = '', ylab = 'ILI % of all visits', ylim = c(0, 5), col = 'blue', xaxt = 'n', lwd = 2)
lines(cdc_lm$perc_unwt_ili, type = 'l', col = 'black', lwd = 2)
legend('topleft', c('ILINet', 'insurance claims'), lwd = 2, col = c('black', 'blue'))
axis(1, at = seq(1, 496, by = 53), labels = sdi2$wk[seq(1, 496, by = 53)], las = 2)
dev.off()

##########################################
# plot positive lab % for cdc_lm
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F1')

png(filename="pos_lab_perc.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)
plot(cdc_lm$perc_pos, type = 'l', xlab = '', ylab = '% positive lab tests', col = 'black', xaxt = 'n', lwd = 2)
axis(1, at = seq(1, 496, by = 53), labels = sdi2$wk[seq(1, 496, by = 53)], las = 2)
par(new=T)
plot(cdc_lm$a_H1, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0, 1600))
lines(cdc_lm$a_H3sum, col = 'red', type = 'l')
lines(cdc_lm$b, col = 'orange', type = 'l')
lines(cdc_lm$a_2009H1N1, col = 'green', type = 'l')
axis(4, at = seq(0, 1600, by=250), labels = seq(0, 1600, by=250))
mtext(4, text = 'Positive Lab Samples', line = 2.5)
legend('topleft', c('% pos tests', 'A/H1 samples', 'A/H3', 'B', '2009 H1N1'), col = c('black', 'blue', 'red', 'orange', 'green'), lwd = c(2, 1, 1, 1, 1))
dev.off()

##########################################
# hosp. rates for children and adults
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F1')

png(filename="hosp_rate.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)
plot(cdc_lm$hosp_tot_diff, type = 'l', xlab = '', ylab = 'Hospitalizations per 100,000', xaxt = 'n', lwd = 2, ylim = c(0, 4))
axis(1, at = seq(1, 496, by = 53), labels = sdi2$wk[seq(1, 496, by = 53)], las = 2)
lines(cdc_lm$hosp_5.17_diff, type = 'l', col = 'red', lwd = 2)
lines(cdc_lm$hosp_18.49_diff, type = 'l', col = 'blue', lwd = 2)
legend('topleft', c('Total Pop', '5-17 Years', '18-49 Years'), col = c('black', 'red', 'blue'), lwd = 2)
dev.off()

##########################################
# mortality counts
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F1')

png(filename="deaths.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)
plot(cdc_lm$pi_only, type = 'l', xlab = '', ylab = 'Pneumonia & Influenza Deaths', xaxt = 'n', lwd = 2, ylim = c(400, 1300))
axis(1, at = seq(1, 496, by = 53), labels = sdi2$wk[seq(1, 496, by = 53)], las = 2)
par(new=T)
plot(cdc_lm$ped_deaths, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0,20))
axis(4, at = seq(0, 20, by=4), labels = seq(0, 20, by=4), col.axis = 'blue', col = 'blue', col.ticks = 'blue')
mtext(4, text = 'Pediatric Deaths', line = 2.5, col = 'blue')
dev.off()