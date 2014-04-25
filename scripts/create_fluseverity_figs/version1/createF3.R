
## Name: Elizabeth Lee
## Date: 2/13/14
## Function: draw figure 3 manuscript
### benchmark severity index by season
### max z-OR vs benchmark index by season
### OR w/ classification (wks 2-3) and early warning (wks 48-50)
## Filenames: CDC_Source/cdc_severity_index.csv, Py_export/zOR_avgs_relative_outpatient.csv, Py_export/zOR_avgs_outpatient.csv
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

######################################
# import data
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source')
benchmark <- read.csv('cdc_severity_index.csv', colClasses = 'numeric')
slab <- c('01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10')
# drop season 1 (00-01) data

# 4/16/14 updated zOR imports
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
z_avgs <- read.csv('zOR_avgs_outpatient.csv', header=T) # 7 wk norm
z_avgs_relative <- read.csv('zOR_avgs_relative_outpatient.csv', header=T) # 7 wk moving window

seas <- 2:10
# 7 wk norm for static and relative normalization methods
avg_zOR <- data.frame(season = seas, slab = slab, zOR_retro_mn = z_avgs$retro_mn, benchmark = benchmark$ix[2:10], zOR_early_mn = z_avgs$early_mn, zOR_tot_mn = z_avgs$fluwks_mn, zOR_retromn_rel = z_avgs_relative$retro_mn, zOR_earlymn_rel = z_avgs_relative$early_mn)

# dataframe is from OR_seasonseverity.sql, health insurance claims data
ili <- c(871832, 978677, 1485711, 1763132, 1481798, 1550142, 2381998, 2314294, 4601514)
pop <- c(283987704, 286776721, 290637947, 292927888, 295132821, 298012768, 300961101, 304009593, 306500542)
AR <- ili/pop*10000
ar_fluwks <- data.frame(season = seas, slab = slab, ILI = ili, popstat = pop, ar_10000 = AR)

library(calibrate)


######################################
# plot formatting
seasonlabs <- c('2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10')
w = 450 
h = 450
ps = 14
margin = c(3, 4, 1, 2) + 0.1 # bottom, left, top, right
omargin = c(1, 1, 1, 1)
sz = 2
sz2 = 1.2
un = "px"

######################################
# plot benchmark index

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="benchmark_ix.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)

mp <- barplot(benchmark$ix, ylab = '', xlab = '', ylim = c(-5, 10), cex.lab = 2, axes = F)
axis(2, at = seq(-5, 10, by=5), labels = seq(-5, 10, by=5))
mtext(2, text = 'benchmark index', line = 2, cex = sz2)
axis(1, at = mp, labels = seasonlabs, las = 2, cex.lab = sz)
abline(h=c(0, -1, 1))
dev.off()

######################################
# avg z-OR during classification weeks (2-3) vs. benchmark index by season

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="zORretromn_benchmark_7wknorm.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)

plot(avg_zOR$benchmark, avg_zOR$zOR_retro_mn, ylab = '', xlab = '', xlim = c(-5, 10), ylim = c(-10, 25), pch = 21, bg = 'black', cex.lab = sz, cex = sz2, axes = F) # 7wk norm
axis(2, at = seq(-10, 25, by=5), labels = seq(-10, 25, by=5)) # 7wk norm
mtext(2, text = 'Z-OR mean, retrospective', line = 2, cex = sz2)
axis(1, at = seq(-5, 10, by=5), labels = seq(-5, 10, by=5))
mtext(1, text = 'benchmark index', line = 2, cex = sz2)
textxy(avg_zOR$benchmark, avg_zOR$zOR_retro_mn, labs=avg_zOR$slab, cex = 1, m = c(0, 0), pos = 2, offset = c(0, 0), cex.lab = sz)
abline(v = c(-1, 1), h = c(-1, 1))
dev.off()

# correlation coefficient = -0.470
cor(avg_zOR$benchmark, avg_zOR$zOR_retro_mn)
# correlation coefficient w/S10 = -0.676
cor(avg_zOR$benchmark[1:8], avg_zOR$zOR_retro_mn[1:8])

######################################
# attack rate across flu season (Oct to May) vs benchmark index by season

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="arfluwks_benchmark.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)

plot(avg_zOR$benchmark, ar_fluwks$ar_10000, ylab = '', xlab = '', xlim = c(-5, 10), ylim = c(0, 150), pch = 21, bg = 'black', cex.lab = sz, cex = sz2, axes = F)
axis(2, at = seq(0, 150, by=30), labels = seq(0, 150, by=30))
mtext(2, text = 'attack rate per 10,000 (flu season)', line = 2, cex = sz2)
axis(1, at = seq(-5, 10, by=5), labels = seq(-5, 10, by=5))
mtext(1, text = 'benchmark index', line = 2, cex = sz2)
textxy(avg_zOR$benchmark, ar_fluwks$ar_10000, labs=avg_zOR$slab, cex = 1, m = c(0, 0), pos = 1, offset = c(0, 0), cex.lab = sz)
abline(v = c(-1, 1))
dev.off()

# correlation coefficient = 0.785
cor(avg_zOR$benchmark, ar_fluwks$ar_10000)
# correlation coefficient w/o S10 = 0.138
cor(avg_zOR$benchmark[1:8], ar_fluwks$ar_10000[1:8])


######################################
# avg z-OR during early warning period (48-50) vs. benchmark index by season

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="zORearlymn_benchmark_7wknorm.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)

