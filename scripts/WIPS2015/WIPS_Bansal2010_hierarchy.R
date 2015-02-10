
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

setwd('/home/elee/R/source_functions')
source("dfsumm.R")

###########
## plotting settings ##
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

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/WIPS2015/importData/')
childdata <- scan('child_attack_rate.txt')
childdata2 <- as.numeric(childdata)
adultdata <- scan('adult_attack_rate.txt')
adultdata2 <- as.numeric(adultdata)

setwd('/home/elee/Dropbox/Department/Presentations/2015_WIPS/Figures')
png('Bansal2010_HierarchicalAgeSpread_R.png', , units=un, width=w, height=h, pointsize=ps, bg = 'white')
par(mfrow=c(1,1), mar=c(4,4,0.5,0.5), oma=c(1,1,1,1))

plot(childdata2, type='l', col='red', lwd=linewidth, xlab='Time (days)', 'ylab'='Attack Rate', cex.lab=lab_sz, cex.main=main_sz, cex.axis=axis_sz, xlim=c(0,100))
lines(adultdata2, col='blue', lwd=linewidth)
abline(v=c(which(adultdata2==max(adultdata2)), which(childdata2==max(childdata2))), col=c('blue', 'red'), lwd=1)
legend(63.5, 0.077, c('children', 'adults'), col=c('red', 'blue'), lwd=linewidth, lty=1, cex=axis_sz)
dev.off()
