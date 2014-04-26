
## Name: Elizabeth Lee
## Date: 4/26/14
## Function: draw figure 1 for manuscript
### 10-year time series panels: SDI ILI % of total visits (outpatient only) & ILINet ILI % of total visits, positive lab test percentages, hospital rate for children, hospital rate for adults, pediatric deaths, P&I mortality
## Filenames: SQL_export/F1.csv, CDC_Source/Import_Data/all_cdc_source_data.csv
## Data Source: 'season', 'wk', 'yr', 'wknum', 'ILI', 'anydiag', 'pop'
## Notes: cF1.csv: 'season', 'wk', 'yr', 'wknum', 'outpatient & office ILI', 'outpatient & office anydiag', 'pop'
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
wkticks = seq(1, 550, by = 50)
wklabs = substr(sdi2$wk[wkticks], 1, 7)


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
legend('topleft', c('ILINet', 'outpatient claims'), lwd = 2, col = c('black', 'blue'))

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
axis(4, at = seq(0, 1600, by=500), labels = seq(0, 1600, by=500), col.axis = 'blue', col = 'blue')
mtext(4, text = 'pos. lab samples', line = 2.5, cex = sz2, col = 'blue')
legend('topleft', c('% pos tests', 'A/H1 samples', 'A/H3', 'B', '2009 H1N1'), col = c('black', 'blue', 'red', 'orange', 'green'), lwd = c(2, 1, 1, 1, 1))

# hosp panel
par(mar=margin)
plot(cdc_lm$hosp_tot_diff, type = 'l', xlab = '', ylab = '', axes = F, lwd = 2, ylim = c(0, 4), cex.lab = sz)
axis(2, at = seq(0, 4, by=1), labels=seq(0, 4, by=1))
mtext(2, text = 'hosp. by 100,000', line = 2, cex = sz2)
lines(cdc_lm$hosp_5.17_diff, type = 'l', col = 'red', lwd = 2)
lines(cdc_lm$hosp_18.49_diff, type = 'l', col = 'blue', lwd = 2)
legend('topleft', c('Total Pop', '5-17 Years', '18-49 Years'), col = c('black', 'red', 'blue'), lwd = 2)

# death panel
par(mar=c(6, 4, 0, 4))
plot(cdc_lm$pi_only, type = 'l', xlab = '', ylab = '', axes = F, lwd = 2, ylim = c(400, 1400), cex.lab = sz)
axis(2, at = seq(400, 1400, by = 250), labels = seq(400, 1400, by = 250))
mtext(2, text = 'P&I deaths', line = 2, cex = sz2)
axis(1, at = wkticks, labels = wklabs, las = 2, cex = sz)
par(new=T)
plot(cdc_lm$ped_deaths, col = 'blue', type = 'l', axes = F, ylab = '', xlab = '', ylim = c(0,20))
axis(4, at = seq(0, 20, by=10), labels = seq(0, 20, by=10), col.axis = 'blue', col = 'blue', col.ticks = 'blue')
mtext(4, text = 'ped. deaths', line = 2.5, col = 'blue', cex = sz2)
dev.off()