plot(avg_zOR$benchmark, avg_zOR$zOR_early_mn, ylab = '', xlab = '', xlim = c(-5, 10), ylim = c(-5, 15), pch = 21, bg = 'black', cex.lab = sz, cex = sz2, axes = F)
axis(2, at = seq(-5, 15, by=5), labels = seq(-5, 15, by=5))
mtext(2, text = 'Z-OR mean, early warning', line = 2, cex = sz2)
axis(1, at = seq(-5, 10, by=5), labels = seq(-5, 10, by=5))
mtext(1, text = 'benchmark index', line = 2, cex = sz2)
textxy(avg_zOR$benchmark, avg_zOR$zOR_early_mn, labs=avg_zOR$slab, cex = 1, m = c(0, 0), pos = 2, offset = c(0, 0), cex.lab = sz)
abline(v = c(-1, 1), h = c(-1, 1))
dev.off()

# correlation coefficient = -0.4590
cor(avg_zOR$benchmark, avg_zOR$zOR_early_mn)
# correlation coefficient w/S10 = -0.5443
cor(avg_zOR$benchmark[1:8], avg_zOR$zOR_early_mn[1:8])
       
       
######################################
# avg z-OR during total flu season (wks 40-20) vs. benchmark index by season
       
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="zORtotmn_benchmark_7wknorm.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)
      
plot(avg_zOR$benchmark, avg_zOR$zOR_tot_mn, ylab = '', xlab = '', xlim = c(-5, 10), ylim = c(-5, 15), pch = 21, bg = 'black', cex.lab = sz, cex = sz2, axes = F)
axis(2, at = seq(-5, 15, by=5), labels = seq(-5, 15, by=5))
mtext(2, text = 'Z-OR mean, entire flu season', line = 2, cex = sz2)
axis(1, at = seq(-5, 10, by=5), labels = seq(-5, 10, by=5))
mtext(1, text = 'benchmark index', line = 2, cex = sz2)
textxy(avg_zOR$benchmark, avg_zOR$zOR_tot_mn, labs=avg_zOR$slab, cex = 1, m = c(0, 0), pos = 4, offset = c(0, 0), cex.lab = sz)
abline(v = c(-1, 1), h = c(-1, 1))
dev.off()
      
# correlation coefficient = -0.409
cor(avg_zOR$benchmark, avg_zOR$zOR_tot_mn)
# correlation coefficient w/S10 = -0.593
cor(avg_zOR$benchmark[1:8], avg_zOR$zOR_tot_mn[1:8])
      
       
######################################
# avg z-OR during relative retrospective weeks (2 wks before epidemic peak) vs. benchmark index by season (outpatient/OP data only)

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="zORretromnrel_benchmark_7wknorm_op.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)

plot(avg_zOR$benchmark[1:8], avg_zOR$zOR_retromn_rel[1:8], ylab = '', xlab = '', xlim = c(-5, 5), ylim = c(-10, 25), pch = 21, bg = 'black', cex.lab = sz, cex = sz2, axes = F) # 7wk norm
axis(2, at = seq(-10, 25, by=5), labels = seq(-10, 25, by=5)) # 7wk norm
mtext(2, text = 'Z-OR mean, peak-based retrospective', line = 2, cex = sz2)
axis(1, at = seq(-5, 5, by=1), labels = seq(-5, 5, by=1))
mtext(1, text = 'benchmark index', line = 2, cex = sz2)
textxy(avg_zOR$benchmark[1:8], avg_zOR$zOR_retromn_rel[1:8], labs=avg_zOR$slab[1:8], cex = 1, m = c(0, 0), pos = 2, offset = c(0, 0), cex.lab = sz)
abline(v = c(-1, 1), h = c(-1, 1))
dev.off()

# correlation coefficient = -0.536
cor(avg_zOR$benchmark, avg_zOR$zOR_retromn_rel)
# correlation coefficient w/S10 = -0.795
cor(avg_zOR$benchmark[1:8], avg_zOR$zOR_retromn_rel[1:8])


######################################
# avg z-OR during relative early warning period (wk after Thanksgiving +1) vs. benchmark index by season (outpatient/OP data only)

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
png(filename="zORearlymnrel_benchmark_7wknorm_op.png", units="px", width=w, height=h, pointsize=ps, bg = 'white')
par(mar=margin)

plot(avg_zOR$benchmark[1:8], avg_zOR$zOR_earlymn_rel[1:8], ylab = '', xlab = '', xlim = c(-5, 5), ylim = c(-5, 15), pch = 21, bg = 'black', cex.lab = sz, cex = sz2, axes = F)
axis(2, at = seq(-5, 15, by=5), labels = seq(-5, 15, by=5))
mtext(2, text = 'Z-OR mean, Thanksgiving early warning', line = 2, cex = sz2)
axis(1, at = seq(-5, 5, by=1), labels = seq(-5, 5, by=1))
mtext(1, text = 'benchmark index', line = 2, cex = sz2)
textxy(avg_zOR$benchmark[1:8], avg_zOR$zOR_earlymn_rel[1:8], labs=avg_zOR$slab[1:8], cex = 1, m = c(0, 0), pos = 2, offset = c(0, 0), cex.lab = sz)
abline(v = c(-1, 1), h = c(-1, 1))
dev.off()

# correlation coefficient = -0.507
cor(avg_zOR$benchmark, avg_zOR$zOR_earlymn_rel)
# correlation coefficient w/S10 = -0.557
cor(avg_zOR$benchmark[1:8], avg_zOR$zOR_earlymn_rel[1:8])
       
       
       
       

    
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       

       