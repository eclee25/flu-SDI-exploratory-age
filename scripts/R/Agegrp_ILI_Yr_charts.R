	m##############################################
###R template
###Author: Elizabeth Lee
###Date: 9/20/12	
###Function: clean and cast data to look at information by age group by year for the symptoms of interest. draw bar plots of information.
###Import data: Agegrp_ILI_Yr.csv (9/20/12: 4:12:26 PM EDT)
###Outputs: ANYDIAG_cts_yr.ps, ILI_cts_yr.ps, ILI_prop_yr.ps, ANYDIAG_cts_yryr.ps, ILI_cts_yryr.ps, ILI_prop_yryr.ps

###Command Line: R
##############################################

### packages ###
library(reshape)
library(RColorBrewer)

### functions ###

### data structures ###

### import data ###
data<-read.csv('Agegrp_ILI_Yr.csv', colClasses='character')
colnames(data)<-c('AGEGROUP', 'YEAR', 'sum_ILI_m', 'sum_ANY_DIAG_VISIT_CT', 'ILI_prop')

### figure template ###
agecol<-brewer.pal(12,"Set3")
yrcol<-brewer.pal(11, "Spectral")

### program ###

# rm TOTAL agegroup data
data2<-data[data$AGEGROUP!="TOTAL",]

# reshape data for bar plot format
colnames(data2)<-c("AGEGROUP", "YEAR", "value", "sum_ANY_DIAG_VISIT_CT", "ILI_prop")
sum_ILI_data<-data.frame(cast(data2, AGEGROUP ~ YEAR))
ILI_dta<-apply(sum_ILI_data[,2:12],2,as.numeric)
rownames(ILI_dta)<-sum_ILI_data[,1]

colnames(data2)<-c("AGEGROUP", "YEAR", "sum_ILI_m", "value", "ILI_prop")
sum_ANYDIAG_data<-data.frame(cast(data2, AGEGROUP ~ YEAR))
ANYDIAG_dta<-apply(sum_ANYDIAG_data[,2:12],2,as.numeric) #remove AGEGROUP from dataset
rownames(ANYDIAG_dta)<-sum_ANYDIAG_data[,1]

colnames(data2)<-c("AGEGROUP", "YEAR", "sum_ILI_m", "sum_ANY_DIAG_VISIT_CT", "value")
prop_ILI_data<-data.frame(cast(data2, AGEGROUP ~ YEAR))
prop_dta<-apply(prop_ILI_data[,2:12],2,as.numeric)
rownames(prop_dta)<-prop_ILI_data[,1]

# organized data for barplots (x-axis = years)
ageorder<-c(5,4,9,1,2,3,6,7,8,10,11,12)
ILI_dta2<-ILI_dta[ageorder,]/1000
ANYDIAG_dta2<-ANYDIAG_dta[ageorder,]/1000000
prop_dta2<-prop_dta[ageorder,]

# draw barplots over years
par(xpd=NA)
	postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ILI_cts_yr.ps")
barplot(ILI_dta2, ylab="ILI counts in 1000s", beside=TRUE, ylim=c(0,1400), col=agecol)
abline(h=0)
legend(4, 1300, rownames(ILI_dta2), fill=agecol)
dev.off()

postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ANYDIAG_cts_yr.ps")
barplot(ANYDIAG_dta2, ylab="Any Visit counts in millions", beside=TRUE, col=agecol, ylim=c(0,120))
abline(h=0)
legend(2, 100, rownames(ANYDIAG_dta2), fill=agecol)
dev.off()

postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ILI_prop_yr.ps")
barplot(prop_dta2, ylab="ILI as a proportion of all visits", beside=TRUE, col=agecol, ylim=c(0,.06), xlim=c(0,170))
abline(h=0)
legend(148, .05, rownames(prop_dta2), fill=agecol)
dev.off()

#draw barplot over age group
postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ILI_cts_yryr.ps")
barplot(t(ILI_dta2), ylab="ILI counts in 1000s", beside=TRUE, ylim=c(0,1400), col=yrcol)
abline(h=0)
legend(127, 1200, rownames(t(ILI_dta2)), fill=yrcol)
dev.off()

postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ANYDIAG_cts_yryr.ps")
barplot(t(ANYDIAG_dta2), ylab="Any Visit counts in millions", beside=TRUE, col=yrcol, ylim=c(0,120))
abline(h=0)
legend(6, 100, rownames(t(ANYDIAG_dta2)), fill=yrcol)
dev.off()

postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ILI_prop_yryr.ps")
barplot(t(prop_dta2), beside=TRUE, col=yrcol, ylim=c(0,.06), ylab="ILI as a proportion of all visits")
abline(h=0)
legend(126,.05, rownames(t(prop_dta2)), fill=yrcol)
dev.off()

