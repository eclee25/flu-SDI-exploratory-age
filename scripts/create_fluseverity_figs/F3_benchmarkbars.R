
## Name: Elizabeth Lee
## Date: 
## Function: 
## Filenames: 
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

# plot formatting
w = 464 
h = 464
ps = 14
margin = c(1, 4, 1, 4) + 0.1 # bottom, left, top, right
omargin = c(1, 1, 1, 1)
un = "px"

###################################
## 8/16/14 plot benchmark index long ##

# read data
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
nat <-read.csv('regression_data.csv', header=T, colClasses='numeric')

# specific formatting
seasonlab <- c('97-98', '98-99', '99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '10-11', '11-12', '12-13', '13-14')
# assign colors based on severity
# red severe, yellow moderate, blue mild
sev <- which(nat$ix_noILI> 1)
mod <- which(nat$ix_noILI<= 1 & nat$ix_noILI >= -1)
colorvec <- rep('blue',16)
colorvec[sev] <- 'red'
colorvec[mod] <- 'yellow'

# barplot
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/F3')
par(mar = margin)
png(filename="benchmarkbars.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
mids <- barplot(nat$ix_noILI, xlab='', ylab=expression(paste('Benchmark, ', beta, sep=' ')), ylim=c(-6,6), col = colorvec)
axis(1, at=mids, seasonlab, las = 2)
mtext('Season', side=1, line=3.5)
dev.off()

###################################
## plot benchmark index 01-02 to 08-09 ## 9/3/14
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
og <- read.csv('cdc_severity_index.csv', header=T, colClasses='numeric')

# specific formatting
seasonlab <- c('01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09')
# assign colors based on severity
# red severe, yellow moderate, blue mild
sev <- which(og$ix_noILI> 1)
mod <- which(og$ix_noILI<= 1 & og$ix_noILI >= -1)
colorvec <- rep('blue',8)
colorvec[sev] <- 'red'
colorvec[mod] <- 'yellow'

# barplot
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_composition')
par(mar = margin)
png(filename="benchmarkbars_orig.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
mids <- barplot(og$ix_noILI, xlab='', ylab=expression(paste('Benchmark, ', beta, sep=' ')), ylim=c(-6,6), col = colorvec)
axis(1, at=mids, seasonlab, las = 2)
mtext('Season', side=1, line=3.5)
dev.off()

###################################
## plot benchmark index 01-02 to 08-09, excesspi replacement ## 9/3/14
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
exc <- read.csv('cdc_severity_index_excesspi.csv', header=T, colClasses='numeric')

# specific formatting
seasonlab <- c('01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09')
# assign colors based on severity
# red severe, yellow moderate, blue mild
sev <- which(exc$ix_noILI> 1)
mod <- which(exc$ix_noILI<= 1 & exc$ix_noILI >= -1)
colorvec <- rep('blue',8)
colorvec[sev] <- 'red'
colorvec[mod] <- 'yellow'

# barplot
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs/Supp/bench_composition')
par(mar = margin)
png(filename="benchmarkbars_excesspi.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
mids <- barplot(exc$ix_noILI, xlab='', ylab=expression(paste('Benchmark, ', beta, sep=' ')), ylim=c(-6,6), col = colorvec)
axis(1, at=mids, seasonlab, las = 2)
mtext('Season', side=1, line=3.5)
dev.off()